from dotenv import load_dotenv
import streamlit as st
import requests

# =========================
# CONFIG
# =========================
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
st.set_page_config(page_title="AI Assistant", layout="wide")

st.title("🤖 AI Chat Assistant")

# =========================
# SIDEBAR (Controls)
# =========================
st.sidebar.header("⚙️ Settings")

model = st.sidebar.selectbox( 
    "Choose Model",
    [
        
        "meta-llama/llama-3-8b-instruct",
        "anthropic/claude-3-haiku"
    ]
)

mode = st.sidebar.selectbox(
    "Choose Mode",
    ["General", "Code", "Study"]
)

# System prompts for agent-like behavior
system_prompts = {
    "General": "You are a helpful AI assistant.",
    "Code": "You are an expert programmer. Provide clean, efficient, and well-explained code.",
    "Study": "Explain concepts in a simple, clear, and structured way like a teacher."
}

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompts[mode]}
    ]

# Reset chat when mode changes
if st.session_state.messages[0]["content"] != system_prompts[mode]:
    st.session_state.messages = [
        {"role": "system", "content": system_prompts[mode]}
    ]


if len(st.session_state.messages) <= 1:
    st.markdown("### 👋 Welcome!")
    st.write("Ask anything and get instant AI responses.")

    st.write("1. Select model from sidebar")
    st.write("2. Choose mode (General / Code / Study)")
    st.write("3. Ask your question below 👇")

    st.markdown("---")


# =========================
# DISPLAY CHAT HISTORY
# =========================
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# =========================
# USER INPUT
# =========================
user_input = st.chat_input("Ask something...")

if user_input:
    # Add user message
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # API Call
    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": st.session_state.messages
                }
            )

            result = response.json()

            # Debug (optional)
            # st.write(result)

            reply = result["choices"][0]["message"]["content"]

        except Exception as e:
            reply = f"Error: {str(e)}"

    # Show assistant reply
    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
