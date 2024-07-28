from fastapi import HTTPException
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key = os.getenv('API_KEY')
)

async def CreatePost(script:str, link:str, type:str):
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": read_file(f"rules/{type}.txt")
            },
            {
                "role": "user",
                "content": script
            }
        ],
        temperature=1,
        max_tokens=4096,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    response_content = completion.choices[0].message.content
    
    try:
        # Try to parse the response content as JSON
        return json.loads(response_content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from the model")

def read_file(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file at path {file_path} was not found."
    except IOError as e:
        return f"Error reading file at path {file_path}: {e}"