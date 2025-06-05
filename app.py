import streamlit as st
import time
from groq import Groq
import os

# Initialize Grok client
client = Groq(api_key=os.getenv("GROK_API_KEY"))

# Streamlit app configuration
st.set_page_config(page_title="FlutterBot - Grok Chat", layout="centered")

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        max-width: 600px;
        margin: 0 auto;
    }
    .chat-container {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        height: 600px;
        display: flex;
        flex-direction: column;
    }
    .chat-header {
        padding: 16px;
        border-bottom: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #f8fafc;
    }
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
        background-color: #f1f5f9;
    }
    .message {
        margin-bottom: 16px;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        justify-content: flex-end;
    }
    .bot-message {
        justify-content: flex-start;
    }
    .message-bubble {
        padding: 8px 16px;
        border-radius: 16px;
        max-width: 85%;
    }
    .user-bubble {
        background-color: #2563eb;
        color: white;
        border-bottom-right-radius: 4px;
    }
    .bot-bubble {
        background-color: #e2e8f0;
        color: #1e293b;
        border-bottom-left-radius: 4px;
    }
    .timestamp {
        font-size: 12px;
        color: #64748b;
        margin-top: 4px;
        padding: 0 4px;
    }
    .typing-indicator {
        display: flex;
        gap: 4px;
        padding: 12px 16px;
        background-color: #e2e8f0;
        border-radius: 16px;
        width: 64px;
        border-bottom-left-radius: 4px;
    }
    .dot {
        width: 8px;
        height: 8px;
        background-color: #94a3b8;
        border-radius: 50%;
        animation: blink 1.4s infinite both;
    }
    .dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    .dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    @keyframes blink {
        0% { opacity: 0.1; }
        20% { opacity: 1; }
        100% { opacity: 0.1; }
    }
    .input-container {
        padding: 16px;
        border-top: 1px solid #e2e8f0;
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "id": "1",
            "text": "Hi there! I'm FlutterBot, powered by Grok. How can I help you today?",
            "is_user": False,
            "timestamp": time.strftime("%H:%M")
        }
    ]
if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

# Function to get Grok response
def get_grok_response(user_input):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are FlutterBot, a helpful chatbot inspired by Flutter and powered by Grok. Assist users with a friendly tone."},
                {"role": "user", "content": user_input}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=1024
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Chat header
st.markdown("""
<div class='chat-container'>
    <div class='chat-header'>
        <div style='display: flex; align-items: center; gap: 12px;'>
            <h2 style='margin: 0; font-size: 18px; font-weight: 500;'>FlutterBot</h2>
            <p style='margin: 0; font-size: 12px; color: #16a34a;'>Online</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Chat messages
st.markdown("<div class='chat-messages'>", unsafe_allow_html=True)
for message in st.session_state.messages:
    direction = "user-message" if message["is_user"] else "bot-message"
    bubble_style = "user-bubble" if message["is_user"] else "bot-bubble"
    st.markdown(
        f"""
        <div class='message {direction}'>
            <div style='display: flex; flex-direction: column; max-width: 85%;'>
                <div class='message-bubble {bubble_style}'>
                    {message['text']}
                </div>
                <span class='timestamp'>
                    {message['timestamp']}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Typing indicator
if st.session_state.is_typing:
    st.markdown("""
    <div class='message bot-message'>
        <div class='typing-indicator'>
            <span class='dot'></span>
            <span class='dot'></span>
            <span class='dot'></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Message input
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
user_input = st.text_input("Type your message...", key="user_input", on_change=None)
if st.button("Send"):
    if user_input:
        # Add user message
        st.session_state.messages.append({
            "id": str(time.time()),
            "text": user_input,
            "is_user": True,
            "timestamp": time.strftime("%H:%M")
        })
        
        # Show typing indicator
        st.session_state.is_typing = True
        st.rerun()
        
        # Get and add bot response
        bot_response = get_grok_response(user_input)
        st.session_state.is_typing = False
        st.session_state.messages.append({
            "id": str(time.time() + 1),
            "text": bot_response,
            "is_user": False,
            "timestamp": time.strftime("%H:%M")
        })
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Note about API key
st.markdown("""
<div style='margin-top: 16px; font-size: 12px; color: #64748b;'>
    Note: Ensure GROK_API_KEY is set in your environment variables. Get your key from https://x.ai/api
</div>
""", unsafe_allow_html=True)
