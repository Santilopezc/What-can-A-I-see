import streamlit as st
import cv2
from speech_to_text import transcribe
from description_model import describe_image
from text_to_speech import speak
import speech_recognition as sr
import time

from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.app_logo import add_logo
from streamlit_extras.mention import mention
from streamlit_extras.add_vertical_space import add_vertical_space

# Function to capture audio and picture
def capture_picture():
    cap = cv2.VideoCapture(0)  # Change index for different cameras
    for _ in range(10):
        ret, frame = cap.read()
    # Now capture the frame
    ret, frame = cap.read()
    fs = 44100  # Sample rate
    cv2.imwrite("captured_image.jpg", frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cap.release()
    return frame




def display():
    global state
    st.set_page_config(layout='wide')
    add_logo("logo.png", height = 300)
    
    # Display title and button
    st.title("What can (A)I see? :eyes:")
    
    with stylable_container(
            key="container_buttons",
            css_styles="""
                {
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px);
                    text-align: center;
                }
                """,
        ):
      colA, colB = st.columns(2)
    
      with colA:
        with stylable_container(
            key="whatcanAIsee_button",
            css_styles="""
                button {
                    background-color: red;
                    color: black;
                    border-radius: 20px;
                    width: 75%;
                    transition: all 0.5s;
                    font-size: 28px;
                    font-weight : 700;
                }
                """,
        ):
            start_button = st.button("Describe!")
      with colB:
        popover = st.popover("Settings")
        save_image = popover.checkbox("Save image", True)
        save_audio = popover.checkbox("Save audio", True)
        save_description = popover.checkbox("Save description", True)
    
    num = 0
    if save_image:
      num +=1
    if save_audio:
      num +=1
    if save_description:
      num +=1

    if start_button:
       state = "listening"
       start_button = False

    placeholder_text1 = st.empty()
    placeholder_text2 = st.empty()
    placeholder_transcription = st.empty()
    placeholder_image_and_desc = st.empty()
    savings_placeholder = st.empty()
    footer_placeholder = st.empty()
    add_vertical_space(5)
    with stylable_container(key="bottom",
                            css_styles="""
                {
                  padding : 0px;
                  margin: 0px;
                }
                """,):
      colx, coly = footer_placeholder.columns(2)

      with colx:
        with stylable_container(
            key="quotes",
            css_styles="""
                {
                  padding : 0px;
                  margin: 0px;
                  text-align: left;
                }
                """,
        ):
          st.write("This is a web app demo for the final project fo the course of Deep Learning @UGent")
          st.write("Bermúdez Gregorio, Dokupil Michal, López Santiago, Plebani Paola and Ramcke David")

      with coly:
        with stylable_container(
            key="mention_github",
            css_styles="""
                {text-align: right;
                }
                """,
        ):
          mention(
          label="Code source",
          icon="github",  
          url="hhttps://github.com/Santilopezc/What-can-A-I-see",
          )

    while True:

      if state == "idle":
        keyword = "hello"
        r = sr.Recognizer()
        with sr.Microphone() as source:
            placeholder_text1.write("Listening for keyword...")
            audio = r.listen(source)
            #state = "listening" # TODO delete this line
            try:
                text = r.recognize_google(audio)
                if keyword in text.lower():
                  state = "listening"

            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                pass
                #st.error
      
      # if "What can AI see button is pressed"
      #if start_button:
      
      if state == "listening" or start_button:
          state = "idle"
          placeholder_text1.empty()
          placeholder_text2.empty()
          placeholder_transcription.empty()
          
          savings_placeholder.empty()
          #footer_placeholder.empty()
          
          placeholder_text1.write("Recording request...")
          transcription = transcribe()
          frame = capture_picture()
          
          
      
          #transcription = "This is the transcription" *10
          #frame = "image_test.jpg"
          #image = cv2.imread(frame)
          #image_description = "This is the image description" *10000
          
          placeholder_text1.write("Your request has been successfully recorded! :alien:")
          placeholder_text2.header("Your transcription", divider="rainbow")
          # display audio transcription
          with placeholder_transcription.container(height=80):
              st.markdown(transcription)

          # display image and description
          placeholder_image_and_desc.empty()
          with placeholder_image_and_desc.container():
            col1, col2 = st.columns(2)
      
            with col1:
              st.header("Your image :eyes:", divider="rainbow")
              st.image(frame)
      
            with col2:
              st.header("Image description :lips:", divider="rainbow")
              with st.container(height=450):
                image_description = describe_image(transcription, "captured_image.jpg")
                st.markdown(image_description)
      
          speak(image_description)
      
      
          #savings (only if selected)
          if num != 0:
            with savings_placeholder.container(height=50*num):
              if save_image:
                  # save image
                  st.write("Your image has been saved! :penguin:")
              if save_audio:
                  # save audio
                  st.write("Your audio has been saved! :penguin:")
              if save_description:
                  # save description
                  st.write("Your description has been saved! :penguin:")
          else:
            with savings_placeholder.container(height=50):
              st.write("Nothing has been saved :dizzy_face:")
          

          state = "idle"
      else:
        savings_placeholder.write(" ")



# main:

state = "idle"  # values: "idle", "listening" maybe "processing"
display()
