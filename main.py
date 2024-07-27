from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()

client = Groq(
    api_key = os.getenv('API_KEY')
)

app = FastAPI()

class Item(BaseModel):
    script: str
    link: str

@app.post('/blog')
async def generate_linkedin(item:Item):
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "you be given a blog that contains the same content as a YouTube video.\nI want you to generate a LinkedIn post with the following constraints in mind:\nthe post contains an abstract of the video or a glimpse of its content. \nthe post serves as a port to get LinkedIn users to click the link and watch the video and to increase the reach of the LinkedIn account. \nyour response message should only contain the post, no titles, clarifications, and no notes. \nthe post should follow LinkedIn's best practices and be appealing and attractive to catch users' attention.\nuse emojis carefully.\nuse JSON format."
            },
            {
                "role": "user",
                "content": item.script
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    response_content = completion.choices[0].message.content
    
    try:
        # Try to parse the response content as JSON
        parsed_content = json.loads(response_content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from the model")

    # Return the parsed JSON content
    return parsed_content

@app.post('/linkedin')
async def generate_linkedin(item:Item):
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "you be given a blog that contains the same content as a YouTube video.\nI want you to generate a LinkedIn post with the following constraints in mind:\nthe post contains an abstract of the video or a glimpse of its content. \nthe post serves as a port to get LinkedIn users to click the link and watch the video and to increase the reach of the LinkedIn account. \nyour response message should only contain the post, no titles, clarifications, and no notes. \nthe post should follow LinkedIn's best practices and be appealing and attractive to catch users' attention.\nuse emojis carefully.\nuse JSON format."
            },
            {
                "role": "user",
                "content": item.script
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    response_content = completion.choices[0].message.content
    
    try:
        # Try to parse the response content as JSON
        parsed_content = json.loads(response_content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from the model")

    # Return the parsed JSON content
    return parsed_content

@app.post('/twitter')
async def generate_linkedin(item:Item):
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "you be given a blog that contains the same content as a YouTube video.\nI want you to generate a LinkedIn post with the following constraints in mind:\nthe post contains an abstract of the video or a glimpse of its content. \nthe post serves as a port to get LinkedIn users to click the link and watch the video and to increase the reach of the LinkedIn account. \nyour response message should only contain the post, no titles, clarifications, and no notes. \nthe post should follow LinkedIn's best practices and be appealing and attractive to catch users' attention.\nuse emojis carefully.\nuse JSON format."
            },
            {
                "role": "user",
                "content": item.script
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    response_content = completion.choices[0].message.content
    
    try:
        # Try to parse the response content as JSON
        parsed_content = json.loads(response_content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from the model")

    # Return the parsed JSON content
    return parsed_content

@app.post('/facebook')
async def generate_linkedin(item:Item):
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "you be given a blog that contains the same content as a YouTube video.\nI want you to generate a LinkedIn post with the following constraints in mind:\nthe post contains an abstract of the video or a glimpse of its content. \nthe post serves as a port to get LinkedIn users to click the link and watch the video and to increase the reach of the LinkedIn account. \nyour response message should only contain the post, no titles, clarifications, and no notes. \nthe post should follow LinkedIn's best practices and be appealing and attractive to catch users' attention.\nuse emojis carefully.\nuse JSON format."
            },
            {
                "role": "user",
                "content": item.script
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    response_content = completion.choices[0].message.content
    
    try:
        # Try to parse the response content as JSON
        parsed_content = json.loads(response_content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from the model")

    # Return the parsed JSON content
    return parsed_content