from dataclasses import dataclass

@dataclass
class Note:
    id: int|None
    user_id: int|None
    name: str|None
    contents: str|None