import os
import uuid
from dtos import Item, ScriptDto
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from llama_service import CreatePost, CreateTitle
from langchain_service import CreatePostLangchain, semantic_search
from media_service import extract_top_frames_from_video
from rating_service import analyze_post
from whisper_service import get_transcribe
from fastapi import FastAPI, Form, HTTPException, WebSocket, WebSocketDisconnect, File, UploadFile
import logging

app = FastAPI()

# Serve the output directory as static files

app.mount("/output", StaticFiles(directory="output"), name="output")

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

# @app.post("/api/whisper")
# async def get_transcribe_whisper(file: UploadFile = File(...)):
#     return await get_transcribe(file)

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



@app.post('/api/langchain')
async def generate_test(item:Item):
    post = await CreatePostLangchain(item.script, item.link, "facebook")
    return {"post": post}

@app.post('/api/search')
async def search():
    return semantic_search("instagram")


@app.post('/api/blog')
async def generate_blog(script: str = Form(...), link: str = Form(...), video_file: UploadFile = File(...)):
    unique_id = str(uuid.uuid4())
    video_path = f"temp_video{unique_id}.mp4"

    with open(video_path, "wb") as f:
        while chunk := await video_file.read(1024):
            f.write(chunk)

    blog = await CreatePost(script, link, "blog")
    title = await CreateTitle(script, "blog")
    rate = await analyze_post(blog)
    top_frame_paths = await extract_top_frames_from_video(video_path)

    base_url = "http://127.0.0.1:8000/output/"
    top_frame_urls = [base_url + os.path.basename(path) for path in top_frame_paths]

    if os.path.exists(video_path):
        logging.log(1, f"Video '{video_path}' has been successfully deleted.")
        os.remove(video_path)

    return JSONResponse(content={"title": title, "post": blog, "rate": rate, "images": top_frame_urls})
    # return {"title": title, "post": blog, "rate": rate, "images": top_frame_urls}


@app.delete('/api/image')
async def delete_image(name: str = Form(...)):
    image_directory = os.path.join(os.getcwd(), "output")

    image_path = os.path.join(image_directory, name)

    if os.path.exists(image_path):
        os.remove(image_path)

        logging.log(1, f"Image '{name}' has been successfully deleted.")

        return JSONResponse(content={"message": f"Image '{name}' has been successfully deleted."}, status_code=204)
        # return {"message": f"Image '{name}' has been successfully deleted."}

    else:
        logging.error(1, f"Image '{name}' not found.")
        raise HTTPException(status_code=404, detail=f"Image '{name}' not found.")


# uvicorn.run(app, host="127.0.0.1", port=8000)