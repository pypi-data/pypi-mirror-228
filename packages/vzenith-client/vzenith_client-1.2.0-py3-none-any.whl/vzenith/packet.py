from __future__ import annotations

from enum import Enum


class PacketType(Enum):
    DATA = 0
    HEARTBEAT = 1
    BINARY = 2


class PacketHeader:
    type: PacketType
    length: int
    sn: int

    def __init__(self, length: int, sn: int = 0):
        self.length = length & 0xffffffff
        self.sn = sn & 0xff

        if length == 0:
            self.type = PacketType.HEARTBEAT
        else:
            self.type = PacketType.DATA

    def bytes(self) -> bytearray:
        return bytearray(
            [
                0x56, 0x5a,
                self.type.value,
                self.sn,
                (self.length >> 24) & 0xff,
                (self.length >> 16) & 0xff,
                (self.length >> 8) & 0xff,
                (self.length & 0xff)
            ]
        )

    @staticmethod
    def parse(b: bytearray) -> PacketHeader | None:
        if len(b) == 0 or b[0] != 0x56 or b[1] != 0x5a:
            return None

        length = 0
        length += (0x000000ff & (int(b[4]))) << 24
        length += (0x000000ff & (int(b[5]))) << 16
        length += (0x000000ff & (int(b[6]))) << 8
        length += (0x000000ff & (int(b[7])))

        return PacketHeader(length, b[3])


class Packet:
    header: PacketHeader
    data: bytearray | None

    def __init__(self, data: bytearray | None = None):
        if data is None:
            self.header = PacketHeader(0)
        else:
            self.header = PacketHeader(len(data))

        self.data = data

    def bytes(self) -> bytearray:
        packet = self.header.bytes()

        if self.data is not None:
            packet += self.data

        return packet
