from dataclasses import dataclass
from liveline.presentation.slides import BaseSlide
from liveline.presentation.slide import Slide
from typing import List, Type, Dict, Any


@dataclass
class Presentation:
    slides: List[Type[BaseSlide]]
    name: str
    identifier: str

    @staticmethod
    def deserialize_presentation(inp: Dict[str, Any]):
        return Presentation(BaseSlide.deserialize_slides(inp["slides"]), inp["name"], inp["identifier"])

    @staticmethod
    def deserialize_presentations(inp: Dict[str, Any]):
        pres_list = inp["presentations"]
        pres_list_deserialized = []
        for json_pres in pres_list:
            pres_list_deserialized.append(
                Presentation.deserialize_presentation(json_pres)
            )
        return pres_list_deserialized


@dataclass
class WidgetBasedPresentation:
    slides: List[Type[Slide]]
    name: str
    identifier: str
