from typing import Literal
from langchain_groq import ChatGroq
from langchain_community.document_loaders import TextLoader
from dtos import Item, QueryDto
from shared import read_file, get_pov_text
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

async def generate_post(item:QueryDto):
    llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=1,
    max_tokens=6660,
    timeout=None,
    max_retries=2,
    stop_sequences=[],
    )    

    messages = [
        ("system", await create_prompt(item)),
        ("human", f"script:{item.script}, link:{item.link}"),
    ]
    
    ai_msg = llm.invoke(messages)
    
    return ai_msg.content

async def create_prompt(item:QueryDto):
    base_prompt = read_file(f"prompts/{item.options.platform}.txt")

    dynamic_prompt = base_prompt

    if item.options.post_format != 'auto':
        dynamic_prompt += f"\nPost format: generate a {item.options.post_format}."
    
    if item.options.point_of_view != 'auto':
        # dynamic_prompt += f"\nWrite from a {get_pov_text(item.options.point_of_view)} point of view."
        dynamic_prompt += f"\nWrite from a {item.options.point_of_view} point of view."
    
    if item.options.use_emojis:
        dynamic_prompt += "\nFeel free to use emojis Wisely.."
    else:
        dynamic_prompt += "\nDo not use emojis."

    if item.options.additional_prompt:
        dynamic_prompt += f"\nAdditional user instructions: {item.options.additional_prompt}"

    if item.options.word_count:
        dynamic_prompt += f"\nTarget word count: around {item.options.word_count} words."

    topic=' ' + str(item.options.post_format) if item.options.post_format != 'auto' else ''
    
    db_query = f"writing an engaging {item.options.platform}{topic} post"

    retrieved_data= semantic_search(db_query)

    dynamic_prompt += f"\nUse these information if you found them useful: {retrieved_data}"

    return dynamic_prompt

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

db = None

def initialize_database():
    global db

    if db is None:  # Check if the database is already initialized
        directory_path = "./documents"

        all_documents = []

        for filename in os.listdir(directory_path):
            loader = TextLoader(f"documents/{filename}", encoding = 'UTF-8')

            print(filename)

            docs = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
            
            splits = text_splitter.split_documents(docs)

            all_documents.extend(splits)

        db = Chroma.from_documents(persist_directory="./db/" ,documents=all_documents, embedding=CohereEmbeddings(model='embed-english-v3.0', client='Obay', async_client='Eyas'))
        
        print("Database initialized successfully!")

def semantic_search(query:str):
    global db

    if os.path.isfile("./db/chroma.sqlite3"):
        print("Loading DB...")
        db = Chroma(persist_directory="./db", embedding_function=CohereEmbeddings(model='embed-english-v3.0', client=None, async_client=None))
    else:
        initialize_database()

    if db is None:
        raise ValueError("Database not initialized")
    
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 6})

    documents = retriever.invoke(query)

    result = [doc.page_content for doc in documents]

    return result