from elevenlabs import ElevenLabs, VoiceSettings
import streamlit as st
import base64

# --- Page config ---
st.set_page_config(page_title="AI Text to Speech Generator", page_icon="🗣️", layout="centered")

# --- Inject Google Fonts and Internal CSS (light mode) ---
st.markdown("""
<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">

<style>
  html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background-color: #ffffff;
    color: #222222;
  }

  /* Title styling */
  h1 {
    font-weight: 600;
    margin-bottom: 0.3rem;
  }

  /* Text area style */
  textarea {
    background-color: #f5f5f5 !important;
    color: #222 !important;
    border-radius: 10px;
    border: 1px solid #ccc;
    padding: 1rem;
    font-size: 1.1rem;
    resize: vertical;
  }

  /* Buttons */
  button {
    background-color: #4fa3ff;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    border: none;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    transition: background-color 0.3s ease;
  }

  button:hover {
    background-color: #3a82d7;
    cursor: pointer;
  }

  /* Download link styling */
  a {
    color: #4fa3ff;
    font-weight: 600;
    text-decoration: none;
    margin-top: 1rem;
    display: inline-block;
  }

  a:hover {
    text-decoration: underline;
  }

  /* Footer styling */
  .footer {
    margin-top: 40px;
    font-size: 13px;
    color: #555;
    text-align: center;
  }
</style>
""", unsafe_allow_html=True)

# --- ElevenLabs API setup ---
API_KEY = "sk_e52d274257ddb7decd0be211483d5444e38e3fcd6d1a418d"
client = ElevenLabs(api_key=API_KEY)

# --- Title and Description ---
st.title("🗣️ AI Text to Speech Generator")
st.caption("Powered by ElevenLabs")

# Constants
MAX_WORDS = 2500

# Text input
text_input = st.text_area("📝 Enter text (max 2500 words):", height=180)

# Language Model selection
model_choice = st.selectbox("🌐 Choose language model:", [
    "eleven_monolingual_v1",
    "eleven_multilingual_v2"
])

# Voices
voice_dict = {
    "Rachel (English 🇺🇸)": "21m00Tcm4TlvDq8ikWAM",
    "Bella (Multilingual 🌍)": "EXAVITQu4vr4xnSDxMaL",
    "Antoni (English 🇬🇧)": "ErXwobaYiN019PkySvjV",
    "Elli (English 🇺🇸)": "MF3mGyEYCl7XYWbV9V6O"
}
voice_name = st.selectbox("🎤 Choose a voice:", list(voice_dict.keys()))
voice_id = voice_dict[voice_name]

# Voice Controls
st.markdown("🎛️ **Voice Controls**")
stability = st.slider("🎚️ Stability (natural tone)", 0.0, 1.0, 0.5, 0.05)
similarity_boost = st.slider("🧠 Similarity Boost (character match)", 0.0, 1.0, 0.75, 0.05)

voice_settings = VoiceSettings(
    stability=stability,
    similarity_boost=similarity_boost
)

# Generate button and logic
if st.button("🔊 Generate & Play"):
    if not text_input.strip():
        st.warning("⚠️ Please enter some text.")
    else:
        words = text_input.strip().split()
        if len(words) > MAX_WORDS:
            st.error(f"🚫 Text exceeds the max word limit of {MAX_WORDS} words. You entered {len(words)} words.")
        else:
            try:
                with st.spinner("🧠 Generating voice..."):
                    audio_generator = client.text_to_speech.convert(
                        text=text_input,
                        voice_id=voice_id,
                        model_id=model_choice,
                        voice_settings=voice_settings
                    )
                    audio_bytes = b"".join(audio_generator)

                    st.success("✅ Audio generated!")
                    st.audio(audio_bytes, format="audio/wav")

                    # Download link
                    b64_audio = base64.b64encode(audio_bytes).decode()
                    href = f'<a href="data:audio/wav;base64,{b64_audio}" download="speech_output.wav">📥 Download Audio</a>'
                    st.markdown(href, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error: {e}")

# Footer
st.markdown('<div class="footer">© 2025 AI Text to Speech Project by AK | Kaung Kaung | Kaung Si Thu</div>', unsafe_allow_html=True)
