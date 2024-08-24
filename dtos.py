from typing import Literal, Optional
from pydantic import BaseModel, Field

class PostOptionsRequest(BaseModel):
    platform: Literal['linkedin', 'facebook', 'twitter', 'blog']
    post_format: Literal['auto', 'summary', 'promotional'] = 'auto'
    point_of_view: Optional[Literal['auto', 'FirstPersonSingular', 'FirstPersonPlural', 'SecondPerson', 'ThirdPerson']] = 'auto'
    use_emojis: Optional[bool] = True
    additional_prompt: Optional[str] = None
    word_count: Optional[int] = None

class QueryDto(BaseModel):
    script: str
    link: Optional[str] = None
    options: PostOptionsRequest

class Item(BaseModel):
    script: str
    link: str | None = None
    platform: str | None = None

class ScriptDto(BaseModel):
    script:str