import streamlit as st
import base64
from google import genai
from google.genai import types

# 1. Premium App Configurations
st.set_page_config(
    page_title="Gemini Live Companion", 
    page_icon="✨", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Modern Glassmorphism Premium CSS UI Styling
st.markdown("""
    <style>
    /* Hide top default streamlit accent lines and menus */
    [data-testid="stHeader"] { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Clean custom background adjustments */
    .stApp {
        background-color: #0d0e12;
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Minimize page padding layout blocks */
    .block-container {
        max-width: 680px;
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
    }

    /* Target User and Assistant Chat message wrapper designs */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 1rem 1.25rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Accent separate branding headers */
    .premium-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -1px;
        background: linear-gradient(45deg, #3b82f6, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    .premium-caption {
        color: #9ca3af;
        font-size: 0.95rem;
        margin-top: -5px;
        margin-bottom: 2rem;
    }
    
    /* Smooth style tweaks for audio tracks */
    audio {
        width: 100%;
        margin-top: 10px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Application Branding Titles
st.markdown('<p class="premium-title">✨ Gemini Search Companion</p>', unsafe_allow_html=True)
st.markdown('<p class="premium-caption">An elegant, native low-latency AI voice asset workspace.</p>', unsafe_allow_html=True)

# 3. Key Verification
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 System Configuration Error: Please append your GEMINI_API_KEY inside Streamlit Advanced Secrets.")
    st.stop()

# Initialize the Gemini engine client
client = genai.Client(api_key=api_key)

# 4. Maintain Persistent Memory Logs 
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Continuously paint the ongoing conversation to screen with sleek formatting
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])
        if "audio_bytes" in message and message["audio_bytes"]:
            st.audio(message["audio_bytes"], format="audio/mp3")

# 5. Streamlit Unified Bottom Interactivity Control
prompt = st.chat_input("Speak or Type your search query here...", accept_audio=True)

if prompt:
    user_text = prompt.text if hasattr(prompt, 'text') else prompt.get("text", "")
    uploaded_audio = prompt.audio if hasattr(prompt, 'audio') else prompt.get("audio")
    
    contents_payload = []
    
    # Process Voice Input
    if uploaded_audio:
        audio_data_bytes = uploaded_audio.read()
        contents_payload.append(
            types.Part.from_bytes(data=audio_data_bytes, mime_type="audio/wav")
        )
        if not user_text:
            user_text = "🎙️ Spoken Search Query"
            
    if user_text and user_text != "🎙️ Spoken Search Query":
        contents_payload.append(user_text)

    # Render User Query Bubble Immediately
    if contents_payload:
        with st.chat_message("user"):
            st.markdown(user_text)
        st.session_state.chat_history.append({"role": "user", "text": user_text})

        # Generate Agent AI Response
        with st.chat_message("assistant"):
            with st.spinner("Processing deep analysis..."):
                try:
                    contents_payload.append(
                        "You are an elegant, elite AI voice companion just like Siri or Gemini Live. "
                        "Process the input query and provide a sophisticated response. Keep it concise "
                        "(under 3 sentences)."
                    )
                    
                    # Generate Context Answer
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=contents_payload
                    )

                    ai_text_summary = response.text
                    st.markdown(ai_text_summary)
                    
                    # Synthesize to clean Text-to-Speech audio asset
                    try:
                        tts_response = client.models.generate_content(
                            model='gemini-2.5-flash-tts',
                            contents=f"Say naturally: {ai_text_summary}"
                        )
                        
                        audio_parts = [
                            part for part in tts_response.candidates[0].content.parts 
                            if part.inline_data and part.inline_data.mime_type.startswith("audio/")
                        ]
                        
                        if audio_parts:
                            raw_ai_voice = audio_parts[0].inline_data.data
                            st.audio(raw_ai_voice, format="audio/mp3", autoplay=True)
                            
                            st.session_state.chat_history.append({
                                "role": "assistant", 
                                "text": ai_text_summary, 
                                "audio_bytes": raw_ai_voice
                            })
                        else:
                            st.session_state.chat_history.append({"role": "assistant", "text": ai_text_summary})
                            
                    except Exception as tts_error:
                        st.session_state.chat_history.append({"role": "assistant", "text": ai_text_summary})

                except Exception as e:
                    st.error(f"Execution Error: {e}")
