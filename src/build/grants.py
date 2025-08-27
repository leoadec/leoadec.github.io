from dataclasses import dataclass
from typing import Self

@dataclass
class Grant:
    title: str
    project: str
    external_url: str
    agency: str
    start: int
    end: int | None

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            title=data["title"],
            project=data["project"],
            external_url=data["external_url"],
            agency=data["agency"],
            start=data["start"],
            end=data["end"],
        )

    def render(self) -> Self:
        return {
            "title": self.title,
            "project": self.project,
            "external_url": self.external_url,
            "agency": self.agency,
            "start": self.start,
            "end": self.end,
        }
