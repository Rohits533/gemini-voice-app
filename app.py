import streamlit as st
import time
import random
import hashlib
from google import genai
from google.genai import types
from google.genai.errors import ClientError

st.set_page_config(
    page_title="Savan Audio Lab",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize fundamental structural session state parameters
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processed_hashes" not in st.session_state:
    st.session_state.processed_hashes = set()

st.markdown("""
<style>
/* Hide default header wrappers completely to clean up layout */
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

.sidebar-history-box {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 8px;
    font-size: 0.85rem;
    color: #d1d5db;
}

div[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.06) !important; 
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    margin-bottom: 0.75rem !important;
}

div[data-testid="stChatMessage"] p {
    color: #f3f4f6 !important;
    font-size: 0.95rem !important;
}

.modern-portfolio-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%);
    color: #ffffff !important;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 12px 32px;
    border-radius: 30px;
    text-decoration: none !important;
    box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3);
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: 5px;
}

.modern-portfolio-btn:hover {
    background: linear-gradient(135deg, #f43f5e 0%, #a855f7 100%);
    box-shadow: 0 6px 20px rgba(236, 72, 153, 0.5), 0 0 10px rgba(139, 92, 246, 0.3);
    transform: translateY(-2px);
    color: #ffffff !important;
}

/* CUSTOM SIDEBAR TOGGLE CONTAINER */
.custom-toggle-container {
    position: fixed;
    top: 15px;
    left: 15px;
    z-index: 999999;
}
</style>
""", unsafe_allow_html=True)

# Helper function to query the model text pipeline
def safe_generate_text(prompt_text):
    client = genai.Client()
    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
        )
        return resp.text
    except ClientError as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            st.error("🚦 Rate Limit: Free quota maxed. Please wait 30 seconds before submitting.")
        else:
            st.error(f"API Connection Error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected Pipeline Error: {str(e)}")
        return None

# Helper function to query the model audio pipeline
def safe_generate_audio(audio_bytes):
    client = genai.Client()
    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "Listen to this voice question and answer naturally.",
                types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
            ],
        )
        return resp.text
    except ClientError as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            st.error("🚦 Rate Limit: Free quota maxed. Please wait 30 seconds before submitting.")
        else:
            st.error(f"API Connection Error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected Pipeline Error: {str(e)}")
        return None

# Render floating custom toggle button at top-left
st.markdown('<div class="custom-toggle-container">', unsafe_allow_html=True)
if st.button("☰ Menu", key="custom_sidebar_toggle"):
    # Since Streamlit handles visibility dynamically via state engine resets, triggering rerun switches viewport bounds
    st.html("<script>window.parent.document.querySelector('button[aria-label=\"Open sidebar\"]').click();</script>")
st.markdown('</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<h2 style="color:#fff; font-weight:800; margin-bottom:2rem; letter-spacing:-1px;">✨ Savan Audio Lab</h2>', unsafe_allow_html=True)
    menu_selection = st.radio("Navigation Links", ["🏠 Home Workspace", "📖 Engineering Guide", "ℹ️ About Application"])
    st.markdown('<br><hr style="border-color: rgba(255,255,255,0.05);"><br>', unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Cache & Reset System", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.processed_hashes = set()
        st.rerun()
        
    st.markdown('<br><p style="font-size:0.75rem; color:#6b7280; text-transform:uppercase; font-weight:700; letter-spacing:1px; margin-bottom:12px;">📜 Chat History Logs</p>', unsafe_allow_html=True)
    if not st.session_state.chat_history:
        st.markdown('<p style="font-size:0.85rem; color:#4b5563; font-style:italic;">No recent sessions found.</p>', unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            role_label = "👤 You" if msg["role"] == "user" else "✨ Assistant"
            short_text = msg["text"][:35] + "..." if len(msg["text"]) > 35 else msg["text"]
            st.markdown(f'<div class="sidebar-history-box"><strong>{role_label}:</strong> {short_text}</div>', unsafe_allow_html=True)

if menu_selection == "🏠 Home Workspace":
    # Add minor padding offset to the title block to clear the floating custom menu button
    st.markdown('<h1 style="font-size: 2.8rem; font-weight: 800; letter-spacing: -1.5px; margin-bottom:0; margin-top:20px;">Voice Workspace</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9ca3af; font-size:1.1rem; margin-bottom:2.5rem;">Use your voice or type below to interact with the audio asset platform.</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="hero-card"><span style="color:#ec4899; text-transform:uppercase; font-size:0.75rem; font-weight:700; letter-spacing:1px;">Core Pipeline</span><h2 style="margin-top:5px; margin-bottom:8px; font-weight:800; color:#fff;">Gemini 2.5 Engine</h2><p style="color:#9ca3af; font-size:0.95rem; margin-bottom:0;">Multimodal context analytics system optimized and ready.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="hero-card" style="background: linear-gradient(135deg, #281534, #110917);"><span style="color:#a855f7; text-transform:uppercase; font-size:0.75rem; font-weight:700; letter-spacing:1px;">Latency Profile</span><h2 style="margin-top:5px; margin-bottom:8px; font-weight:800; color:#fff;">Realtime Session</h2><p style="color:#caa5e6; font-size:0.95rem; margin-bottom:0;">Low-latency context loops running live.</p></div>', unsafe_allow_html=True)

    st.markdown('<br><h2 style="font-weight:800; margin-bottom:1rem; letter-spacing:-0.5px;">Voice + Chat Input</h2>', unsafe_allow_html=True)

    # Render History Layout cleanly
    for message in st.session_state.chat_history:
        avatar_icon = "👤" if message["role"] == "user" else "✨"
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(message["text"])

    # UI Inputs outside of forms to prevent layout clipping
    voice_audio = st.audio_input("Record a voice message", sample_rate=16000)
    text_input = st.chat_input("Message Savan Audio Lab...")

    # --- PERMANENT HASH LOCK EXECUTION ---
    if text_input:
        text_hash = hashlib.md5(text_input.encode()).hexdigest()
        if text_hash not in st.session_state.processed_hashes:
            st.session_state.processed_hashes.add(text_hash)
            st.session_state.chat_history.append({"role": "user", "text": text_input})
            
            with st.chat_message("user", avatar="👤"):
                st.markdown(text_input)

            with st.chat_message("assistant", avatar="✨"):
                with st.spinner("Processing text pipeline..."):
                    response_content = safe_generate_text(text_input)

                if response_content:
                    st.session_state.chat_history.append({"role": "assistant", "text": response_content})
                    st.rerun()

    elif voice_audio is not None:
        audio_bytes = voice_audio.read()
        audio_hash = hashlib.md5(audio_bytes).hexdigest()
        
        if audio_hash not in st.session_state.processed_hashes:
            st.session_state.processed_hashes.add(audio_hash)
            st.session_state.chat_history.append({"role": "user", "text": "🎤 Voice question recorded"})
            
            with st.chat_message("user", avatar="👤"):
                st.markdown("🎤 Voice question recorded")
                st.audio(audio_bytes, format="audio/wav")

            with st.chat_message("assistant", avatar="✨"):
                with st.spinner("Processing audio pipeline..."):
                    response_content = safe_generate_audio(audio_bytes)

                if response_content:
                    st.session_state.chat_history.append({"role": "assistant", "text": response_content})
                    st.rerun()

elif menu_selection == "📖 Engineering Guide":
    st.markdown('<h1 style="font-size: 2.8rem; font-weight: 800; letter-spacing: -1.5px; margin-bottom:0; margin-top:20px;">Architecture & Guide</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9ca3af; font-size:1.1rem; margin-bottom:2.5rem;">A technical overview explaining how this advanced multimodal voice workspace was engineered.</p>', unsafe_allow_html=True)
    st.markdown('<div class="hero-card"><h3 style="color:#fff; font-weight:700; margin-bottom:10px;">🛠️ The Technology Stack</h3><span class="tech-badge">Python 3.11</span><span class="tech-badge">Google GenAI SDK</span><span class="tech-badge">Gemini 2.5 Flash</span><span class="tech-badge">Streamlit UI Engine</span><span class="tech-badge">Custom CSS3 Injection</span><p style="color:#9ca3af; font-size:0.95rem; line-height:1.6; margin-top:10px;">This app keeps both text chat and voice input, and routes each to Gemini.</p></div>', unsafe_allow_html=True)

elif menu_selection == "ℹ️ About Application":
    st.markdown('<h1 style="font-size: 2.8rem; font-weight: 800; letter-spacing: -1.5px; margin-bottom:0; margin-top:20px;">About Savan Audio Lab</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9ca3af; font-size:1.1rem; margin-bottom:2.5rem;">Interactive voice + chat workspace built with Streamlit and Gemini.</p>', unsafe_allow_html=True)
    st.markdown('<div class="hero-card"><h3 style="color:#fff; font-weight:700; margin-bottom:10px;">About This Application</h3><p style="color:#9ca3af; font-size:0.95rem; line-height:1.7; margin-bottom:12px;">Savan Audio Lab is a modern AI voice and chat interface. It lets users speak or type a question, then sends it to Gemini for a fast response inside a polished workspace.</p><p style="color:#9ca3af; font-size:0.95rem; line-height:1.7; margin-bottom:12px;">The app includes a voice input flow, a text chat flow, session history, and a clean sidebar layout for easy navigation.</p><p style="color:#9ca3af; font-size:0.95rem; line-height:1.7; margin-bottom:0;">Hi, I’m Rohit Savan, 17 years old, from Mumbai.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-card" style="background: linear-gradient(135deg, #23162d, #120d18);"><h3 style="color:#fff; font-weight:700; margin-bottom:10px;">What This App Does</h3><p style="color:#cbd5e1; font-size:0.95rem; line-height:1.7; margin-bottom:0;">It combines voice input, text chat, session history, and a polished sidebar layout. You can ask a question by typing or speaking, and Gemini will respond in the same interface.</p></div>', unsafe_allow_html=True)
    st.markdown('<a href="https://rohits533.github.io" target="_blank" class="modern-portfolio-btn">✨ View Portfolio</a>', unsafe_allow_html=True)
