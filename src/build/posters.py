from dataclasses import dataclass
from typing import Self

from authors import Author

@dataclass
class Poster:
    authors: list[Author]
    title: str

    @classmethod
    def from_dict(cls, data: dict, authors: dict[str, Author]) -> Self:
        return cls(
            title=data["title"], authors=[authors[key] for key in data["authors"]]
        )

    def render(self) -> dict:
        return {
            "title": self.title, "authors": [author.render() for author in self.authors]
        }
