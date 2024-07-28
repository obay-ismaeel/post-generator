from fastapi import FastAPI
from pydantic import BaseModel
from llama_service import CreatePost

app = FastAPI()

class Item(BaseModel):
    script: str
    link: str

@app.post('/blog')
async def generate_linkedin(item:Item):
    return await CreatePost(item.script, item.link, "blog")

@app.post('/linkedin')
async def generate_linkedin(item:Item):
    return await CreatePost(item.script, item.link, "linkedin")

@app.post('/twitter')
async def generate_linkedin(item:Item):
    return await CreatePost(item.script, item.link, "twitter")

@app.post('/facebook')
async def generate_linkedin(item:Item):
    return await CreatePost(item.script, item.link, "facebook")