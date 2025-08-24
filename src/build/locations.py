from dataclasses import dataclass

@dataclass
class Location:
    city: str
    country: str
    state: str | None = None

    def render(self) -> str:
        if self.state is not None:
            return ", ".join([self.city, self.state, self.country])
        return ", ".join([self.city, self.country])

    @classmethod
    def from_dict(cls, data: dict):
        return cls(city=data.get("city"), state=data.get("state"), country=data.get("country"))
