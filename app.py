import streamlit as st
import os
from core import DocumentLoader, Chunker, Retriever
from core.generator import Generator
import config

# Page config
st.set_page_config(page_title="RAGverse", page_icon="🤖", layout="wide")

# Title and description
st.title("RAGverse")
st.markdown("Chat with your documents")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "retriever" not in st.session_state:
    st.session_state.retriever = Retriever()
    if st.session_state.retriever.load():
        st.toast("Loaded existing vector store", icon="✅")

if "generator" not in st.session_state:
    try:
        st.session_state.generator = Generator()
    except Exception as e:
        st.error(f"Failed to initialize Gemini: {e}")

# Sidebar
with st.sidebar:
    st.header("**Document Management**")
    
    # File Uploader
    uploaded_files = st.file_uploader(
        "Upload Documents", 
        type=["txt", "pdf"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for uploaded_file in uploaoneded_files:
            # Save file
            file_path = os.path.join(config.DATA_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded {len(uploaded_files)} files!")

    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Index Docs"):
            with st.spinner("Indexing..."):
                # Load
                loader = DocumentLoader(config.DATA_DIR)
                documents = loader.load_documents()
                
                if documents:
                    # Chunk
                    chunker = Chunker()
                    chunks = chunker.chunk_documents(documents)
                    
                    # Index
                    st.session_state.retriever.vector_store.clear()
                    st.session_state.retriever.index_documents(chunks)
                    st.session_state.retriever.save()
                    
                    st.success(f"Indexed {len(documents)} docs!")
                else:
                    st.warning("No docs found.")

    with col2:
        if st.button("🗑️ Clear All"):
            # Delete files
            if os.path.exists(config.DATA_DIR):
                for file in os.listdir(config.DATA_DIR):
                    os.remove(os.path.join(config.DATA_DIR, file))
            
            # Clear index
            st.session_state.retriever.vector_store.clear()
            st.session_state.retriever.save()
            st.success("Cleared all!")

    st.divider()
    st.markdown("### Settings")
    st.caption(f"Embedding: {config.EMBEDDING_MODEL}")
    st.caption(f"Generation: {config.GENERATION_MODEL}")

# Chat Interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Retrieve
        results = st.session_state.retriever.retrieve(prompt, top_k=3)
        
        if results:
            # Generate with Gemini
            if "generator" in st.session_state:
                full_response = st.session_state.generator.generate_response(prompt, results)
                message_placeholder.markdown(full_response)
                
                # Show sources in expander
                with st.expander("View Sources"):
                    for i, result in enumerate(results, 1):
                        st.markdown(f"**Source {i}:** {result['source']} (Score: {1/(1+result['distance']):.4f})")
                        st.caption(result['content'])
            else:
                full_response = "Gemini is not configured. Please check your API key."
                message_placeholder.error(full_response)
        else:
            full_response = "I couldn't find any relevant information in the documents."
            message_placeholder.markdown(full_response)
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
