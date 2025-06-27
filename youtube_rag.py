from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama


# take user input 
video_id = "Gfr50f6ZBvo" # only the ID, not full URL
try:
    # If you don’t care which language, this returns the “best” one
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])

    # Flatten it to plain text
    transcript = " ".join(chunk["text"] for chunk in transcript_list)
    print(transcript)

except TranscriptsDisabled:
    print("No captions available for this video.")


# Indexing: split transcript into chunks and create embeddings
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.create_documents([transcript])

len(chunks)

# Indexing (Embedding Generation and Storing in Vector Store)
embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")
# embeddings = OllamaEmbeddings(model="tinyllama1.1b")
vector_store = FAISS.from_documents(chunks, embeddings)

# print vector_store.index_to_docstore_id

# Retrieval: Create a retriever from the vector store
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
retriever.invoke('What is deepmind')


# - Augmentation: Create a prompt template for the LLM
# llm = ChatOllama(model="tinyllama:1.1b", temperature=0.2)
llm = ChatOllama(model="deepseek-r1:1.5b", temperature=0.2)

# llm = OllamaLLM(model="deepseek-r1:1.5b")

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

question          = "is the topic of nuclear fusion discussed in this video? if yes then what was discussed"
retrieved_docs    = retriever.invoke(question)

context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
# context_text

final_prompt = prompt.invoke({"context": context_text, "question": question})

# Generate the final answer using the LLM
answer = llm.invoke(final_prompt)
print(answer.content)


# Build chain
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

def format_docs(retrieved_docs):
  context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
  return context_text

parallel_chain = RunnableParallel({
    'context': retriever | RunnableLambda(format_docs),
    'question': RunnablePassthrough()
})

parallel_chain.invoke('who is Demis')

parser = StrOutputParser()
main_chain = parallel_chain | prompt | llm | parser
main_chain.invoke('Can you summarize the video')

# import streamlit as st
# from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_ollama.llms import OllamaLLM
# from langchain_ollama import OllamaEmbeddings, ChatOllama
# from langchain_core.prompts import PromptTemplate

# # Custom CSS for smooth UI
# st.markdown("""
#     <style>
#     body { background: #f7f7f9; }
#     .main { background: #fff; border-radius: 16px; box-shadow: 0 2px 16px #0001; padding: 2rem; }
#     .chat-bubble { background: #e3e8f0; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }
#     .chat-bubble.user { background: #d1e7dd; text-align: right; }
#     .chat-bubble.bot { background: #f8d7da; text-align: left; }
#     .video-box { margin-bottom: 2rem; }
#     .stTextInput>div>div>input { border-radius: 8px; }
#     </style>
# """, unsafe_allow_html=True)

# st.markdown('<div class="main">', unsafe_allow_html=True)
# st.title("🎬 YouTube RAG Q&A App")

# # Session state for chat history and vector store
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "vector_store" not in st.session_state:
#     st.session_state.vector_store = None
# if "chunks" not in st.session_state:
#     st.session_state.chunks = None

# video_id = st.text_input("Enter YouTube Video ID (e.g. Gfr50f6ZBvo):", key="video_id")
# if st.button("Load Video Transcript & Build Index"):
#     try:
#         transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
#         transcript = " ".join(chunk["text"] for chunk in transcript_list)
#         splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#         chunks = splitter.create_documents([transcript])
#         embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")
#         vector_store = FAISS.from_documents(chunks, embeddings)
#         st.session_state.vector_store = vector_store
#         st.session_state.chunks = chunks
#         st.success("Transcript loaded and indexed!")
#     except TranscriptsDisabled:
#         st.error("No captions available for this video.")
#     except Exception as e:
#         st.error(f"Error: {e}")

# if st.session_state.vector_store:
#     question = st.text_input("Ask a question about the video:", key="question")
#     if st.button("Ask"):
#         retriever = st.session_state.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
#         retrieved_docs = retriever.invoke(question)
#         context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
#         prompt = PromptTemplate(
#             template="""
#               You are a helpful assistant.
#               Answer ONLY from the provided transcript context.
#               If the context is insufficient, just say you don't know.

#               {context}
#               Question: {question}
#             """,
#             input_variables = ['context', 'question']
#         )
#         final_prompt = prompt.invoke({"context": context_text, "question": question})
#         llm = ChatOllama(model="deepseek-r1:1.5b", temperature=0.2)
#         answer = llm.invoke(final_prompt)
#         st.session_state.chat_history.append({"question": question, "answer": answer.content})

# # Display chat history
# for chat in st.session_state.chat_history:
#     st.markdown(f'<div class="chat-bubble user"><b>You:</b> {chat["question"]}</div>', unsafe_allow_html=True)
#     st.markdown(f'<div class="chat-bubble bot"><b>Bot:</b> {chat["answer"]}</div>', unsafe_allow_html=True)

# st.markdown('</div>', unsafe_allow_html=True)
