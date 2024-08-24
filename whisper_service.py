# import whisper
# from fastapi import File, UploadFile
# from fastapi.responses import JSONResponse
# import os
# from pathlib import Path

# async def get_transcribe(file: UploadFile = File(...)) -> JSONResponse:

#     model: whisper.Whisper = whisper.load_model("base")

#     # Get the current working directory
#     current_directory: Path = Path.cwd()
#     # # Get the current working directory
#     # current_directory = os.getcwd()

#     # Save the uploaded file to disk
#     file_path: str = f"{current_directory}{file.filename}"
#     with open(file_path, "wb") as f:
#         f.write(await file.read())

#     # Transcribe the audio using Whisper
#     result: dict[str , str | list ] = model.transcribe(file_path)

#     # Remove the temporary file
#     os.remove(file_path)

#     # Extract the text from the transcription result
#     transcription_text: str | list = result.get("text", "")

#     # Return the transcription text as a JSON response
#     return JSONResponse(content={"text": transcription_text})