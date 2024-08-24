from typing import Literal
from langchain_groq import ChatGroq
from langchain_community.document_loaders import TextLoader
from dtos import Item
from shared import read_file
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
import os
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

client = AsyncGroq(
    api_key = os.getenv('GROQ_API_KEY')
)

async def generate_post(item:Item):
    llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=1,
    max_tokens=6660,
    timeout=None,
    max_retries=2,
    stop_sequences=[],
    )    

    messages = [
        ("system", read_file(f"prompts/{item.platform}.txt"),),
        ("human", item.script),
    ]
    
    ai_msg = llm.invoke(messages)
    
    return ai_msg.content

async def generate_title(script:str, type:Literal['blog', 'youtube']):
    llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=1,
    max_tokens=5000,
    timeout=None,
    max_retries=2,
    stop_sequences=[],
    )    

    messages = [
        ("system", read_file(f"prompts/{type}_title.txt"),),
        ("human", script),
    ]
    
    ai_msg = llm.invoke(messages)
    
    return ai_msg.content


def initialize_database():
    global db

    if db is None:  # Check if the database is already initialized
        if os.path.isfile("chroma.sqlite3"):
            print("Loading DB...")
            db = Chroma(collection_name='chroma', persist_directory="./", embedding_function=CohereEmbeddings(model='embed-english-v3.0', client=None, async_client=None))
            return

        directory_path = "./documents"

        all_documents = []

        for filename in os.listdir(directory_path):
            loader = TextLoader(f"documents/{filename}", encoding = 'UTF-8')

            print(filename)

            docs = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
            
            splits = text_splitter.split_documents(docs)

            all_documents.extend(splits)

        db = Chroma.from_documents(persist_directory="./db/" ,documents=all_documents, embedding=CohereEmbeddings(model='embed-english-v3.0', client='Obay', async_client='Eyas'))
        
        print("Database initialized successfully!")

def semantic_search(query:str):
    initialize_database()
    if db is None:
        raise ValueError("Database not initialized")

    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 6})

    documents = retriever.invoke(query)

    result = [doc.page_content for doc in documents]

    return result