from dataclasses import dataclass
from typing import Self

from authors import Author

@dataclass
class Talk:
    title: str
    authors: list[Author]

    @classmethod
    def from_dict(cls, data: dict, authors: dict[str, Author]) -> Self:
        return cls(
            title=data["title"], authors=[authors[author_key] for author_key in data["authors"]]
        )

    def render(self) -> dict:
        return {
            "title": self.title,
            "authors": ", ".join([author.render() for author in self.authors]),
        }
