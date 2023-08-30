from dataclasses import dataclass
from typing import Callable, List, Any
from abc import ABC


@dataclass
class Event:
    name: str
    target: Any


EventListener = Callable[[Event, ...], None]


class Emitter(ABC):
    _events: dict[str, List[EventListener]]

    def on(self, event: str, listener: EventListener):
        if event not in self._events:
            self._events[event] = []

        self._events[event].append(listener)

    def emit(self, event: str, *args) -> bool:
        if event not in self._events:
            return False

        for listener in self._events[event]:
            listener(Event(name=event, target=self), *args)

        return True
