from fastapi import HTTPException
from groq import AsyncGroq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = AsyncGroq(
    api_key = os.getenv('API_KEY')
)

async def CreatePost(script:str, link:str, type:str):

    stream = await client.chat.completions.create(
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
        max_tokens=6660,
        top_p=1,
        stream=True,
        stop=None,
    )

    response = ""
    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content

    return response

async def CreateTitle(script:str):

    stream = await client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": read_file(f"rules/title.txt")
            },
            {
                "role": "user",
                "content": script
            }
        ],
        temperature=1,
        max_tokens=6660,
        top_p=1,
        stream=True,
        stop=None,
    )

    response = ""
    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content

    return response

def read_file(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file at path {file_path} was not found."
    except IOError as e:
        return f"Error reading file at path {file_path}: {e}"