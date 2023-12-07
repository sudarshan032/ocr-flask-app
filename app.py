from PIL import Image
import pytesseract
from flask import Flask, render_template, request, url_for

# Specify the path to the Tesseract executable (update this based on your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    # If the user does not select a file, submit an empty part without filename
    if file.filename == '':
        return render_template('index.html', error='No selected file')

    # Replace spaces with underscores in the filename
    filename_without_spaces = file.filename.replace(' ', '_')

    # Save the uploaded image in the static folder with a unique filename
    image_filename = f'static/{filename_without_spaces}'
    file.save(image_filename)

    # Perform OCR
    img = Image.open(file)
    text = pytesseract.image_to_string(img, config='--psm 6')


    # Pass the image filename to the result.html template
    return render_template('result.html', text=text, image_filename=image_filename)

# Adding a back button to navigate to the home page
@app.route('/back')
def back():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
