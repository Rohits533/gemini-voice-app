import streamlit as st
import time
from google import genai
from google.genai.errors import ResourceExhausted

# 1. Page Configuration
st.set_page_config(
    page_title="Savan Audio Lab",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Session Memory States Early
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 2. Modern Minimalist Sidebar and Guide Layout CSS
st.markdown(
    """
    <style>
    [data-testid="stHeader"], footer { visibility: hidden; display: none; }

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
        background: rgba(236, 72, 153, 0.1);
        color: #ec4899;
        border: 1px solid rgba(236, 72, 153, 0.2);
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
        background: linear-gradient(135deg, #ec4899, #8b5cf6);
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
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 8px;
        font-size: 0.85rem;
        color: #d1d5db;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2.5 API Execution Pipeline with Graceful Error Handling
def safe_generate_content(prompt_text):
    """Executes the pipeline while intercepting rate limits with live visual countdowns."""
    client = genai.Client()
    max_retries = 3
    base_delay = 20

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_text,
            )
            return response.text
        except ResourceExhausted:
            if attempt == max_retries - 1:
                st.error("🚨 API Engine Quota fully exhausted. Please try again later or upgrade your plan.")
                return None

            delay = base_delay * (2 ** attempt)
            warning_placeholder = st.empty()
            for remaining in range(delay, 0, -1):
                warning_placeholder.warning(
                    f"⚠️ **Rate Limit Hit (429)**: Free tier requests exceeded. Retrying connection in **{remaining}s**..."
                )
                time.sleep(1)
            warning_placeholder.empty()

        except Exception as e:
            st.error(f"🚨 An unexpected generation error occurred: {str(e)}")
            return None

# 3. INTERACTIVE SIDEBAR
with st.sidebar:
    st.markdown(
        '<h2 style="color:#fff; font-weight:800; margin-bottom:2rem; letter-spacing:-1px;">✨ Savan Audio Lab</h2>',
        unsafe_allow_html=True,
    )

    menu_selection = st.radio(
        "Navigation Links",
        ["🏠 Home Workspace", "📖 Engineering Guide", "ℹ️ About Application"],
    )

    st.markdown(
        '<br><hr style="border-color: rgba(255,255,255,0.05);"><br>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="font-size:0.75rem; color:#6b7280; text-transform:uppercase; font-weight:700; letter-spacing:1px; margin-bottom:12px;">📜 Chat History Logs</p>',
        unsafe_allow_html=True,
    )

    if not st.session_state.chat_history:
        st.markdown(
            '<p style="font-size:0.85rem; color:#4b5563; font-style:italic;">No recent sessions found.</p>',
            unsafe_allow_html=True,
        )
    else:
        for msg in st.session_state.chat_history:
            role_label = "👤 You" if msg["role"] == "user" else "✨ Assistant"
            short_text = msg["text"][:35] + "..." if len(msg["text"]) > 35 else msg["text"]
            st.markdown(
                f"""
                <div class="sidebar-history-box">
                    <strong>{role_label}:</strong> {short_text}
                </div>
                """,
                unsafe_allow_html=True,
            )

# 4. MAIN WINDOW WORKSPACE ROUTER
if menu_selection == "🏠 Home Workspace":
    st.markdown(
        '<h1 style="font-size: 2.8rem; font-weight: 800; letter-spacing: -1.5px; margin-bottom:0;">Voice Workspace</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#9ca3af; font-size:1.1rem; margin-bottom:2.5rem;">Speak or type below to interact with the audio asset platform.</p>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="hero-card">
                <span style="color:#ec4899; text-transform:uppercase; font-size:0.75rem; font-weight:700; letter-spacing:1px;">Core Pipeline</span>
                <h2 style="margin-top:5px; margin-bottom:8px; font-weight:800; color:#fff;">Gemini 2.5 Engine</h2>
                <p style="color:#9ca3af; font-size:0.95rem; margin-bottom:0;">Multimodal context analytics system optimized and ready.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="hero-card" style="background: linear-gradient(135deg, #281534, #110917);">
                <span style="color:#a855f7; text-transform:uppercase; font-size:0.75rem; font-weight:700; letter-spacing:1px;">Latency Profile</span>
                <h2 style="margin-top:5px; margin-bottom:8px; font-weight:800; color:#fff;">Realtime Session</h2>
                <p style="color:#caa5e6; font-size:0.95rem; margin-bottom:0;">Low-latency context loops running live.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<br><h2 style="font-weight:800; margin-bottom:1.5rem; letter-spacing:-0.5px;">Active Conversation Feed</h2>',
        unsafe_allow_html=True,
    )

    for message in st.session_state.chat_history:
        avatar_icon = "👤" if message["role"] == "user" else "✨"
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(message["text"])

    if user_input := st.chat_input("Message Savan Audio Lab..."):
        st.session_state.chat_history.append({"role": "user", "text": user_input})

        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="✨"):
            with st.spinner("Processing system context..."):
                response_content = safe_generate_content(user_input)

            if response_content:
                st.markdown(response_content)
                st.session_state.chat_history.append({"role": "assistant", "text": response_content})
                st.rerun()

elif menu_selection == "📖 Engineering Guide":
    st.markdown(
        '<h1 style="font-size: 2.8rem; font-weight: 800; letter-spacing: -1.5px; margin-bottom:0;">Architecture & Guide</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#9ca3af; font-size:1.1rem; margin-bottom:2.5rem;">A technical overview explaining how this advanced multimodal voice workspace was engineered.</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-card">
            <h3 style="color:#fff; font-weight:700; margin-bottom:10px;">🛠️ The Technology Stack</h3>
            <span class="tech-badge">Python 3.11</span>
            <span class="tech-badge">Google GenAI SDK</span>
            <span class="tech-badge">Gemini 2.5 Flash</span>
            <span class="tech-badge">Streamlit UI Engine</span>
            <span class="tech-badge">Custom CSS3 Injection</span>
            <p style="color:#9ca3af; font-size:0.95rem; line-height:1.6; margin-top:10px;">
                This application acts as a low-latency bridge between multimodal foundation models and interactive consumer interfaces.
                Inspired by systems like Siri and Gemini Live, it is designed to send prompts to Gemini and display responses in real time.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif menu_selection == "ℹ️ About Application":
    st.markdown(
        '<h1 style="font-size: 2.8rem; font-weight: 800; letter-spacing: -1.5px; margin-bottom:0;">About Savan Audio Lab</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#9ca3af; font-size:1.1rem; margin-bottom:2.5rem;">Interactive voice asset workspace interface.</p>',
        unsafe_allow_html=True,
    )
