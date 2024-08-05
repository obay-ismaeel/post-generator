from pydantic import BaseModel
from llama_service import CreatePost, CreateTitle
# import whisper
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class Item(BaseModel):
    script: str
    link: str

@app.post('/api/blog')
async def generate_linkedin(item:Item):
    blog = await CreatePost(item.script, item.link, "blog")
    title = await CreateTitle(item.script, "blog")

    return {"title": title, "post": blog}

@app.post('/api/linkedin')
async def generate_linkedin(item:Item):
    post = await CreatePost(item.script, item.link, "linkedin")

    return {"post": post}

@app.post('/api/twitter')
async def generate_linkedin(item:Item):
    post = await CreatePost(item.script, item.link, "twitter")

    return {"post": post}

@app.post('/api/facebook')
async def generate_linkedin(item:Item):
    post = await CreatePost(item.script, item.link, "facebook")

    return {"post": post}

@app.post('/api/youtubetitle')
async def generate_linkedin(item:Item):
    title = await CreateTitle(item.script, "youtube")

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