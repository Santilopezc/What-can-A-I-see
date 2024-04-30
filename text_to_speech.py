#https://gtts.readthedocs.io/en/latest/module.html#localized-accents for the language list

from gtts import gTTS
import os

# The text that you want to convert to audio
mytext = 'What can AI see?'

# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)

# Saving the converted audio in a mp3 file 
myobj.save("deeplearning.mp3")

# Playing the converted file
os.system("deeplearning.mp3")
