from speech_to_text import transcribe
from description_model import describe_image
from text_to_speech import speak
from image_from_webcam import take_picture

image_path = take_picture(res_width = 512, res_height = 512)
prompt = transcribe()
image_description = describe_image(prompt, image_path)
speak(image_description)
