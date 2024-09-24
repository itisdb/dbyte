import pytesseract
from googletrans import Translator
from PIL import Image, ImageDraw, ImageFont

# Initialize translator
translator = Translator()

# Load an image from file
def load_image(image_path):
    return Image.open(image_path)

# Extract text from the image
def extract_text(image):
    return pytesseract.image_to_string(image)

# Translate text into the desired language
def translate_text(text, target_language='en'):
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Draw translated text onto the image
def draw_text_on_image(image, translated_text):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Write the text at the top-left corner
    text_position = (10, 10)  # Adjust this as needed
    draw.text(text_position, translated_text, fill=(255, 0, 0), font=font)
    
    return image

# Main function to load, translate, and write text on the image
def process_image(image_path, target_language='en'):
    # Load the image
    image = load_image(image_path)

    # Extract the text from the image
    extracted_text = extract_text(image)

    # Translate the extracted text
    translated_text = translate_text(extracted_text, target_language)

    # Write the translated text back onto the image
    processed_image = draw_text_on_image(image, translated_text)

    # Save or display the modified image
    processed_image.show()  # Display the image
    processed_image.save('translated_image.png')  # Save the new image

# Example usage
if __name__ == "__main__":
    image_path = '1.jpg'  # Path to your input image
    target_language = 'es'  # Translate to Spanish (or any other language)
    process_image(image_path, target_language)
