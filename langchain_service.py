from langchain_groq import ChatGroq
from shared import read_file

async def CreatePostLangchain(script:str, link:str, type:str):

    llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=1,
    max_tokens=6660,
    timeout=None,
    max_retries=2,
    stop_sequences=[],
    )

    messages = [
        ("system", read_file(f"prompts/{type}.txt"),),
        ("human", script),
    ]
    
    ai_msg = llm.invoke(messages)
    
    return ai_msg.content
