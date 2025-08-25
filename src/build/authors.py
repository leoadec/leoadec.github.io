from dataclasses import dataclass
from typing import Self

@dataclass
class MultiScriptName:
    anglicized: str | None = None
    transliteration: str | None = None
    original: str | None = None

@dataclass
class Author:
    full_name: str | None = None

    first_name: str | None = None
    middle_initial: str | None = None
    last_name: str | None = None

    given_name: MultiScriptName | None = None
    family_name: MultiScriptName | None = None

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        if full_name := data.get("full_name"):
            return cls(full_name=full_name)

        if (first_name := data.get("first_name")) and (last_name := data.get("last_name")):
            return cls(
                first_name=first_name,
                middle_initial=data.get("middle_initial"),
                last_name=last_name,
            )

        if (given_name := data.get("given_name")) and (family_name := data.get("family_name")):
            return cls(
                given_name=MultiScriptName(**given_name),
                family_name=MultiScriptName(**family_name),
            )

        raise

    def render(self: Self) -> str:
        if self.full_name:
            return self.full_name

        if self.first_name and self.last_name:
            if self.middle_initial:
                return f"{self.first_name} {self.middle_initial}. {self.last_name}" 
            return f"{self.first_name} {self.last_name}" 

        if self.given_name and self.family_name:
            return f"{self.given_name.transliteration} {self.family_name.transliteration}"

        raise
