import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationalRetrievalChain

# --- KONFIGURACJA ---
DOCS_DIR = "data"
DB_DIR = "vector_db"
MODEL_NAME = "llama3"

# Upewnij się, że folder na dane istnieje
if not os.path.exists(DOCS_DIR):
    os.makedirs(DOCS_DIR)

# --- FUNKCJE RAG ---

def initialize_vector_store():
    """Wczytuje dokumenty i tworzy/ładuje bazę wektorową."""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
        # Załaduj istniejącą bazę
        return Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    else:
        # Stwórz nową bazę z dokumentów w folderze /data
        st.info("Indeksowanie dokumentów... To potrwa chwilę.")
        loader = DirectoryLoader(DOCS_DIR, glob="./*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(documents)
        
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=DB_DIR
        )
        return vector_db

def setup_rag_chain(vector_db):
    """Konfiguruje model LLM z pamięcią i dostępem do bazy wektorowej."""
    llm = ChatOllama(model=MODEL_NAME)
    
    # Pamięć rozmowy
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # Tworzenie łańcucha konwersacyjnego
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        verbose=False
    )
    return chain

# --- INTERFEJS STREAMLIT ---

st.set_page_config(page_title="Lokalny RAG", page_icon="🤖")
st.title("🤖 Twój Lokalny Asystent Dokumentów")

# Inicjalizacja stanu sesji (aby dane nie znikały po odświeżeniu)
if "vector_db" not in st.session_state:
    if not os.listdir(DOCS_DIR):
        st.warning(f"Folder '{DOCS_DIR}' jest pusty. Dodaj pliki PDF i odśwież stronę.")
        st.stop()
    st.session_state.vector_db = initialize_vector_store()

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = setup_rag_chain(st.session_state.vector_db)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Wyświetlanie historii czatu
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Obsługa pytania użytkownika
if prompt := st.chat_input("O co chcesz zapytać?"):
    # Dodaj pytanie użytkownika do historii
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generowanie odpowiedzi
    with st.chat_message("assistant"):
        with st.spinner("Myślę..."):
            response = st.session_state.rag_chain.invoke({"question": prompt})
            answer = response["answer"]
            st.markdown(answer)
            
    # Dodaj odpowiedź asystenta do historii
    st.session_state.messages.append({"role": "assistant", "content": answer})