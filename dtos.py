from typing import Literal
from pydantic import BaseModel, Field

class PostOptionsRequest(BaseModel):
    platform: Literal['linkedin', 'facebook', 'twitter', 'blog']
    point_of_view: str = None
    primary_key_phrase: str = None
    post_format: Literal[]
    use_emojis: bool = None
    additional_prompt: str = None
    word_count: int = None
    
class QueryDto(BaseModel):
    script: str
    link: str
    options: PostOptionsRequest

class Item(BaseModel):
    script: str
    link: str | None = None
    platform: str | None = None

class ScriptDto(BaseModel):
    script:str