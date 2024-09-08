from groq import Groq
import base64
import os
import streamlit as st
from IPython.display import Image, display

# Set up Groq client
key = "Your API Key "  # Replace with your actual API key
client = Groq(api_key=key)
llava_model = 'llava-v1.5-7b-4096-preview'

#Image encoding function
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Function to generate text from images and prompt using Groq LLaVA model
def image_to_text(client, model, base64_images, prompt):
  chat_completion = client.chat.completions.create(
      messages=[
          {
              "role": "user",
              "content": [
                  {"type": "text", "text": prompt},
                  {
                      "type": "image_url",
                      "image_url": {
                          "url": f"data:image/jpeg;base64,{base64_images[0]}",
                      },
                  },
              ],
          }
      ],
      model=model
  )

  return chat_completion.choices[0].message.content

# Streamlit UI element
uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

# Text prompt input 
testing_instructions_prompt = st.text_area("Enter your prompt:")

# Define the testing instructions prompt
prompt  = "describe testing instructions for any digital product's features, based on the screenshots. Output should describe a detailed, step-by-step guide on how to test each functionality. Each test case should include: Description: What the test case is about. Pre-conditions: What needs to be set up or ensured before testing. Testing Steps: Clear, step-by-step instructions on how to perform the test. Expected Result: What should happen if the feature works correctly."

# Button to trigger text generation
if uploaded_files and prompt:
    # Encode images
    base64_images = []
    for uploaded_file in uploaded_files:
        try:
            filename = uploaded_file.name
            bytes_data = uploaded_file.read()
            base64_images.append(base64.b64encode(bytes_data).decode('utf-8'))
            # prompt += f"Filename: {filename}\n"            # Add filename to prompt
            prompt = prompt + testing_instructions_prompt  # Add testing instructions prompt
        except Exception as e:
            st.error(f"Error encoding image: {e}")

    # Generate text from images and prompt
    if st.button("Generate Text"):
      if base64_images:
        try:
          outputs = []
          for image in base64_images:
            output = image_to_text(client, llava_model, [image], prompt)
            outputs.append(output)

          concatenated_output = "\n".join(outputs)
          st.success("Generated text:")
          st.write(concatenated_output)
        except Exception as e:
          st.error(f"Error generating text: {e}")
