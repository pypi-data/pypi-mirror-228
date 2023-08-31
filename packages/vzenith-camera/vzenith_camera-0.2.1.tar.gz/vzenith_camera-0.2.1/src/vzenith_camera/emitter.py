from typing import Dict, List
from abc import ABC

from .types import Event, EventListener


class Emitter(ABC):
    _events: Dict[str, List[EventListener]]

    def __init__(self):
        self._events = {}

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
