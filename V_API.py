from flask import Flask, request, render_template
import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from google.cloud import translate_v2 as translate
import base64

app = Flask(__name__)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'serviceacc_token.json'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            image_content = file.read()

            # Process image with Google Cloud Vision API
            client = vision_v1.ImageAnnotatorClient()
            image = vision_v1.Image(content=image_content)
            response = client.text_detection(image=image)
            texts = response.text_annotations

            descriptions = [text.description for text in texts]
            text_to_translate = descriptions[0] if descriptions else ''

            # Translate text
            translate_client = translate.Client()
            target_language = 'en'
            translation = translate_client.translate(text_to_translate, target_language=target_language)
            translated_text = translation['translatedText']

            # Encode image to base64
            img_data = base64.b64encode(image_content).decode('utf-8')

            return render_template('index.html', translated_text=translated_text, img_data=img_data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
