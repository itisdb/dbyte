import requests

# Open the file in read mode > keep the token in the file named huggingface.token
with open('huggingface.token', 'r') as file:
    # Read the contents of the file and store it in a variable
    file_contents = file.read()
token = file_contents

with open('creator.string', 'r') as file:
    # Read the contents of the file and store it in a variable
    file_contents = file.read()
creator_string = file_contents

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": token.strip()}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

image_bytes = query({
	"inputs": creator_string,
})

# You can access the image with PIL.Image for example
# import io
# from PIL import Image
# image = Image.open(io.BytesIO(image_bytes))
with open("debug_image.png", "wb") as f:
    f.write(image_bytes)
