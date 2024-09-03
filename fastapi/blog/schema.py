from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    id: int
    title: str
    author: str
    written_date: str
    content: str
    likes: int
    published: Optional[bool] 
