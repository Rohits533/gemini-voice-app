import streamlit as st
import base64
from google import genai
from google.genai import types

# 1. Page Styling and Branding
st.set_page_config(
    page_title="Gemini Live Search Asset", 
    page_icon="✨", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom minimal styling to make it look like a clean search app
st.markdown("""
    <style>
    .block-container { max-width: 700px; padding-top: 2rem; }
    h1 { font-weight: 800; letter-spacing: -1px; }
    </style>
""", unsafe_allow_html=True)

st.title("✨ Gemini Search Assistant")
st.caption("A premium native voice & text search companion powered by Gemini 2.5 Flash")

# 2. Key Verification
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 System Error: GEMINI_API_KEY missing in Streamlit Advanced Secrets.")
    st.stop()

# Initialize the Gemini engine client
client = genai.Client(api_key=api_key)

# 3. Maintain Persistent Memory Logs 
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Continuously paint the ongoing conversation to screen
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])
        if "audio_bytes" in message and message["audio_bytes"]:
            st.audio(message["audio_bytes"], format="audio/mp3")

# 4. Streamlit Unified Bottom Interactive Input 
prompt = st.chat_input("Ask or speak to Gemini...", accept_audio=True)

if prompt:
    user_text = prompt.text if hasattr(prompt, 'text') else prompt.get("text", "")
    uploaded_audio = prompt.audio if hasattr(prompt, 'audio') else prompt.get("audio")
    
    contents_payload = []
    
    # Process Voice Input if user spoke
    if uploaded_audio:
        audio_data_bytes = uploaded_audio.read()
        contents_payload.append(
            types.Part.from_bytes(data=audio_data_bytes, mime_type="audio/wav")
        )
        if not user_text:
            user_text = "🎙️ Spoken Search Query"
            
    # Add text layer to payload if present
    if user_text and user_text != "🎙️ Spoken Search Query":
        contents_payload.append(user_text)

    # Render User Query Bubble Immediately
    if contents_payload:
        with st.chat_message("user"):
            st.markdown(user_text)
        st.session_state.chat_history.append({"role": "user", "text": user_text})

        # Generate Agent AI Response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing context & generating response..."):
                try:
                    # Clear instruction persona
                    contents_payload.append(
                        "You are an elegant, elite AI voice companion just like Siri or Gemini Live. "
                        "Process the input query and provide a sophisticated response. Keep it concise "
                        "(under 3 sentences)."
                    )
                    
                    # Call standard generation (text-based return)
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=contents_payload
                    )

                    ai_text_summary = response.text
                    st.markdown(ai_text_summary)
                    
                    # Generate text-to-speech output using Gemini's TTS model variant
                    try:
                        tts_response = client.models.generate_content(
                            model='gemini-2.5-flash-tts',
                            contents=f"Say naturally: {ai_text_summary}"
                        )
                        
                        # Extract the audio bits
                        audio_parts = [
                            part for part in tts_response.candidates[0].content.parts 
                            if part.inline_data and part.inline_data.mime_type.startswith("audio/")
                        ]
                        
                        if audio_parts:
                            raw_ai_voice = audio_parts[0].inline_data.data
                            st.audio(raw_ai_voice, format="audio/mp3", autoplay=True)
                            
                            # Record to chat history with audio
                            st.session_state.chat_history.append({
                                "role": "assistant", 
                                "text": ai_text_summary, 
                                "audio_bytes": raw_ai_voice
                            })
                        else:
                            st.session_state.chat_history.append({"role": "assistant", "text": ai_text_summary})
                            
                    except Exception as tts_error:
                        # Fallback smoothly if TTS model is not available on your API tier region
                        st.session_state.chat_history.append({"role": "assistant", "text": ai_text_summary})

                except Exception as e:
                    st.error(f"Execution Error: {e}")
