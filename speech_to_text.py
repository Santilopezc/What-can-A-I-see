import speech_recognition as sr
import time

# Configure speech recognition engine
r = sr.Recognizer()

# Conversation loop
while True:
    # Listen for user speech input
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)  # Optional: Adjust for ambient noise levels
        audio = r.listen(source, timeout=5)

    # Convert speech to text
    print('finished listening')
    user_input = r.recognize_google(audio)
    print(user_input)

    if 'stop' in user_input:
        break
    

