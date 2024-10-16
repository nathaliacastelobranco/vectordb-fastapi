# Data validation
from pydantic import BaseModel

class Query(BaseModel):
    query: str
    neighbours: int = 3