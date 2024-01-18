from pydantic import BaseModel

class Shoe(BaseModel):
    """
    Schema for the response body
    """
    name: str
    colors: str
    dateUpdated: str


class ColouredItem(BaseModel):
    """
    Schema for request body for querying latest n shoes of the required color
    """
    n: int
    color:str