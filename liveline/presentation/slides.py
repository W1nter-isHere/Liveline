from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any

@dataclass
class BaseSlide:
    typ: str = field(init=False)
    title: str

    def __post_init__(self):
        self.typ = type(self).__name__

    @staticmethod
    def deserialize_slide(slide_json):
        TYPE = slide_json["typ"]

        if TYPE == "TitleSlide":
            return TitleSlide(slide_json["title"], slide_json["image"])
        elif TYPE == "TextSlide":
            return TextSlide(
                slide_json["title"], slide_json["text"], slide_json["image"]
            )
        elif TYPE == "ImageSlide":
            return ImageSlide(slide_json["title"], slide_json["images"])
        elif TYPE == "PollSlide":
            return PollSlide(slide_json["title"], slide_json["image"], slide_json["options"])

        return BaseSlide(slide_json["title"])

    @staticmethod
    def deserialize_slides(slides_json: Dict[str, Any]):
        slides = []
        for slide_dict in slides_json:
            slides.append(BaseSlide.deserialize_slide(slide_dict))
        return slides


@dataclass
class TitleSlide(BaseSlide):
    image: Optional[str] = None


@dataclass
class TextSlide(BaseSlide):
    text: str
    image: Optional[str]


@dataclass
class ImageSlide(BaseSlide):
    images: List[str]

@dataclass
class PollSlide(BaseSlide):
    image: Optional[str]
    options: List[str]

TEMPLATE_TITLE = TitleSlide(
    "Title",
    None
)

TEMPLATE_TEXT = TextSlide(
    "Title",
    "content",
    None
)

TEMPLATE_IMAGE = ImageSlide(
    "Title",
    [
        "https://imgur.com/Kv504Sh"
    ]
)