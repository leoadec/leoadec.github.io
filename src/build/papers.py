from dataclasses import dataclass
from typing import Self

from authors import Author

@dataclass
class Paper:
    title: str
    authors: list[Author]
    journal: str
    volume: int
    pages: str
    year: int
    url: str | None
    doi: str | None
    arXiv: str | None

    @classmethod
    def from_dict(cls, data: dict, authors: dict[str, Author]) -> Self:
        return cls(
            title=data["title"],
            authors=[authors[author_key] for author_key in data["authors"]],
            journal=data["journal"],
            volume=data["volume"],
            pages=data["pages"],
            year=data["year"],
            url=data.get("url"),
            doi=data.get("doi"),
            arXiv=data.get("arXiv"),
        )

    def render(self) -> dict:
        output = {
            "title": self.title,
            "authors": ", ".join([author.render() for author in self.authors]),
            "journal": self.journal,
            "volume": self.volume,
            "pages": str(self.pages),
            "year": self.year,
        }
        if self.url:
            output["url"] = self.url
        if self.doi:
            output["doi"] = self.doi
        if self.arXiv:
            output["arXiv"] = self.arXiv
        return output
