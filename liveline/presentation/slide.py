from .widget import Widget
from typing import List, Type
from dataclasses import dataclass


@dataclass
class Slide:
    widgets: List[Type[Widget]]
    background: str
