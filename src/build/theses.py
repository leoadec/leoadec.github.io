from dataclasses import dataclass
from typing import Self

from authors import Author

@dataclass
class Thesis:
    title: str
    external_url: str
    language: str
    supervisor: Author
    original_title: str | None = None

    @classmethod
    def from_dict(cls, data: dict, authors: Author) -> Self:
        return cls(
            title = data["title"],
            external_url = data["external_url"],
            language = data["language"],
            original_title = data.get("original_title"),
            supervisor = authors[data["supervisor"]],
        )

    def render(self) -> dict:
        output = {
            "title": self.title,
            "external_url": self.external_url,
            "language": self.language,
            "supervisor": self.supervisor.render(),
        }
        if self.original_title:
            output["original_title"] = self.original_title
        return output
