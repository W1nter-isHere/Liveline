from __future__ import annotations
from dataclasses import dataclass, asdict
from liveline.presentation.slides import BaseSlide
from typing import List, Type, Dict, Any


@dataclass
class Presentation:
    slides: List[Type[BaseSlide]]
    name: str
    identifier: str
    creator: str

    @staticmethod
    def deserialize_presentation(inp: Dict[str, Any]):
        return Presentation(
            BaseSlide.deserialize_slides(inp["slides"]),
            inp["name"],
            inp["identifier"],
            inp["creator"],
        )

    @staticmethod
    def deserialize_presentations(inp: Dict[str, Any]):
        pres_list = inp["presentations"]
        pres_list_deserialized = []
        for json_pres in pres_list:
            pres_list_deserialized.append(
                Presentation.deserialize_presentation(json_pres)
            )
        return pres_list_deserialized

    @staticmethod
    def serialize_presentations(presentations: List[Presentation]):
        pres = []
        for presentation in presentations:
            if isinstance(presentation, dict):
                pres.append(presentation)
            else:
                pres.append(asdict(presentation))
        return pres
