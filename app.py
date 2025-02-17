from flask import Flask, request, jsonify
from PIL import Image
from fpdf import FPDF
import os

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_image_to_pdf():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        image = Image.open(file)
        pdf = FPDF()
        pdf.add_page()
        pdf.image(file, x=10, y=10, w=100)
        pdf_output = f"{file.filename}.pdf"
        pdf.output(pdf_output)
        return jsonify({"message": f"File converted to {pdf_output}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)