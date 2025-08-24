from dataclasses import dataclass
from typing import Self

from locations import Location

@dataclass
class Job:
    start: int
    end: int | None
    title: str
    employer: str
    location: Location

    @classmethod
    def from_dict(cls, data: dict, locations: dict[str, Location]) -> Self:
        return Job(
            start=data["start"],
            end=data.get("end"),
            title=data["title"],
            employer=data["employer"],
            location=locations[data["location"]],
        )

    def render(self: Self) -> dict:
        output = {
            "start": self.start,
            "title": self.title,
            "employer": self.employer,
            "location": self.location.render(),
        }
        if self.end is not None:
            output["end"] = self.end
        return output
