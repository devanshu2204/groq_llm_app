import streamlit as st
import time
from groq import Groq

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Define message structure
class Message:
    def __init__(self, id: str, text: str, is_user: bool, timestamp: float):
        self.id = id
        self.text = text
        self.is_user = is_user
        self.timestamp = timestamp

# Initial bot message
INITIAL_MESSAGES = [
    Message(
        id="1",
        text="Hi there! I'm FlutterBot, now powered by Groq. How can I help you today?",
        is_user=False,
        timestamp=time.time() - 60
    )
]

# Streamlit app setup
st.set_page_config(page_title="FlutterBot Chat", layout="centered")
st.title("FlutterBot Chat")

# Dark mode toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode, key="dark_mode_toggle")
st.session_state.dark_mode = dark_mode

# Custom CSS for styling with dark mode support
st.markdown(f"""
<style>
    .stApp {{
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
    }}
    .chat-container {{
        border: 1px solid {'#4b5563' if dark_mode else '#e2e8f0'};
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        background-color: {'#1f2937' if dark_mode else '#ffffff'};
        height: 600px;
        display: flex;
        flex-direction: column;
    }}
    .chat-header {{
        padding: 0.75rem;
        border-bottom: 1px solid {'#4b5563' if dark_mode else '#e2e8f0'};
        position: sticky;
        top: 0;
        z-index: 10;
        background-color: {'#1f2937' if dark_mode else '#ffffff'};
        color: {'#ffffff' if dark_mode else '#000000'};
    }}
    .message-container {{
        flex: 1;
        overflow-y: auto;
        padding: 1rem;
        background-color: {'#111827' if dark_mode else '#f9fafb'};
    }}
    .user-message {{
        background-color: {'#2563eb' if dark_mode else '#1e40af'};
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 1rem;
        border-bottom-right-radius: 0.25rem;
        max-width: 85%;
        align-self: flex-end;
        margin-bottom: 1rem;
    }}
    .bot-message {{
        background-color: {'#374151' if dark_mode else '#e5e7eb'};
        color: {'#ffffff' if dark_mode else '#1f2937'};
        padding: 0.5rem 1rem;
        border-radius: 1rem;
        border-bottom-left-radius: 0.25rem;
        max-width: 85%;
        align-self: flex-start;
        margin-bottom: 1rem;
    }}
    .timestamp {{
        font-size: 0.75rem;
        color: {'#9ca3af' if dark_mode else '#6b7280'};
        margin-top: 0.25rem;
        padding: 0 0.25rem;
    }}
    .input-container {{
        padding: 1rem;
        border-top: 1px solid {'#4b5563' if dark_mode else '#e2e8f0'};
        background-color: {'#1f2937' if dark_mode else '#ffffff'};
    }}
    .typing-indicator {{
        display: flex;
        gap: 0.25rem;
        padding: 0.75rem 1rem;
        background-color: {'#374151' if dark_mode else '#e5e7eb'};
        border-radius: 1rem;
        border-bottom-left-radius: 0.25rem;
        width: 4rem;
        align-self: flex-start;
    }}
    .typing-dot {{
        width: 0.5rem;
        height: 0.5rem;
        background-color: {'#9ca3af' if dark_mode else '#6b7280'};
        border-radius: 50%;
        opacity: 0.6;
        animation: blink 1.4s infinite both;
    }}
    .typing-dot:nth-child(2) {{
        animation-delay: 0.2s;
    }}
    .typing-dot:nth-child(3) {{
        animation-delay: 0.4s;
    }}
    @keyframes blink {{
        0% {{ opacity: 0.1; }}
        20% {{ opacity: 1; }}
        100% {{ opacity: 0.1; }}
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state for messages and typing indicator
if "messages" not in st.session_state:
    st.session_state.messages = INITIAL_MESSAGES
if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

# Function to get Groq response with chat history
def get_groq_response(user_input: str) -> str:
    try:
        # Build message history
        messages = [
            {"role": "system", "content": "You are FlutterBot, a helpful chatbot inspired by Flutter, powered by Groq. Assist users with questions about Flutter, UI design, or general queries."}
        ]
        # Add previous messages for context (limit to last 5 to avoid token overflow)
        for msg in st.session_state.messages[-5:]:
            role = "user" if msg.is_user else "assistant"
            messages.append({"role": role, "content": msg.text})
        messages.append({"role": "user", "content": user_input})

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=500
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Function to handle message submission
def handle_send_message(text: str):
    if text.strip():
        # Add user message
        user_message = Message(
            id=str(time.time()),
            text=text,
            is_user=True,
            timestamp=time.time()
        )
        st.session_state.messages.append(user_message)

        # Show typing indicator
        st.session_state.is_typing = True

        # Get bot response
        bot_response = get_groq_response(text)

        # Add bot message
        bot_message = Message(
            id=str(time.time() + 1),
            text=bot_response,
            is_user=False,
            timestamp=time.time()
        )
        st.session_state.messages.append(bot_message)

        # Hide typing indicator
        st.session_state.is_typing = False

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Chat header with Back button
st.markdown(f"""
<div class="chat-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <button onclick="history.back()" style="border: none; background: none; cursor: pointer; color: {'#ffffff' if dark_mode else '#000000'}; font-size: 1.2rem;">⬅️</button>
            <h2 style="font-weight: 500;">FlutterBot</h2>
            <p style="font-size: 0.75rem; color: #16a34a;">Online</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Message display area
st.markdown('<div class="message-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    time_str = time.strftime("%I:%M %p", time.localtime(message.timestamp))
    if message.is_user:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; width: 100%;">
            <div style="display: flex; flex-direction: column; align-items: flex-end; max-width: 85%;">
                <div class="user-message">{message.text}</div>
                <span class="timestamp">{time_str}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; width: 100%;">
            <div style="display: flex; flex-direction: column; align-items: flex-start; max-width: 85%;">
                <div class="bot-message">{message.text}</div>
                <span class="timestamp">{time_str}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Typing indicator
if st.session_state.is_typing:
    st.markdown("""
    <div class="typing-indicator">
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Message input area with form to reduce reruns
st.markdown('<div class="input-container">', unsafe_allow_html=True)
with st.form(key="message_form", clear_on_submit=True):
    user_input = st.text_input("Type your message...", key="user_input")
    submit_button = st.form_submit_button("Send")
    if submit_button and user_input.strip():
        handle_send_message(user_input)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Auto-scroll to bottom and enable Enter key submission
st.markdown("""
<script>
    const messageContainer = document.querySelector('.message-container');
    if (messageContainer) {
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }
    document.getElementById('user_input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.querySelector('button').click();
        }
    });
</script>
""", unsafe_allow_html=True)
