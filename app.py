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

# 2. Complete CSS Fix - Resolving Text Overlap Problems
st.markdown("""
    <style>
    /* Total reset to hide standard Streamlit container boundaries */
    [data-testid="stHeader"], footer, [data-testid="stSidebar"] { visibility: hidden; display: none; }
    
    .stApp {
        background: radial-gradient(circle at top right, #1f1b2e, #0f0c15 60%);
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Make sure Streamlit's internal layout padding starts after our custom 260px sidebar */
    .block-container {
        padding: 0rem !important;
        max-width: 100% !important;
    }
    
    /* Strict Column/Sidebar Position Rules */
    .nav-sidebar {
        background-color: #12101a;
        height: 100vh;
        padding: 2.5rem 1.5rem;
        border-right: 1px solid rgba(255,255,255,0.03);
        position: fixed;
        width: 260px;
        left: 0;
        top: 0;
        z-index: 999;
    }
    
    .nav-item {
        padding: 0.75rem 1rem;
        color: #9ca3af;
        font-weight: 500;
        border-radius: 8px;
        margin-bottom: 0.25rem;
        font-size: 0.95rem;
    }
    .nav-item.active {
        background: linear-gradient(90deg, rgba(236,72,153,0.12), transparent);
        color: #ec4899;
        border-left: 3px solid #ec4899;
        font-weight: 600;
    }
    
    /* Content Padding to Prevent Layout Collisions */
    .dashboard-main-content {
        padding-left: 300px !important;  /* Strict margin pushing text past sidebar */
        padding-right: 40px !important;
        padding-top: 3rem !important;
        padding-bottom: 8rem !important;
    }
    
    /* Card Elements matching reference design */
    .hero-card {
        background: linear-gradient(135deg, #1d182b, #110e1a);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 16px;
        padding: 1.75rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
    }
    
    /* Media Player Bar Bottom Fix */
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
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar UI Layout Component 
st.markdown("""
    <div class="nav-sidebar">
        <h2 style="color:#fff; font-weight:800; margin-bottom:2.5rem; letter-spacing:-1px;">🎵 AudioStudio</h2>
        <div class="nav-item active">🏠 Home</div>
        <div class="nav-item">✨ Recommendations</div>
        <div class="nav-item">🔥 New Releases</div>
        <div class="nav-item">📈 Top Charts</div>
        <div class="nav-item">📻 Radio</div>
        <br><br>
        <p style="font-size:0.75rem; color:#4b5563; text-transform:uppercase; font-weight:700; padding-left:1rem; letter-spacing:1px;">Playlists</p>
        <div class="nav-item" style="font-size:0.9rem;">✨ Best Hits of Mine</div>
        <div class="nav-item" style="font-size:0.9rem;">🔥 Recent AI Generations</div>
    </div>
""", unsafe_allow_html=True)

# 4. Content Area Container Wrapper
# Everything inside this container gets padded cleanly away from the sidebar
with st.container():
    st.markdown('<div class="dashboard-main-content">', unsafe_allow_html=True)
    
    st.markdown('<h1 style="font-size: 2.8rem; font-weight: 800; letter-spacing: -1.5px; margin-bottom:0;">Discover Voice Assets</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9ca3af; font-size:1.1rem; margin-bottom:2.5rem;">Speak or type below to compile real-time speech assets natively.</p>', unsafe_allow_html=True)
    
    # Grid Content Rows using native safe metrics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="hero-card">
                <span style="color:#ec4899; text-transform:uppercase; font-size:0.75rem; font-weight:700; letter-spacing:1px;">Featured Agent</span>
                <h2 style="margin-top:5px; margin-bottom:8px; font-weight:800; color:#fff;">Jose Carreras</h2>
                <p style="color:#9ca3af; font-size:0.95rem; margin-bottom:0;">Bel canto ambient generation preset active.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="hero-card" style="background: linear-gradient(135deg, #281534, #110917);">
                <span style="color:#a855f7; text-transform:uppercase; font-size:0.75rem; font-weight:700; letter-spacing:1px;">Active Pipeline</span>
                <h2 style="margin-top:5px; margin-bottom:8px; font-weight:800; color:#fff;">Best Day Voice Suite</h2>
                <p style="color:#caa5e6; font-size:0.95rem; margin-bottom:0;">Low-latency audio synthesis engine online.</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<br><h2 style="font-weight:800; margin-bottom:1.5rem; letter-spacing:-0.5px;">Conversation Logs</h2>', unsafe_allow_html=True)
    
    # Core backend memory array engine
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("🔑 API Key Missing. Please set your GEMINI_API_KEY value inside Streamlit Cloud Secrets.")
        st.stop()
        
    client = genai.Client(api_key=api_key)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["text"])
            
    st.markdown('</div>', unsafe_allow_html=True) # Close dashboard-main-content wrapper

# 5. Fixed Audio Controller Taskbar Bar
st.markdown('<div class="fixed-player-bar">', unsafe_allow_html=True)
f_col1, f_col2 = st.columns([1, 2])

with f_col1:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:14px; margin-top:8px; margin-left:15px;">
            <div style="background: linear-gradient(135deg, #ec4899, #8b5cf6); width:44px; height:44px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-weight:800; color:#fff; box-shadow: 0 4px 12px rgba(236,72,153,0.3);">AI</div>
            <div>
                <p style="margin:0; font-weight:600; font-size:0.95rem; color:#fff;">Gemini Realtime Engine</p>
                <p style="margin:0; color:#10b981; font-size:0.75rem; font-weight:600;">● Online & Streaming</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

with f_col2:
    prompt = st.chat_input("Speak or Type your query...", accept_audio=True)

st.markdown('</div>', unsafe_allow_html=True)

# 6. Request Generation Cycle Hook
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
            response = client.models.generate_content(model='gemini-2.5-flash', contents=contents_payload)
            ai_text_summary = response.text
            
            tts_response = client.models.generate_content(model='gemini-2.5-flash-tts', contents=f"Say naturally: {ai_text_summary}")
            audio_parts = [part for part in tts_response.candidates[0].content.parts if part.inline_data and part.inline_data.mime_type.startswith("audio/")]
            
            st.session_state.chat_history.append({"role": "assistant", "text": ai_text_summary})
            if audio_parts:
                st.audio(audio_parts[0].inline_data.data, format="audio/mp3", autoplay=True)
                
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
