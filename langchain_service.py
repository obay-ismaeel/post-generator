from langchain_groq import ChatGroq
from langchain_community.document_loaders import TextLoader
from shared import read_file
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
import os

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

db = None

def initialize_database():
    global db

    if db is None:  # Check if the database is already initialized
        if os.path.isfile("chroma.sqlite3"):
            print("Loading DB...")
            db = Chroma(collection_name='chroma', persist_directory="./", embedding_function=CohereEmbeddings(model='embed-english-v3.0'))
            return


        directory_path = "./documents"

        all_documents = []

        for filename in os.listdir(directory_path):
            loader = TextLoader(f"documents/{filename}", encoding = 'UTF-8')

            print(filename)

            docs = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            
            splits = text_splitter.split_documents(docs)

            all_documents.extend(splits)

        db = Chroma.from_documents(persist_directory="./" ,documents=all_documents, embedding=CohereEmbeddings(model='embed-english-v3.0'))
        
        print("Database initialized successfully!")

def semantic_search(query:str):
    initialize_database()

    documents = db.similarity_search(query, 5)

    result = [doc.page_content for doc in documents]

    return result