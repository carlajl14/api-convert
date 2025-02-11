from flask import Flask, request, send_file
import img2pdf
import os

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_images_to_pdf():
    # Crear un archivo temporal para el PDF
    pdf_path = "output.pdf"
    
    # Obtener las imágenes del request
    images = request.files.getlist("images")
    image_paths = []
    
    for image in images:
        path = os.path.join("/tmp", image.filename)
        image.save(path)
        image_paths.append(path)

    # Convertir imágenes a PDF
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(image_paths))
    
    # Enviar el archivo PDF generado
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)