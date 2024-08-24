from pydantic import BaseModel

class Item(BaseModel):
    script: str
    link: str

class ScriptDto(BaseModel):
    script:str