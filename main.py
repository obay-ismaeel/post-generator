import os
import uuid
from dtos import Item, QueryDto, ScriptDto
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from langchain_service import generate_post, generate_title
from media_service import extract_top_frames_from_video
from rating_service import analyze_post
from whisper_service import get_transcribe
from fastapi import FastAPI, Form, HTTPException, WebSocket, WebSocketDisconnect, File, UploadFile
import logging

app = FastAPI()

# Serve the output directory as static files
app.mount("/output", StaticFiles(directory="output"), name="output")

@app.post('/api/generate')
async def generate(dto:QueryDto):
    post = await generate_post(dto)
    
    rating = await analyze_post(post)
    
    title = None

    if(dto.platform == "blog"):
        title = await generate_title(dto.script, "blog")
    
    return { "post": post, "title": title, "rating": rating }

@app.post('/api/title')
async def generate_title(dto:ScriptDto):
    title = await generate_title(dto.script, "youtube")

    return {"title": title}

@app.post("/api/whisper")
async def get_transcribe_whisper(file: UploadFile = File(...)):
    return await get_transcribe(file)

###
# websocket
###

@app.post('/api/upload-video')
async def upload_video(video_file: UploadFile = File(...)):
    unique_id = str(uuid.uuid4())
    video_path = f"temp_video{unique_id}.mp4"
    
    try:
        with open(video_path, "wb") as f:
            while chunk := await video_file.read(1024):
                f.write(chunk)
        
        top_frame_paths = await extract_top_frames_from_video(video_path)

        # Generate URLs for the extracted frames
        base_url = "http://127.0.0.1:8000/output/"
        top_frame_urls = [base_url + os.path.basename(path) for path in top_frame_paths]

        # Clean up: remove the video file after processing
        if os.path.exists(video_path):
            logging.log(1, f"Video '{video_path}' has been successfully deleted.")
            os.remove(video_path)

        return JSONResponse(content={"images": top_frame_urls})
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the video: {str(e)}")


@app.delete('/api/image')
async def delete_image(name: str = Form(...)):
    image_directory = os.path.join(os.getcwd(), "output")
    image_path = os.path.join(image_directory, name)

    try:
        if os.path.exists(image_path):
            os.remove(image_path)
            logging.log(1, f"Image '{name}' has been successfully deleted.")
            return JSONResponse(content={"message": f"Image '{name}' has been successfully deleted."})
        else:
            logging.error(f"Image '{name}' not found.")
            raise HTTPException(status_code=404, detail=f"Image '{name}' not found.")

    except Exception as e:
        logging.error(f"An error occurred while deleting the image '{name}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the image '{name}': {str(e)}")


# @app.websocket("/api/linkedin")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()

#     try:
#         data = await websocket.receive_json()
#         dto = Item(**data)
#         for i in range(4):
#             post =  await CreatePost(dto.script, dto.link, "linkedin")
#             await websocket.send_json({"post": post})
#         await websocket.close(code=1000, reason="All posts sent")
#     except WebSocketDisconnect:
#         print("Client disconnected")
#     except Exception as e:
#         await websocket.close(code=1011, reason=f"Server error: {e}")
#         print(f"Error: {e}")

# uvicorn.run(app, host="127.0.0.1", port=8000)