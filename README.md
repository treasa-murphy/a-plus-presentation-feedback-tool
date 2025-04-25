<p align="center">
  <img src="a-plus-logo.png" width="120" alt="A+ Logo">
</p>

Presentation Delivery Feedback Tool
===================================

This project is a prototype Presentation Delivery Feedback Tool developed for 
COMP47700. It is designed to assist university students in practising and improving 
their spoken communication skills by providing automated feedback on presentation 
delivery.
## A+ Presentation Feedback Tool

<p align="center">
  <img src="/Users/treasaj2/a-plus-presentation-feedback-tool/a_plus_streamlit_tool.png" width="600" alt="Screenshot of A+ tool interface">
</p>

The tool analyses a short audio recording of the user reading a presentation-style 
passage and provides objective feedback on key delivery metrics including:

- Speech rate (Words Per Minute)
- Vocal inflection (pitch variation)
- Vocal energy (volume/projection)
- Pause usage (timing and frequency)
- Filler words (e.g., "um", "eh")

By offering structured and actionable feedback, this tool aims to help students 
deliver clearer, more confident, and more engaging presentations.

Overview of Features
--------------------

- Audio feature extraction using:
  - `librosa` for pitch and energy analysis
  - `pydub` for pause detection
  - `speech_recognition` for transcription and WPM calculation
- Automatic detection of filler words
- Rule-based evaluation logic grounded in public speaking literature
- Visualisation of key metrics (e.g., pitch contour, pause distribution)
- Simple web-based interface built with Streamlit

Typical Workflow
----------------

1. User records or uploads an audio sample of a presentation.
2. The tool processes the audio, extracts relevant features, and generates a 
transcript.
3. Heuristics evaluate the delivery and produce targeted feedback.
4. Users receive visual and textual summaries, including suggestions for 
improvement.
5. Users may re-record the passage to assess progress.

Technical Summary
-----------------

- **Speech Rate**: Calculated by dividing transcript word count by duration.
- **Pitch**: Extracted using `librosa.pyin` and analysed for range and variation.
- **Energy**: Measured using RMS (Root Mean Square) loudness.
- **Pauses**: Detected using `pydub.silence` analysis.
- **Filler Words**: Identified via keyword scan of the transcript.

Educational Value
-----------------

This tool enables users to:

- Develop greater self-awareness regarding speech delivery
- Practise critical aspects of public speaking independently
- Receive consistent, evidence-based feedback
- Monitor improvement through repeated trials

Technologies Used
-----------------

- Python
- Streamlit
- librosa
- pydub
- speech_recognition
- matplotlib / seaborn

Evaluation Method
-----------------

The tool’s impact is assessed through a before-and-after test:

- Users record a first attempt and receive feedback
- They then re-record the same passage after reviewing the suggestions
- Changes in metrics such as pitch variation, speech rate, and vocal energy are 
compared to assess improvement

References
----------

- [Presenting With Confidence 
(PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6505544/)
- [Effects of Speaking Rate on Speech and Silent Speech Recognition 
(ACM)](https://dl.acm.org/doi/fullHtml/10.1145/3491101.3519611)
- [Exploring Feedback Strategies for Public 
Speaking](https://www.researchgate.net/publication/292148167)
- [Lawrence Bernstein: The Trick to Powerful Public Speaking (TED 
Talk)](https://www.ted.com/talks/lawrence_bernstein_the_trick_to_powerful_public_speaking?language=en)

Acknowledgements
----------------

This project was created as part of the Speech and Audio Processing module at 
University College Dublin. Special thanks to those who contributed voice samples 
and to academic supervisors for their guidance.

Future Work
-----------

- Support for longer presentations
- Live recording and playback functionality
- Machine learning-based personalised feedback

