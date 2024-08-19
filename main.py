from pydantic import BaseModel
from llama_service import CreatePost, CreateTitle
from langchain_service import CreatePostLangchain
# import whisper
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class Item(BaseModel):
    script: str
    link: str

class ScriptDto(BaseModel):
    script:str

@app.post('/api/blog')
async def generate_blog(item:Item):
    blog = await CreatePost(item.script, item.link, "blog")
    title = await CreateTitle(item.script, "blog")

    return {"title": title, "post": blog}

@app.post('/api/linkedin')
async def generate_linkedin(item:Item):
    post = await CreatePost(item.script, item.link, "linkedin")

    return {"post": post}

@app.post('/api/twitter')
async def generate_twitter(item:Item):
    post = await CreatePost(item.script, item.link, "twitter")

    return {"post": post}

@app.post('/api/facebook')
async def generate_facebook(item:Item):
    post = await CreatePost(item.script, item.link, "facebook")

    return {"post": post}

@app.post('/api/title')
async def generate_title(dto:ScriptDto):
    title = await CreateTitle(dto.script, "youtube")

    return {"title": title}

###
# websocket
###

@app.websocket("/api/linkedin")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        data = await websocket.receive_json()
        dto = Item(**data)
        for i in range(4):
            post =  await CreatePost(dto.script, dto.link, "linkedin")
            await websocket.send_json({"post": post})
        await websocket.close(code=1000, reason="All posts sent")
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.close(code=1011, reason=f"Server error: {e}")
        print(f"Error: {e}")

# model = whisper.load_model("base")

# @app.post("/api/whisper")
# async def get_transcribe(file: UploadFile = File(...)):
#     current_directory = Path.cwd()

#     file_path = f"{current_directory}{file.filename}"
#     with open(file_path, "wb") as f:
#         f.write(await file.read())

#     result = model.transcribe(file_path)

#     os.remove(file_path)

#     transcription_text = result.get("text", "")

#     return JSONResponse(content={"text": transcription_text})


@app.post('/api/test')
async def generate_test(item:Item):
    post = await CreatePostLangchain(item.script, item.link, "facebook")

    return {"post": post}