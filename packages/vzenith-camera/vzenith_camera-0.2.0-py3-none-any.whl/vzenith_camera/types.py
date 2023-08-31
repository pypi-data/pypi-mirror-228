from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Event:
    name: str
    target: Any


EventListener = Callable[[Event, Any], None]


@dataclass
class PlateResult:
    license: str
