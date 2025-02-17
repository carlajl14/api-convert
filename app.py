from flask import Flask, request, send_file
from PIL import Image
from fpdf import FPDF
import os

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_image_to_pdf():
    if 'image' not in request.files:
        return "No file part", 400

    file = request.files['image']

    if file.filename == '':
        return "No selected file", 400

    try:
        image = Image.open(file)
        pdf = FPDF()
        pdf.add_page()
        # Guarda la imagen temporalmente para poder agregarla al PDF
        temp_image_path = f"/tmp/{file.filename}"
        image.save(temp_image_path)
        pdf.image(temp_image_path, x=10, y=10, w=100)
        
        # Guarda el PDF temporalmente
        pdf_output = f"/tmp/{file.filename}.pdf"
        pdf.output(pdf_output)
        
        # Envía el archivo PDF como respuesta
        return send_file(pdf_output, as_attachment=True, download_name=f"{file.filename}.pdf")

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=False)