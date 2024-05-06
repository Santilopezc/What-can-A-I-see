import tkinter as tk
import cv2
import pyaudio
import wave
import threading
import speech_recognition as sr
from PIL import Image, ImageTk
from speech_to_text import transcribe
from description_model import describe_image
from text_to_speech import speak

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.vid = cv2.VideoCapture(0)  # Access the camera
        self.video_canvas = tk.Canvas(window, width=200, height=150)  # Size of the video stream canvas
        self.video_canvas.grid(row=0, column=0, padx=10, pady=10)  # Place in upper-left corner
        
        self.photo_canvas = tk.Canvas(window, width=800, height=600)  # Size of the canvas for displaying the picture
        self.photo_canvas.grid(row=0, column=1, padx=10, pady=10)  # Place in the next column
        
        self.btn_snapshot = tk.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.grid(row=1, columnspan=2, padx=10, pady=10)
        
        self.delay = 10
        self.update()
        
        # Audio recording variables
        self.audio_thread = None
        self.audio_frames = []
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.WAVE_OUTPUT_FILENAME = "output.wav"
        self.audio_stream = None
        self.audio_recording = True

        self.audio_thread = threading.Thread(target=self.record_audio)
        self.audio_thread.start()

        # Speech recognition
        self.r = sr.Recognizer()
        self.keyword = "hello"

        self.window.after(1000, self.listen_for_keyword)
        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (200, 150))  # Resize the frame
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.video_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)

    def record_audio(self):
        self.audio_stream = pyaudio.PyAudio().open(format=self.FORMAT,
                                                    channels=self.CHANNELS,
                                                    rate=self.RATE,
                                                    input=True,
                                                    frames_per_buffer=self.CHUNK)
        self.audio_frames = []
        while self.audio_recording:
            data = self.audio_stream.read(self.CHUNK)
            self.audio_frames.append(data)


    def snapshot(self, path="snapshot.png"):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.flip(frame, 1)
            cv2.imwrite(path, frame)
            # Display the picture on the photo canvas
            self.photo_canvas.delete("all")
            self.saved_photo = ImageTk.PhotoImage(image=Image.open("snapshot.png").resize((800, 600), Image.ANTIALIAS))
            self.photo_canvas.create_image(0, 0, image=self.saved_photo, anchor=tk.NW)
            print("Snapshot taken!")
        return path


    def listen_for_keyword(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio_data = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio_data)
                print("You said:", text)
                if self.keyword in text:
                    print("Hello World")
                    self.process_question()
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand what you said.")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))


        self.window.after(5000, self.listen_for_keyword)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def process_question(self):
        # TODO maybe take more pictures in some short time interval and preprocess somehow for better input
        self.update()
        prompt = transcribe()
        img_path = self.snapshot()
        image_description = describe_image(prompt, img_path)
        speak(image_description)

# Create a window and pass it to the CameraApp class
root = tk.Tk()
app = CameraApp(root, "Tkinter Camera App")
