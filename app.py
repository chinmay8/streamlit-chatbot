import streamlit as st
import os
import json
import uuid
from datetime import datetime
from openai import OpenAI

# --- Configuration ---
CHAT_FOLDER = "chats"
MODEL_NAME = "openai/gpt-oss-120b"
PAGE_TITLE = "AI Chat Assistant"
PAGE_ICON = "🤖"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
    /* Global Background */
    .stApp { background-color: #121212; color: #FFFFFF; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #1E1E1E; }
    
    /* "New Chat" Button Styling */
    div.stButton > button.new-chat-btn {
        background-color: #FF4B4B; color: white; border: none; width: 100%;
        border-radius: 5px; font-weight: bold;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #2E2E2E;
        color: white;
        border-radius: 5px;
    }
    
    /* Chat Messages */
    .stChatMessage { background-color: transparent; }
    .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# --- File Operations ---

def ensure_chat_folder():
    if not os.path.exists(CHAT_FOLDER):
        os.makedirs(CHAT_FOLDER)

def save_chat_history(chat_id, messages, title="New Chat", summary=None):
    ensure_chat_folder()
    filepath = os.path.join(CHAT_FOLDER, f"{chat_id}.json")
    
    # Auto-generate title from first message if needed
    if title == "New Chat" and len(messages) > 0:
        for msg in messages:
            if msg["role"] == "user":
                title = msg["content"][:30] + "..."
                break
                
    data = {
        "id": chat_id,
        "title": title,
        "timestamp": datetime.now().isoformat(),
        "messages": messages,
        "summary": summary  # Saved field for summary
    }
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    return title

def get_all_chats():
    ensure_chat_folder()
    chats = []
    for filename in os.listdir(CHAT_FOLDER):
        if filename.endswith(".json"):
            filepath = os.path.join(CHAT_FOLDER, filename)
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                    chats.append(data)
            except:
                continue
    chats.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return chats

def delete_chat_file(chat_id):
    filepath = os.path.join(CHAT_FOLDER, f"{chat_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)

# --- Session State Initialization ---

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.chat_title = "New Chat"
    st.session_state.chat_summary = ""  # New state for summary

# --- OpenRouter Client ---
try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"],
        default_headers={"HTTP-Referer": "http://localhost:8501", "X-Title": "Streamlit Chat App"}
    )
except Exception as e:
    st.error(f"Error initializing API Client. Check secrets.toml. {e}")
    st.stop()

# --- Helper Function: Generate Summary ---
def generate_summary_text(messages):
    if not messages:
        return "No conversation to summarize."
    
    # Create a simplified text block of the conversation for the summarizer
    conversation_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    
    prompt = f"""
    Please provide a concise summary (3-4 bullet points) of the following conversation.
    Focus on the main topics discussed and any conclusions reached.
    
    Conversation:
    {conversation_text}
    """
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {e}"

# --- Sidebar Logic ---

with st.sidebar:
    st.title("💬 Conversations")
    
    if st.button("＋ New Chat", type="primary", use_container_width=True):
        st.session_state.current_chat_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.chat_title = "New Chat"
        st.session_state.chat_summary = ""
        st.rerun()

    st.markdown("### Chat History")
    chats = get_all_chats()
    
    for chat in chats:
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            btn_type = "primary" if chat["id"] == st.session_state.current_chat_id else "secondary"
            if st.button(chat["title"], key=f"sel_{chat['id']}", type=btn_type, use_container_width=True):
                st.session_state.current_chat_id = chat["id"]
                st.session_state.messages = chat["messages"]
                st.session_state.chat_title = chat["title"]
                st.session_state.chat_summary = chat.get("summary", "") # Load summary if exists
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"del_{chat['id']}"):
                delete_chat_file(chat["id"])
                if chat["id"] == st.session_state.current_chat_id:
                    st.session_state.current_chat_id = str(uuid.uuid4())
                    st.session_state.messages = []
                    st.session_state.chat_title = "New Chat"
                    st.session_state.chat_summary = ""
                st.rerun()

    st.divider()
    if st.button("Clear Current Chat Data", type="secondary"):
        st.session_state.messages = []
        st.session_state.chat_summary = ""
        save_chat_history(st.session_state.current_chat_id, [], title=st.session_state.chat_title, summary="")
        st.rerun()

# --- Main Interface ---

st.title(f"🙋🏻‍♂️ {st.session_state.chat_title}")

# --- NEW: Summary Expander ---
with st.expander("📝 Conversation Summary", expanded=False):
    # Container to hold the summary text
    summary_container = st.empty()
    
    # If summary exists in state, display it
    if st.session_state.chat_summary:
        summary_container.markdown(st.session_state.chat_summary)
    else:
        summary_container.info("No summary generated yet.")
    
    # Button to generate/update summary
    if st.button("✨ Generate / Update Summary"):
        if not st.session_state.messages:
            st.warning("Start a conversation first!")
        else:
            with st.spinner("Analyzing conversation..."):
                new_summary = generate_summary_text(st.session_state.messages)
                st.session_state.chat_summary = new_summary
                summary_container.markdown(new_summary)
                # Save the new summary to file immediately
                save_chat_history(
                    st.session_state.current_chat_id, 
                    st.session_state.messages, 
                    st.session_state.chat_title,
                    st.session_state.chat_summary
                )

# --- Chat Stream ---
if st.session_state.chat_title == "New Chat" and not st.session_state.messages:
    st.markdown("#### Hey, I am your chatbot assistant. How can I help you today?")

for message in st.session_state.messages:
    avatar = "🧑🏻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    with st.chat_message("user", avatar="🧑🏻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {e}")
            full_response = "Error connecting to API."
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # Save messages + keep existing summary
    save_chat_history(
        st.session_state.current_chat_id, 
        st.session_state.messages, 
        st.session_state.chat_title,
        st.session_state.chat_summary
    )
    
    # If it was the first message, update title
    if st.session_state.chat_title == "New Chat":
        st.rerun()