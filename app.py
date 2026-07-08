import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="Savan Audio Lab", 
    page_icon="🎙️", 
    layout="wide",
    initial_sidebar_state="expanded" 
)

# 2. Modern Minimalist Sidebar CSS
st.markdown("""
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
    
    /* Make the navigation choices look professional and clean */
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
    
    /* Premium Grid Cards styling */
    .hero-card {
        background: linear-gradient(135deg, #1d182b, #110e1a);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 16px;
        padding: 1.75rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
    }
    
    /* Portfolio Button Link Styling */
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
    
    /* Fixed Audio Controller Footer Bar */
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
    
    /* Styled container for history transcripts in sidebar */
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
""", unsafe_allow_html=True)

# Initialize Session Memory States Early
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 3. INTERACTIVE SIDEBAR (Home, About, and History Logs)
with st.sidebar:
    # 📝 YOUR NEW LINKED BRAND NAME:
    st.markdown('<h2 style="color:#fff; font-weight:800; margin-bottom:2rem; letter-spacing:-1px;">✨ Savan Audio Lab</h2>', unsafe_allow_html=True)
    
    menu_selection = st.radio(
        "Navigation Links",
        ["🏠 Home", "ℹ️ About Application"]
    )
    
    st.markdown('<br><hr style="border-color: rgba(255,255,255,0.05);"><br>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.75rem; color:#6b7280; text-transform:uppercase; font-weight:700; letter-spacing:1px; margin-bottom:12px;">📜 Chat History Logs</p>', unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        st.markdown('<p style="font-size:0.85rem; color:#4b5563; font-style:italic;">No recent sessions found.</p>', unsafe_allow_html=True)
    else:
        for idx, msg in enumerate(st.session_state.chat_history):
            role_label = "👤 You" if msg["role"] == "user" else "✨ Assistant"
            short_text = msg["text"][:35] + "..." if len(msg["text"]) > 35 else msg["text"]
            st.markdown(f"""
                <div class="sidebar-history-box">
                    <strong>{role_label}:</strong> {short_text}
                </div>
            """, unsafe_allow_html=True)

# 4. MAIN WINDOW WORKSPACE ROUTER
if menu_selection == "🏠 Home":
    st.markdown('<h1 style="font-size: 2.8rem; font-weight: 800; letter-spacing: -1.5px; margin-bottom:0;">Voice Workspace</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9ca3af; font-size:1.1rem; margin-bottom:2.5rem;">Speak or type below to interact with the audio asset platform.</p>', unsafe_allow_html=True)

    # Core Grid Informational Cards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="hero-card">
                <span style="color:#ec4899; text-transform:uppercase; font-size:0.75rem; font-weight:700; letter-spacing:1px;">Core Pipeline</span>
                <h2 style="margin-top:5px; margin-bottom:8px; font-weight:800; color:#fff;">Gemini 2.5 Engine</h2>
                <p style="color:#9ca3af; font-size:0.95rem; margin-bottom:0;">Multimodal context analytics system optimized and ready.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="hero-card" style="background: linear-gradient(135deg, #281534, #110917);">
                <span style="color:#a855f7; text-transform:uppercase; font-size:0.75rem; font-weight:700; letter-spacing:1px;">Latency Profile</span>
                <h2 style="margin-top:5px; margin-bottom:8px; font-weight:800; color:#fff;">Realtime Session</h2>
                <p style="color:#caa5e6; font-size:0.95rem; margin-bottom:0;">Low-latency context loops running live.</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<br><h2 style="font-weight:800; margin-bottom:1.5rem; letter-spacing:-0.5px;">Active Conversation Feed</h2>', unsafe_allow_html=True)

    # Output active full dialogue chat streams right in center display space
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["text"])

else:
    st.markdown('<h1 style="font-size: 2.8rem; font-weight: 800; letter-spacing: -1.5px; margin-bottom:0;">About Platform</h1>', unsafe_allow_html=True)
    st.markdown("""
        <div class="hero-card" style="margin-top:2rem;">
            <h3 style="color:#fff; font-weight:700; margin-bottom:5px;">Enterprise Voice Assistant</h3>
            <p style="color:#6b7280; font-size:0.9rem; font-weight:600; text-transform:uppercase; margin-bottom:15px; letter-spacing:0.5px;">
                Built by Rohit Savan • 17-Year-Old Developer from Mumbai
            </p>
            <p style="color:#9ca3af; line-height:1.6; margin-bottom:20px;">
                This platform compiles real-time voice and audio input processing routines through Google's Gemini Flash infrastructure. 
                Designed for high-throughput deployment, it delivers ultra-low turn-taking latencies in a unified minimal environment.
            </p>
            <a href="https://rohits533.github.io/" target="_blank" class="portfolio-btn">🌐 View My Portfolio</a>
        </div>
    """, unsafe_allow_html=True)

# 5. SECURE CREDENTIALS SETUP
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 API Key Missing. Please set your GEMINI_API_KEY value inside Streamlit Cloud Secrets.")
    st.stop()
    
client = genai.Client(api_key=api_key)

# 6. FIXED AUDIO CONTROLLER TASKBAR (Only renders on Home layout screen)
if menu_selection == "🏠 Home":
    st.markdown('<div class="fixed-player-bar">', unsafe_allow_html=True)
    f_col1, f_col2 = st.columns([1, 2])

    with f_col1:
        st.markdown("""
            <div style="display:flex; align-items:center; gap:14px; margin-top:8px; margin-left:15px;">
                <div style="background: linear-gradient(135deg, #ec4899, #8b5cf6); width:44px; height:44px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-weight:800; color:#fff; box-shadow: 0 4px 12px rgba(236,72,153,0.3);">AI</div>
                <div>
                    <p style="margin:0; font-weight:600; font-size:0.95rem; color:#fff;">Assistant Status</p>
                    <p style="margin:0; color:#10b981; font-size:0.75rem; font-weight:600;">● Ready to Record</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with f_col2:
        prompt = st.chat_input("Speak or Type your query...", accept_audio=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # 7. LOGIC PIPELINE HOOK
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
                contents_payload.append("Keep your answer clear, direct, and under 2 sentences.")
                response = client.models.generate_content(model='gemini-2.5-flash', contents=contents_payload)
                ai_text_summary = response.text
                
                st.session_state.chat_history.append({"role": "assistant", "text": ai_text_summary})
                st.rerun()
            except Exception as e:
                st.error(f"Error handling engine context: {e}")
