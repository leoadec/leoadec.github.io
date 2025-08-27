from dataclasses import dataclass
from typing import Self

from grants import Grant
from locations import Location
from theses import Thesis

@dataclass
class Degree:
    start: int
    title: str
    university: str
    location: Location
    end: int | None = None
    grant: Grant | None = None
    thesis: Thesis | None = None

    @classmethod
    def from_dict(cls, data: dict, locations: dict, grants: dict, theses: dict) -> Self:
        return cls(
            start=data["start"],
            title=data["title"],
            university=data["university"],
            location=locations[data["location"]],
            end=data.get("end"),
            grant=grants.get(data.get("grant", "")),
            thesis=theses.get(data.get("thesis", "")),
        )

    def render(self) -> dict:
        output = {
            "start": self.start,
            "title": self.title,
            "university": self.university,
            "location": self.location.render(),
        }
        if self.end:
            output["end"] = self.end

        if self.grant:
            output["grant"] = self.grant.render()

        if self.thesis:
            output["thesis"] = self.thesis.render()

        return output
