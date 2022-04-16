from typing import Any, Tuple
from enum import Enum
from dataclasses import dataclass

TEXT_WIDGET = 0
IMAGE_WIDGET = 1


@dataclass
class Widget:
    content: Any
    widget_type: int
    position: Tuple[int, int]


@dataclass
class ImageWidget(Widget):
    size: Tuple[int, int]
