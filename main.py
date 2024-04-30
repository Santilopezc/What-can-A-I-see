from speech_to_text import transcribe
from description_model import describe_image
from text_to_speech import speak

prompt = transcribe()
image_description = describe_image(prompt)
speak(image_description)

