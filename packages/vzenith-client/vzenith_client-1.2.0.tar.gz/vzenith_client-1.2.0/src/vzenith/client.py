from __future__ import annotations
import json
import logging
import time
from socket import socket, AF_INET, SOCK_STREAM, MSG_DONTWAIT
from threading import Thread

from .event import Emitter
from .packet import Packet, PacketHeader, PacketType


class LicensePlateRecognizer(Emitter):
    name: str
    address: str
    port: int

    _socket: socket
    _ivs_thread: IvsResultThread | None

    def __init__(self, name: str, address: str, port: int = 8131):
        self.name = name
        self.address = address
        self.port = port

        self._socket = socket(AF_INET, SOCK_STREAM)
        self._ivs_thread = None

        self._events = {}

    def send_request(self, cmd: dict, sn: int = 0):
        packet = Packet(bytearray(json.dumps(cmd, ensure_ascii=False).encode('gb2312')))

        if sn != 0:
            packet.header.sn = sn

        self.send_data(packet.bytes())

    def send_data(self, data: bytearray):
        self.log_debug(f'send: {data}')
        self._socket.send(data)

    def recv_response(self) -> dict | None:
        header = self.recv_header()

        if header is None or header.type == PacketType.HEARTBEAT:
            return None

        data = self.recv_data(header.length)

        if data is None:
            return None

        return json.loads(data.decode('gb2312'))

    def recv_header(self, nonblocking: bool = False) -> PacketHeader | None:
        data = self.recv_data(8, nonblocking)

        if data is None or data[0] != 0x56 or data[1] != 0x5a:
            return None

        return PacketHeader.parse(data)

    def recv_data(self, n: int, nonblocking: bool = False) -> bytearray | None:
        data = bytearray()

        if nonblocking:
            flags = MSG_DONTWAIT
        else:
            flags = 0

        while len(data) < n:
            byte = self._socket.recv(n - len(data), flags)

            if not byte:
                return None

            data.extend(byte)

        self.log_debug(f'recv: {data}')
        return data

    def heartbeat(self):
        self.send_data(Packet(None).bytes())

    def log_debug(self, msg: str):
        logging.debug('[%s:%d] %s', self.address, self.port, msg)

    def connect(self):
        self._socket.connect((self.address, self.port))
        self.log_debug('connected')

    def cmd_getsn(self) -> dict:
        self.send_request({'cmd': 'getsn'})

        return self.recv_response()

    def cmd_ivsresult(self, enable: bool = False, result_format: str = 'json', image: bool = True, image_type: int = 0):
        if enable:
            if self._ivs_thread is not None:
                return

            cmd = {
                'cmd': 'ivsresult',
                'enable': enable,
                'format': result_format,
                'image': image,
                'image_type': image_type
            }

            self.send_request(cmd)
            assert self.recv_response()['state_code'] == 200

            self._ivs_thread = IvsResultThread(self)
            self._ivs_thread.enable = True
            self._ivs_thread.start()
        else:
            self._ivs_thread.enable = False
            self._ivs_thread = None


class IvsResultThread(Thread):
    enable: bool

    def __init__(self, client: LicensePlateRecognizer, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.client = client

    def run(self) -> None:
        count = 0

        while self.enable:
            if count > 3:
                self.client.heartbeat()
                count = 0

            count += 1

            try:
                header = self.client.recv_header(nonblocking=True)
                if header and header.length > 0:
                    data = self.client.recv_data(header.length)

                    if data is not None:
                        self.client.emit('ivsresult', json.loads(data[0:data.index(0x00) - 1].decode('gb2312')))

            except BlockingIOError:
                ...

            time.sleep(1)
