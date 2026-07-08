import streamlit as st
import time
from google import genai
from google.genai import types
from google.genai.errors import ResourceExhausted

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Savan Audio Lab",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
[data-testid="stHeader"], footer {
    visibility: hidden;
    display: none;
}

.stApp {
    background: radial-gradient(circle at top right, #1f1b2e, #0f0c15 60%);
    color: #f3f4f6;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

[data-testid="stSidebar"] {
    background-color: #12101a !important;
    border-right: 1px solid rgba(255,255,255,0.03) !important;
    width: 280px !important;
}

div[data-testid="stRadio"] > label {
    display: none;
}

div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
    font-size: 1rem !important;
    color: #9ca3af !important;
    font-weight: 500 !important;
    padding: 6px 0px;
}

div[data-testid="stRadio"] input[type="radio"]:checked + div p {
    color: #ec4899 !important;
    font-weight: 600 !important;
}

.hero-card {
    background: linear-gradient(135deg, #1d182b, #110e1a);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 16px;
    padding: 1.75rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    margin-bottom: 1.25rem;
}

.tech-badge {
    background: rgba(236,72,153,0.1);
    color: #ec4899;
    border: 1px solid rgba(236,72,153,0.2);
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
    margin-right: 6px;
    margin-bottom: 6px;
}

.portfolio-btn {
    display: inline-block;
    background: linear-gradient(135deg,#ec4899,#8b5cf6);
    color: white !important;
    font-weight: 600;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    text-decoration: none !important;
    margin-top: 15px;
    box-shadow: 0 4px 15px rgba(236,72,153,0.3);
    transition: transform 0.2s ease;
}

.portfolio-btn:hover {
    transform: translateY(-2px);
}

.fixed-player-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #0b0910;
    border-top: 1px solid rgba(255,255,255,0.05);
    padding: 1.25rem 2.5rem;
    z-index: 9999;
    box-shadow: 0 -10px 40px rgba(0,0,0,0.5);
}

[data-testid="stChatInput"] {
    background-color: #1a1626 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 30px !important;
}

.sidebar-history-box {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 8px;
    font-size: 0.85rem;
    color: #d1d5db;
}
</style>
""", unsafe_allow_html=True)

# ---------------- GEMINI FUNCTION ----------------
def safe_generate_content(prompt_text):
    client = genai.Client()

    max_retries = 3
    base_delay = 20

    for attempt in range(max_retries):

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_text
            )

            return response.text

        except ResourceExhausted:

            if attempt == max_retries - 1:
                st.error("🚨 API Engine Quota fully exhausted. Please try again later.")
                return None

            delay = base_delay * (2 ** attempt)

            warning = st.empty()

            for remaining in range(delay, 0, -1):
                warning.warning(
                    f"⚠️ Rate Limit Hit (429)\nRetrying in **{remaining}s**..."
                )
                time.sleep(1)

            warning.empty()

        except Exception as e:
            st.error(f"🚨 {e}")
            return None

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.markdown(
        "<h2 style='color:white;'>✨ Savan Audio Lab</h2>",
        unsafe_allow_html=True
    )

    menu_selection = st.radio(
        "Navigation",
        [
            "🏠 Home Workspace",
            "📖 Engineering Guide",
            "ℹ️ About Application"
        ]
    )

    st.markdown("---")
    st.markdown("### 📜 Chat History")

    if not st.session_state.chat_history:
        st.write("*No recent sessions.*")

    else:
        for msg in st.session_state.chat_history:

            role = "👤 You" if msg["role"] == "user" else "✨ Assistant"

            text = (
                msg["text"][:35] + "..."
                if len(msg["text"]) > 35
                else msg["text"]
            )

            st.markdown(
                f"""
                <div class="sidebar-history-box">
                    <strong>{role}</strong><br>
                    {text}
                </div>
                """,
                unsafe_allow_html=True
            )

# ---------------- HOME ----------------
if menu_selection == "🏠 Home Workspace":

    st.markdown(
        "<h1>Voice Workspace</h1>",
        unsafe_allow_html=True
    )

    st.write(
        "Speak or type below to interact with the audio asset platform."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="hero-card">
            <h2>Gemini 2.5 Engine</h2>
            <p>Multimodal context analytics system optimized and ready.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="hero-card">
            <h2>Realtime Session</h2>
            <p>Low-latency context loops running live.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## Active Conversation Feed")

    for message in st.session_state.chat_history:

        avatar = "👤" if message["role"] == "user" else "✨"

        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["text"])

    if user_input := st.chat_input("Message Savan Audio Lab..."):

        st.session_state.chat_history.append(
            {
                "role": "user",
                "text": user_input
            }
        )

        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="✨"):

            with st.spinner("Processing..."):
                response = safe_generate_content(user_input)

            if response:

                st.markdown(response)

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "text": response
                    }
                )

                st.rerun()

# ---------------- GUIDE ----------------
elif menu_selection == "📖 Engineering Guide":

    st.title("Architecture & Guide")

    st.write(
        "Technical overview explaining how the application works."
    )

    st.markdown("""
    <div class="hero-card">
        <h3>🛠️ Technology Stack</h3>

        <span class="tech-badge">Python 3.11</span>
        <span class="tech-badge">Google GenAI SDK</span>
        <span class="tech-badge">Gemini 2.5 Flash</span>
        <span class="tech-badge">Streamlit</span>
        <span class="tech-badge">Custom CSS</span>

        <p>
        This application acts as a low-latency bridge between
        multimodal foundation models and interactive interfaces.
        Inspired by Siri and Gemini Live.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- ABOUT ----------------
elif menu_selection == "ℹ️ About Application":

    st.title("About Savan Audio Lab")

    st.write("Interactive voice asset workspace interface.")
