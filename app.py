import streamlit as st
from datetime import datetime
import time
import os
import requests

# --- Config ---
st.set_page_config(page_title="FlutterBot", page_icon="🤖", layout="centered")

# --- Environment variable for API Key ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- Dark Mode Toggle ---
dark_mode = st.sidebar.toggle("Dark Mode", value=False)
if dark_mode:
    st.markdown("""
    <style>
    body { background-color: #111827; color: white; }
    .stTextInput>div>div>input { color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Initial Messages ---
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "id": "1",
        "text": "Hi there! I'm FlutterBot. How can I help you today?",
        "isUser": False,
        "timestamp": datetime.now().strftime("%H:%M")
    }]

# --- Function to query Groq API ---
def generate_groq_response(user_input: str) -> str:
    url = "https://api.groq.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {
                "role": "system",
                "content": "You are FlutterBot, a helpful chatbot for Flutter-related questions."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return "I'm sorry, something went wrong while talking to Groq API."

# --- Chat Header ---
st.markdown(f"""
<div style='display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #ccc; padding: 8px;'>
  <div style='display: flex; align-items: center; gap: 8px;'>
    <button style='border: none; background: none; cursor: pointer;' onclick='window.history.back()'>⬅️</button>
    <div>
      <h2 style='margin: 0;'>FlutterBot</h2>
      <p style='margin: 0; font-size: 12px; color: green;'>Online</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# --- Chat Messages ---
st.markdown("<div style='height: 400px; overflow-y: auto; display: flex; flex-direction: column;'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    bubble_color = "#3b82f6" if msg["isUser"] else "#f1f5f9"
    text_color = "white" if msg["isUser"] else "black"
    align = "flex-end" if msg["isUser"] else "flex-start"
    border_radius = "15px 15px 0 15px" if msg["isUser"] else "15px 15px 15px 0"
    st.markdown(f"""
    <div style='align-self: {align}; background: {bubble_color}; color: {text_color};
        padding: 8px 12px; border-radius: {border_radius}; margin: 4px 0; max-width: 70%;'>
        {msg["text"]}
        <div style='font-size: 10px; opacity: 0.6; text-align: right;'>{msg["timestamp"]}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Typing Indicator ---
if "typing" in st.session_state and st.session_state.typing:
    st.markdown("""
    <div style='align-self: flex-start; background: #f1f5f9; color: black; padding: 8px 12px; border-radius: 15px 15px 15px 0; margin: 4px 0; display: inline-block;'>
        <span style='animation: blink 1.4s infinite;'>.</span>
        <span style='animation: blink 1.4s infinite 0.2s;'>.</span>
        <span style='animation: blink 1.4s infinite 0.4s;'>.</span>
    </div>
    <style>
    @keyframes blink {
      0%, 100% {{ opacity: 0.1; }}
      20% {{ opacity: 1; }}
    }
    </style>
    """, unsafe_allow_html=True)

# --- Message Input ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message…", key="user_input", placeholder="Say something…")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    # Add user message
    st.session_state.messages.append({
        "id": str(int(time.time() * 1000)),
        "text": user_input.strip(),
        "isUser": True,
        "timestamp": datetime.now().strftime("%H:%M")
    })

    # Simulate bot typing
    st.session_state.typing = True
    with st.spinner("FlutterBot is typing…"):
        time.sleep(1.5)
        bot_reply = generate_groq_response(user_input)

    # Add bot response
    st.session_state.typing = False
    st.session_state.messages.append({
        "id": str(int(time.time() * 1000) + 1),
        "text": bot_reply,
        "isUser": False,
        "timestamp": datetime.now().strftime("%H:%M")
    })

# --- Auto Scroll ---
st.markdown("""
<script>
var chatContainer = window.parent.document.querySelectorAll('.element-container')[0];
if (chatContainer) {
  chatContainer.scrollTop = chatContainer.scrollHeight;
}
</script>
""", unsafe_allow_html=True)
