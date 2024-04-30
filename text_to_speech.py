#https://gtts.readthedocs.io/en/latest/module.html#localized-accents for the language list
from gtts import gTTS
from pygame import mixer
import time
import os

# The text that you want to convert to audio
#mytext = 'What can AI see?'

def speak(answer, language = 'en'):
    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=answer, lang=language, slow=False)

    # Saving the converted audio in a mp3 file 
    myobj.save("deeplearning.mp3")

    # Playing the converted file
    #os.system("deeplearning.mp3")

    # Play the audio
    mixer.init()
    mixer.music.load("deeplearning.mp3")
    mixer.music.play()

    # Wait for the audio to finish playing
    while mixer.music.get_busy():
        time.sleep(0.1)