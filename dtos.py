from typing import Literal
from pydantic import BaseModel, Field

class QueryDto(BaseModel):
    script: str
    link: str
    platform: Literal['linkedin', 'facebook', 'twitter', 'blog']
    post_type: str | None = None
    word_count: int | None = None
    user_prompt: str | None = None
    
class Item(BaseModel):
    script: str
    link: str
    platform: str | None = None

class ScriptDto(BaseModel):
    script:str