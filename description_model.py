from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image




prompt_prefix_1 = 'Describe this image regarding that you are giving a blind person details about their surroundings, on top of this they ask you the following task:'
prompt_prefix_2 = 'Describe this image as if you were describing the user what is in front of them, on top of this they ask you the following task:'
prompt_prefix_3 = 'You are describing a blind person details about their surroundings, they also gave you the following task:'
prompt_prefix_4 = 'Generate a description of the image below suitable for visually impaired assistance, taking into account user requests: '
user_prompt = "How much should I wait to cross the road?"

def describe_image(user_prompt, provided_image_path):
    model_id = "vikhyatk/moondream2"
    revision = "2024-04-02"
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, revision=revision)
    
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

    image = Image.open(provided_image_path)
    enc_image = model.encode_image(image)
    
    return model.answer_question(,f"{prompt_prefix_3} {user_prompt}", tokenizer)

#print(model.answer_question(enc_image, f"{prompt_prefix_3} {user_prompt}", tokenizer))
