import streamlit as st
import tempfile
from pydub import AudioSegment
from pydub.utils import which
import speech_recognition as sr
import librosa
import numpy as np
import matplotlib.pyplot as plt

AudioSegment.converter = which("ffmpeg")

# configure page
st.set_page_config(
    page_title="A+: A Presentation Feedback Tool",
    layout="centered"
)

# customise CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #001F3F; /* navy */
        color: white; /* base font colour */
    }
    h1, h2, h3, h4, h5, h6, .stFileUploader label {
        color: white;
    }
    .custom-title {
        font-size: 42px;
        font-weight: 800;
        line-height: 1.2;
        color: #FFC0CB;
        margin-bottom: 10px;
    }
    .custom-subtitle {
        font-size: 26px;
        font-weight: 600;
        line-height: 1.2;
        margin-bottom: 30px;
        color: #FFC0CB;
    }
    .pink-header {
        color: #FFC0CB !important;
    }
    .transcript-box {
        background-color: #003366;
        color: white;
        padding: 1em;
        border-radius: 8px;
        margin-top: 0.5em;
    }
    div.stDownloadButton > button {
        color: #001F3F !important;
        background-color: #FFC0CB !important;
        border: none;
        font-weight: 600;
    }
    div.stDownloadButton > button:hover {
        background-color: #ffb6c1 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# display logo and title
st.image("a-plus-logo.png", width=150)
st.markdown("""
<div class="custom-title">A+: Pace, Loudness, Um-rate, Style</div>
<div class="custom-subtitle">A Presentation Delivery Feedback Tool</div>
""", unsafe_allow_html=True)

st.write("""
Welcome to **A+** – a real-time tool to help you practise and improve your spoken presentations.
Upload a short recording below and receive feedback on **pace**, **loudness**, **pause usage**, **filler words**, and **vocal style**.
""")

# user file uploader (WAV format required)
uploaded_file = st.file_uploader("Upload your presentation audio:", type=["wav"], label_visibility="hidden")

if uploaded_file is not None:
    with st.spinner('Analysing presentation...'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            audio = AudioSegment.from_file(uploaded_file)
            audio.export(temp_audio.name, format="wav")

            # extract features
            y, sr_ = librosa.load(temp_audio.name)
            duration = librosa.get_duration(y=y, sr=sr_)
            rms = np.mean(librosa.feature.rms(y=y))
            f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz("C2"), fmax=librosa.note_to_hz("C7"))
            avg_pitch = np.nanmean(f0)

            # interpolate pitch to smooth gaps
            f0_interp = np.copy(f0)
            nans = np.isnan(f0)
            f0_interp[nans] = np.interp(np.flatnonzero(nans), np.flatnonzero(~nans), f0[~nans])

            # detect pauses using energy threshold
            frame_length = 2048
            hop_length = 512
            energy = np.array([np.sqrt(np.mean(y[i:i+frame_length]**2)) for i in range(0, len(y), hop_length)])
            threshold = 0.02
            num_pauses = np.sum(energy < threshold)
            pause_ratio = num_pauses / len(energy)

            recogniser = sr.Recognizer()
            with sr.AudioFile(temp_audio.name) as source:
                audio_data = recogniser.record(source)
                try:
                    transcript = recogniser.recognize_google(audio_data)
                except sr.UnknownValueError:
                    transcript = "Could not understand the audio."

            word_count = len(transcript.split())
            wpm = word_count / (duration / 60)

            # filler word detection
            filler_words = ["um", "uh", "eh"]
            transcript_lower = transcript.lower()
            filler_count = sum(transcript_lower.count(word) for word in filler_words)

            # display results
            st.markdown("<h3 class='pink-header'>Analysis of Speech</h3>", unsafe_allow_html=True)
            st.write(f"<span style='color:white;'>**Speech Duration:** {duration:.2f} seconds</span>", unsafe_allow_html=True)
            st.write(f"<span style='color:white;'>**Speech Rate:** {wpm:.1f} words per minute</span>", unsafe_allow_html=True)
            st.write(f"<span style='color:white;'>**Average Pitch:** {avg_pitch:.2f} Hz</span>", unsafe_allow_html=True)
            st.write(f"<span style='color:white;'>**Average Loudness (RMS):** {rms:.4f}</span>", unsafe_allow_html=True)
            st.write(f"<span style='color:white;'>**Pause Ratio:** {pause_ratio:.2f}</span>", unsafe_allow_html=True)
            st.write(f"<span style='color:white;'>**Filler Words Count:** {filler_count}</span>", unsafe_allow_html=True)

            st.markdown("<h3 class='pink-header'>Transcript</h3>", unsafe_allow_html=True)
            st.markdown(f"""<div class='transcript-box'>{transcript}</div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            # display plots of speech features
            st.markdown("<h3 class='pink-header'>Visualisation of Speech Metrics</h3>", unsafe_allow_html=True)
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
            fig.subplots_adjust(hspace=0.5)  # add space between plots

            # pitch plot
            ax1.plot(f0_interp, color='mediumvioletred')
            ax1.set_title("Pitch Contour")
            ax1.set_xlabel("Frame")
            ax1.set_ylabel("Pitch (Hz)")
            ax1.grid(True)

            # energy plot
            ax2.plot(energy, color='deepskyblue')
            ax2.set_title("Energy Contour")
            ax2.set_xlabel("Frame")
            ax2.set_ylabel("Energy (RMS")
            ax2.grid(True)

            st.pyplot(fig)

            fig.savefig("a-plus-plots-high-res.png", dpi=300, bbox_inches="tight")

            # generate feedback report
            feedback = []
            if wpm > 180:
                feedback.append("Your speech rate is quite fast. Consider slowing down.")
            elif wpm < 110:
                feedback.append("Your speech rate is quite slow. Consider speaking a little faster.")
            else:
                feedback.append("Your speech rate is within a good range.")

            if pause_ratio > 0.2:
                feedback.append("You have frequent pauses. Practice smoother transitions.")
            else:
                feedback.append("Good use of pauses.")

            if filler_count > 5:
                feedback.append("Try to reduce filler words like 'um', 'uh', and 'eh'.")
            else:
                feedback.append("Minimal filler words detected – great job!")

            if rms < 0.01:
                feedback.append("Your voice could be more projected. Try speaking up confidently to maintain clarity and engagement.")
            elif rms > 0.1:
                feedback.append("You are speaking loudly – just make sure it’s not overwhelming. Adjust as needed for your audience.")
            else:
                feedback.append("Your voice projection is at a comfortable level.")

            st.markdown("<h3 class='pink-header'>Personalised Feedback</h3>", unsafe_allow_html=True)
            for tip in feedback:
                st.write(f"<span style='color:white;'>- {tip}</span>", unsafe_allow_html=True)

            # prepare feedback text for download 
            feedback_text = f"""
A+ Presentation Delivery Feedback Report

Speech Duration: {duration:.2f} seconds
Speech Rate: {wpm:.1f} words per minute
Average Pitch: {avg_pitch:.2f} Hz
Average Loudness (RMS): {rms:.4f}
Pause Ratio: {pause_ratio:.2f}
Filler Words Count: {filler_count}

Transcript:
{transcript}

Presentation Feedback:
"""
            feedback_text += "\n".join([f"- {tip}" for tip in feedback])

            feedback_text += "\n\nThank you for using A+ to practise and polish your speaking skills!"

            # add space before download button
            st.markdown("<br>", unsafe_allow_html=True)

            # customise download feedback button
            st.download_button(
                label="Download Your Feedback Report",
                data=feedback_text,
                file_name="presentation_feedback.txt",
                mime="text/plain"
            )


