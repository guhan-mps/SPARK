from pydantic import BaseModel

class Shoe(BaseModel):
    name: str
    colors: str
    dateUpdated: str


class ColouredItem(BaseModel):
    n: int
    color:str