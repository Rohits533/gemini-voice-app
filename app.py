import streamlit as st
import base64
from google import genai
from google.genai import types

# 1. Force Full Screen Wide Mode
st.set_page_config(
    page_title="Gemini Audio Dashboard", 
    page_icon="🎵", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Immersive Spotify/Apple Music Style Premium Theme CSS
st.markdown("""
    <style>
    /* Absolute reset to hide default Streamlit structures */
    [data-testid="stHeader"], footer, [data-testid="stSidebar"] { visibility: hidden; display: none; }
    
    .stApp {
        background: radial-gradient(circle at top right, #1f1b2e, #0f0c15 60%);
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Global Content Box Adjustment */
    .block-container {
        padding: 0rem !important;
        max-width: 100% !important;
    }
    
    /* Sidebar Navigation panel styling */
    .nav-sidebar {
        background-color: #12101a;
        height: 100vh;
        padding: 2rem 1.5rem;
        border-right: 1px solid rgba(255,255,255,0.03);
        position: fixed;
        width: 240px;
        left: 0;
        top: 0;
    }
    .nav-item {
        padding: 0.75rem 1rem;
        color: #9ca3af;
        font-weight: 500;
        border-radius: 8px;
        cursor: pointer;
        margin-bottom: 0.25rem;
    }
    .nav-item.active {
        background: linear-gradient(90deg, rgba(236,72,153,0.15), transparent);
        color: #ec4899;
        border-left: 3px solid #ec4899;
    }
    
    /* Main Content Wrapper Window */
    .main-dashboard {
        margin-left: 260px;
        padding: 2.5rem;
        margin-bottom: 120px; /* Spacer for fixed footer player */
    }
    
    /* Section Headers */
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
    }
    
    /* Main Hero Featured Cards */
    .hero-container {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 2.5rem;
    }
    .hero-card {
        background: linear-gradient(135deg, #2e1a47, #160f24);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 1.5rem;
        flex: 1;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    .hero-card-pink {
        background: linear-gradient(135deg, #5c2568, #200b2b);
    }
    
    /* Media Player Fixed Controller Footer Bar */
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
    
    /* Re-route native Chat Input element styling to become the audio search trigger bar */
    [data-testid="stChatInput"] {
        background-color: #1a1626 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 30px !important;
        padding: 0.5rem 1rem !important;
    }
    
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar UI Layout Component 
st.markdown("""
    <div class="nav-sidebar">
        <h3 style="color:#fff; font-weight:800; margin-bottom:2rem; letter-spacing:-1px;">🎵 AudioStudio</h3>
        <div class="nav-item active">🏠 Home</div>
        <div class="nav-item">✨ Recommendations</div>
        <div class="nav-item">🔥 New Releases</div>
        <div class="nav-item">📈 Top Charts</div>
        <div class="nav-item">📻 Radio</div>
        <br>
        <p style="font-size:0.75rem; color:#4b5563; text-transform:uppercase; font-weight:700; padding-left:1rem;">Playlists</p>
        <div class="nav-item" style="font-size:0.9rem;">✨ Best Hits of Mine</div>
        <div class="nav-item" style="font-size:0.9rem;">🔥 Recent AI Generations</div>
    </div>
""", unsafe_allow_html=True)

# 4. Main Window Content Area
st.markdown('<div class="main-dashboard">', unsafe_allow_html=True)

# Top Premium Greetings Header
st.markdown('<p class="dashboard-title">Discover Voice Assets</p>', unsafe_allow_html=True)
st.markdown('<p style="color:#9ca3af; margin-bottom:2rem;">Speak to compile custom synthesized speech layouts instantly.</p>', unsafe_allow_html=True)

# Visual Grid Mockup Layout matching user image choice
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        <div class="hero-card">
            <span style="color:#ec4899; text-transform:uppercase; font-size:0.75rem; font-weight:700;">Featured Agent</span>
            <h2 style="margin-top:5px; margin-bottom:5px; font-weight:800;">Jose Carreras</h2>
            <p style="color:#9ca3af; font-size:0.9rem;">Bel canto ambient generation preset active.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="hero-card hero-card-pink">
            <span style="color:#a855f7; text-transform:uppercase; font-size:0.75rem; font-weight:700;">Active Pipeline</span>
            <h2 style="margin-top:5px; margin-bottom:5px; font-weight:800;">Best Day Voice Suite</h2>
            <p style="color:#e9d5ff; font-size:0.9rem;">Low-latency audio synthesis engine online.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown('<br><h3 style="font-weight:700; margin-bottom:1rem;">Conversation History Logs</h3>', unsafe_allow_html=True)

# 5. Core Voice/Logic System Configuration
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 API Key Missing. Please insert GEMINI_API_KEY inside Streamlit Cloud Secrets panel.")
    st.stop()

client = genai.Client(api_key=api_key)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Output the running chat dialogue feed inside clear styled blocks
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

st.markdown('</div>', unsafe_allow_html=True) # Closing Main Dashboard tag wrapper

# 6. Fixed Player Controller Footer System
st.markdown('<div class="fixed-player-bar">', unsafe_allow_html=True)

# Grid to position the prompt controller nicely along the bottom axis
f_col1, f_col2 = st.columns([1, 2])

with f_col1:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:12px; margin-top:5px;">
            <div style="background-color:#c084fc; width:45px; height:45px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:800;">AI</div>
            <div>
                <p style="margin:0; font-weight:600; font-size:0.95rem;">Gemini Realtime Engine</p>
                <p style="margin:0; color:#9ca3af; font-size:0.75rem;">Status: Ready to stream</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

with f_col2:
    # Anchor the Streamlit unified mic/text selector directly inside the right panel segment
    prompt = st.chat_input("Speak or Type your search layout...", accept_audio=True)

st.markdown('</div>', unsafe_allow_html=True) # Closing Fixed Player Bar layout

# 7. Execution Engine Action Handler
if prompt:
    user_text = prompt.text if hasattr(prompt, 'text') else prompt.get("text", "")
    uploaded_audio = prompt.audio if hasattr(prompt, 'audio') else prompt.get("audio")
    
    contents_payload = []
    
    if uploaded_audio:
        audio_data_bytes = uploaded_audio.read()
        contents_payload.append(types.Part.from_bytes(data=audio_data_bytes, mime_type="audio/wav"))
        if not user_text:
            user_text = "🎙️ Audio Search Request"
            
    if user_text and user_text != "🎙️ Audio Search Request":
        contents_payload.append(user_text)

    if contents_payload:
        st.session_state.chat_history.append({"role": "user", "text": user_text})
        
        try:
            contents_payload.append("Keep response under 2 sentences.")
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents_payload
            )
            ai_text_summary = response.text
            
            # Synthesize voice feedback loop
            tts_response = client.models.generate_content(
                model='gemini-2.5-flash-tts',
                contents=f"Say naturally: {ai_text_summary}"
            )
            
            audio_parts = [
                part for part in tts_response.candidates[0].content.parts 
                if part.inline_data and part.inline_data.mime_type.startswith("audio/")
            ]
            
            # Append response and force immediate refresh to autoplay audio
            st.session_state.chat_history.append({"role": "assistant", "text": ai_text_summary})
            
            if audio_parts:
                # Store voice binary temporarily to kickstart autoplay upon context refresh
                st.audio(audio_parts[0].inline_data.data, format="audio/mp3", autoplay=True)
                
            st.rerun()

        except Exception as e:
            st.error(f"Error handling request: {e}")
