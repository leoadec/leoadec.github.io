from dataclasses import dataclass
from typing import Self

@dataclass
class Author:
    full_name: str | None

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(full_name=data["full_name"])

    def render(self: Self) -> str:
        return self.full_name
