import streamlit as st
import requests
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Document Q&A Platform",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Inject CSS Animations and Custom Micro-Interactions
st.markdown("""
    <style>
    /* 1. Global Page Smooth Fade-In */
    @keyframes pageLoad {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stApp {
        animation: pageLoad 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
    }
    
    /* 2. Chat Message Slide-Up Animation */
    @keyframes msgSlideUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    [data-testid="stChatMessage"] {
        animation: msgSlideUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) both;
    }
    
    /* 3. Document Sidebar Cards UI */
    @keyframes filePop {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    .file-card {
        background: linear-gradient(135deg, rgba(74, 144, 226, 0.08) 0%, rgba(74, 144, 226, 0.03) 100%);
        border: 1px solid rgba(74, 144, 226, 0.2);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: filePop 0.3s ease-out both;
        transition: all 0.2s ease;
    }
    .file-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(74, 144, 226, 0.15);
        border-color: rgba(74, 144, 226, 0.4);
    }
    
    /* 4. Interactive Hover Scaling for Action Buttons */
    .stButton>button {
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border-radius: 8px !important;
    }
    .stButton>button:hover {
        transform: translateY(-1px) scale(1.01) !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08) !important;
    }
    .stButton>button:active {
        transform: translateY(1px) scale(0.99) !important;
    }
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

def display_source_expander(sources):
    """Helper component to cleanly render source documents with clean formatting"""
    with st.expander("🔍 View Referenced Context Sources", expanded=False):
        for index, source in enumerate(sources):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"📁 **File:** `{source['file']}`")
            with col2:
                st.markdown(f"📖 **Page:** `{source['page']}`")
            
            if "chunk" in source and source["chunk"]:
                st.caption("Extracted Match Excerpt:")
                st.code(source["chunk"][:400], language="text")
            
            if index < len(sources) - 1:
                st.divider()

with st.sidebar:
    st.title("📂 Control Panel")
    st.caption("Manage document.")
    st.divider()

    st.subheader("📤 Document Uploader")
    uploaded_files = st.file_uploader(
        "Upload PDF Files",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    if st.button("⚡ Process & Index Files", use_container_width=True, type="primary"):
        if uploaded_files:
            progress_bar = st.progress(0)
            status_message = st.empty()

            for index, file in enumerate(uploaded_files):
                status_message.caption(f"Syncing: *{file.name}*...")               
                try:
                    response = requests.post(
                        f"{API_URL}/upload",
                        files={
                            "file": (
                                file.name,
                                file,
                                "application/pdf"
                            )
                        }
                    )
                    if response.status_code == 200:
                        if file.name not in st.session_state.uploaded_files:
                            st.session_state.uploaded_files.append(file.name)
                    else:
                        st.error(f"Upload Failure ({file.name}): {response.text}")
                except Exception as err:
                    st.error(f"Network Connection Exception: {err}")

                
                progress_bar.progress((index + 1) / len(uploaded_files))
            
            
            status_message.empty()
            progress_bar.empty()
            st.toast("Knowledge base synced successfully!", icon="🚀")
        else:
            st.warning("Please stage files within the dropzone first.")
    st.divider()
    st.subheader("📚 Active Knowledge Base")
    if st.session_state.uploaded_files:
        # Wrap in container to retain unified structural sizing
        with st.container():
            for file in st.session_state.uploaded_files:
                st.markdown(f"""
                    <div class="file-card">
                        <span>📄</span>
                        <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{file}</span>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No documents are actively indexed to memory.")
    st.divider()
    if st.button("🗑️ Reset Chat History", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.rerun()


st.title("📄 AI Document Q&A Platform")
st.caption("Interact with your uploaded documents using advanced retrieval-augmented generation (RAG) techniques.")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "sources" in message and message["sources"]:
            display_source_expander(message["sources"])

question = st.chat_input("Query anything contained within your documents...")

if question:
    
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing data vector contexts..."):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": question}
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data["sources"]
                    
                    st.markdown(answer)
                    if sources:
                        display_source_expander(sources)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                else:
                    st.error(f"Backend Server Failure Error Code {response.status_code}: {response.text}")
            except Exception as conn_err:
                st.error(f"Failed to communicate with API server: {conn_err}")