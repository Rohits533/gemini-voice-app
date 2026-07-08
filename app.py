import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="Gemini Audio Dashboard", 
    page_icon="🎵", 
    layout="wide",
    initial_sidebar_state="expanded" 
)

# 2. Advanced CSS styling for Premium UI layout
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
        width: 260px !important;
    }
    
    div[data-testid="stRadio"] > label {
        display: none; 
    }
    
    div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
        font-size: 0.95rem !important;
        color: #9ca3af !important;
        font-weight: 500 !important;
        padding: 4px 0px;
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
        margin-bottom: 1rem;
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
    </style>
""", unsafe_allow_html=True)

# 3. INTERACTIVE SIDEBAR Navigation
with st.sidebar:
    st.markdown('<h2 style="color:#fff; font-weight:800; margin-bottom:2rem; letter-spacing:-1px;">🎵 AudioStudio</h2>', unsafe_allow_html=True)
    
    menu_selection = st.radio(
        "Navigation",
        ["🏠 Home", "✨ Recommendations", "🔥 New Releases", "📈 Top Charts", "📻 Radio"]
    )
    
    st.markdown('<br><p style="font-size:0.75rem; color:#4b5563; text-transform:uppercase; font-weight:700; letter-spacing:1px; margin-bottom:5px;">Playlists</p>', unsafe_allow_html=True)
    playlist_selection = st.radio(
        "Playlists",
        ["✨ Best Hits of Mine", "🔥 Recent AI Generations"]
    )

# 4. MAIN DASHBOARD SPACE
st.markdown(f'<h1 style="font-size: 2.8rem; font-weight: 800; letter-spacing: -1.5px; margin-bottom:0;">{menu_selection}</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#9ca3af; font-size:1.1rem; margin-bottom:2.5rem;">Speak or type below to compile real-time speech assets natively.</p>', unsafe_allow_html=True)

# Main Grid Cards
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

# 5. INITIALIZE GEMINI CORE ENGINE
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

# 6. FIXED STICKY AUDIO CONTROLLER TASKBAR
st.markdown('<div class="fixed-player-bar">', unsafe_allow_html=True)
f_col1, f_col2 = st.columns([1, 2])

with f_col1:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:14px; margin-top:8px; margin-left:15px;">
            <div style="background: linear-gradient(135deg, #ec4899, #8b5cf6); width:44px; height:44px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-weight:800; color:#fff; box-shadow: 0 4px 12px rgba(236,72,153,0.3);">AI</div>
            <div>
                <p style="margin:0; font-weight:600; font-size:0.95rem; color:#fff;">Gemini Realtime Engine</p>
                <p style="margin:0; color:#10b981; font-size:0.75rem; font-weight:600;">● Online & Stable</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

with f_col2:
    prompt = st.chat_input("Speak or Type your query...", accept_audio=True)

st.markdown('</div>', unsafe_allow_html=True)

# 7. EXECUTION REQUEST PROMPTING HOOK
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
            # Explicit system instruction passed cleanly inside standard generation configuration rules
            contents_payload.append(
                "You are an elegant, elite AI voice companion just like Siri or Gemini Live. "
                "Process the input query and provide a sophisticated response. Keep it concise "
                "(under 2 sentences)."
            )
            
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=contents_payload
            )
            ai_text_summary = response.text
            
            # Log the text answer beautifully inside the conversation panel framework
            st.session_state.chat_history.append({"role": "assistant", "text": ai_text_summary})
            st.rerun()
            
        except Exception as e:
            st.error(f"Error executing logic sequence: {e}")
