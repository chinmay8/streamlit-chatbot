# 🤖 AI Chat Assistant (Streamlit + OpenRouter)

A sleek, dark-themed AI chat application built with **Streamlit**. This app mimics a modern chat interface, integrates with the **OpenRouter API** (specifically the `openai/gpt-oss-120b` model), and offers robust local chat management with conversation summarization capabilities.

## ✨ Features

- **Dark Mode UI:** A custom-styled, dark-themed interface inspired by modern chat apps.
- **OpenRouter Integration:** Powered by the `openai/gpt-oss-120b` model via OpenRouter.
- **Persistent Chat History:** Automatically saves all conversations to local JSON files.
- **Chat Management:**
- Create new chats.
- Switch between historical chats instantly.
- Delete individual chats.
- Clear current chat history.

- **Smart Summarization:** Includes an expander to generate and view a 3-4 bullet point summary of the current conversation using the AI model.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Python 3.8 or higher**: [Download Python](https://www.python.org/downloads/)
- **A Code Editor**: VS Code is recommended.
- **OpenRouter API Key**: Get your key from [openrouter.ai](https://openrouter.ai/).

## 🚀 Installation & Setup

Follow these steps to get the app running locally.

### 1. Clone the Repository

(If you haven't already, download this code to a folder)

```bash
git clone <your-repo-url>
cd <your-project-folder>

```

### 2. Create a Virtual Environment (Recommended)

It is best practice to run Python apps in a virtual environment to avoid conflicts.

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate

```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

Install the required Python libraries (Streamlit and OpenAI).

```bash
pip install streamlit openai

```

## 🔑 Configuration

You must configure your API key for the app to work. Streamlit uses a secure secrets management system.

1. In your project root directory, create a folder named `.streamlit`.
2. Inside that folder, create a file named `secrets.toml`.
3. Add your API key to the file:

**File Path:** `.streamlit/secrets.toml`

```toml
OPENROUTER_API_KEY = "sk-or-your-actual-api-key-here"

```

## 🏃‍♂️ How to Run

Once installed and configured, run the application with the following command:

```bash
streamlit run app.py

```

The application will automatically open in your default web browser at `http://localhost:8501`.

## 📂 Project Structure

```text
my_chatbot/
├── .streamlit/
│   └── secrets.toml      # Your API Key (Do not share this file!)
├── chats/                # Automatically created folder for chat history JSONs
├── app.py                # Main application code
└── README.md             # This documentation

```

## 📝 Usage Guide

1. **Start a Chat:** Type your question in the input bar at the bottom.
2. **New Conversation:** Click **"+ New Chat"** in the sidebar to start fresh.
3. **Summarize:** Click the **"📝 Conversation Summary"** expander at the top and hit the "Generate" button to get a quick recap of your discussion.
4. **Manage History:** Select old chats from the sidebar list or click the **Trash Icon (🗑️)** to delete them permanently.

---

_Built with [Streamlit](https://streamlit.io)._
