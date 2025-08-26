from dataclasses import dataclass
from typing import Self

from locations import Location
from posters import Poster
from talks import Talk

@dataclass
class Conference:
    name: str
    year: int
    location: Location
    talk: Talk | None = None
    poster: Poster | None = None

    @classmethod
    def from_dict(
        cls,
        data: dict,
        locations: dict[str, Location],
        posters: dict[str, Poster],
        talks: dict[str, Talk],
    ) -> Self:
        return cls(
            name=data["name"],
            year=data["year"],
            location=locations[data["location"]],
            poster=posters.get(data.get("poster", "")),
            talk=talks.get(data.get("talk", "")),
        )

    def render(self) -> dict:
        output = {
            "name": self.name,
            "year": self.year,
            "location": self.location.render(),
        }
        if self.talk:
            output["talk"] = self.talk.render()
        if self.poster:
            output["poster"] = self.poster.render()
        return output
