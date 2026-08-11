from pydantic import BaseModel
class Note(BaseModel):
    id: int|None
    user_id: int|None
    name: str|None
    contents: str|None