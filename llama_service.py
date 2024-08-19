from fastapi import HTTPException
from groq import AsyncGroq
from dotenv import load_dotenv
from shared import read_file
import os

load_dotenv()

client = AsyncGroq(
    api_key = os.getenv('GROQ_API_KEY')
)

async def CreatePost(script:str, link:str, type:str):

    stream = await client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": read_file(f"prompts/{type}.txt")
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

async def CreateTitle(script:str, type:str):

    stream = await client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": read_file(f"prompts/{type}_title.txt")
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