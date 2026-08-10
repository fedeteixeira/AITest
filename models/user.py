from dataclasses import dataclass

@dataclass
class User:
    id: int|None
    first_name: str|None
    last_name: str|None

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"