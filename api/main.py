import cv2
import numpy as np
from fpdf import FPDF

def convert_image_to_pdf(image_file):
    try:
        # Leer la imagen
        image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        pdf = FPDF()
        pdf.add_page()
        img_buffer = cv2.imencode('.jpg', image)[1].tobytes()
        pdf.image(io.BytesIO(img_buffer), x=10, y=10, w=190)
        pdf_output = io.BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        return {
            "status": "success",
            "pdf": pdf_output.getvalue().hex()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Ejemplo de uso en FastAPI
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/convert-image")
async def api_convert_image_to_pdf(file: UploadFile = File(...)):
    return convert_image_to_pdf(await file.read())
