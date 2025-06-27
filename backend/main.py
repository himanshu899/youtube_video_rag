from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import PromptTemplate

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only, restrict in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_stores = {}

class TranscriptRequest(BaseModel):
    video_id: str

class AskRequest(BaseModel):
    video_id: str
    question: str

@app.post("/transcript")
async def get_transcript(req: TranscriptRequest):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(req.video_id, languages=["en"])
        transcript = " ".join(chunk["text"] for chunk in transcript_list)
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.create_documents([transcript])
        embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")
        vector_store = FAISS.from_documents(chunks, embeddings)
        vector_stores[req.video_id] = vector_store
        return {"success": True, "message": "Transcript loaded and indexed."}
    except TranscriptsDisabled:
        return {"success": False, "message": "No captions available for this video."}
    except Exception as e:
        return {"success": False, "message": str(e)}

@app.post("/ask")
async def ask_question(req: AskRequest):
    if req.video_id not in vector_stores:
        return {"success": False, "message": "Transcript not loaded for this video."}
    vector_store = vector_stores[req.video_id]
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    retrieved_docs = retriever.invoke(req.question)
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
    prompt = PromptTemplate(
        template="""
          You are a helpful assistant.
          Answer ONLY from the provided transcript context.
          If the context is insufficient, just say you don't know.

          {context}
          Question: {question}
        """,
        input_variables = ['context', 'question']
    )
    final_prompt = prompt.invoke({"context": context_text, "question": req.question})
    llm = ChatOllama(model="deepseek-r1:1.5b", temperature=0.2)
    answer = llm.invoke(final_prompt)
    return {"success": True, "answer": answer.content}