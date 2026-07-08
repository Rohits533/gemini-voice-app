import streamlit as st
import os
import base64
from google import genai
from google.genai import types

st.set_page_config(page_title="Gemini Voice Asset", page_icon="🎙️", layout="centered")

st.title("🎙️ Gemini Voice Asset Platform")
st.write("Record your voice below to interact natively with Gemini.")

# API Key Authentication Check
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    api_key = st.text_input("Enter your Gemini API Key:", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
    audio_data = st.audio_input("Click the microphone to speak")

    if audio_data is not None:
        with st.spinner("Gemini is listening and generating speech..."):
            audio_bytes = audio_data.read()
            
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[
                        types.Part.from_bytes(
                            data=audio_bytes,
                            mime_type="audio/wav"
                        ),
                        "Listen carefully to my voice input above. Answer my query directly out loud. Keep your reply conversational and under 3 sentences."
                    ],
                    config=types.GenerateContentConfig(
                        response_modalities=["AUDIO"]
                    )
                )

                audio_parts = [part for part in response.candidates[0].content.parts if part.inline_data and part.inline_data.mime_type.startswith("audio/")]
                
                if audio_parts:
                    raw_audio_output = audio_parts[0].inline_data.data
                    st.success("Response Received!")
                    st.audio(raw_audio_output, format="audio/mp3", autoplay=True)
                else:
                    st.warning("Could not generate audio output. Here is the text response:")
                    st.write(response.text)

            except Exception as e:
                st.error(f"An error occurred with the Gemini API: {e}")
else:
    st.info("💡 Please provide a valid Gemini API key to activate the voice engine pipeline.")
