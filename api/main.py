from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
import os
from fpdf import FPDF

app = FastAPI()

@app.post("/convert-image")
async def convert_image_to_pdf(file: UploadFile = File(...)):
    try:
        # Leer la imagen desde el archivo subido
        image = Image.open(io.BytesIO(await file.read()))

        # Crear un archivo PDF
        pdf = FPDF()
        pdf.add_page()

        # Convertir la imagen a RGB si no lo está
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Guardar la imagen temporalmente
        temp_image_path = "temp_image.jpg"
        image.save(temp_image_path, format="JPEG")

        # Añadir la imagen al PDF
        pdf.image(temp_image_path, x=10, y=10, w=190)

        # Guardar el PDF en memoria
        pdf_output = io.BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)

        # Eliminar el archivo temporal
        os.remove(temp_image_path)

        # Retornar el PDF como respuesta
        return {
            "status": "success",
            "pdf": pdf_output.getvalue().hex()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Configuración para Vercel
if "VERCEL" in os.environ:
    from mangum import Mangum
    handler = Mangum(app)