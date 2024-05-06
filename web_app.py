import streamlit as st
import cv2
from speech_to_text import transcribe
from description_model import describe_image
from text_to_speech import speak

# Function to capture audio and picture
def capture_picture():
    cap = cv2.VideoCapture(1)  # Change index for different cameras
    for _ in range(10):
        ret, frame = cap.read()
    # Now capture the frame
    ret, frame = cap.read()
    fs = 44100  # Sample rate
    cv2.imwrite("captured_image.jpg", frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cap.release()
    return frame

# Display title and button
st.title("Audio Recorder & Picture Taker")

if st.button("What can AI see?"):
    transcription = transcribe()
    st.write("Recording saved!")  # Add functionality to save audio
    st.write("Question: ", transcription)
    frame = capture_picture()
    st.image(frame)
    image_description = describe_image(transcription, "captured_image.jpg")
    speak(image_description)
