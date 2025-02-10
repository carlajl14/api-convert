from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
from fpdf import FPDF
from mangum import Mangum

app = FastAPI()

@app.post("/convert-image")
async def convert_image_to_pdf(file: UploadFile = File(...)):
    try:
        image = Image.open(io.BytesIO(await file.read()))
        pdf = FPDF()
        pdf.add_page()
        if image.mode != "RGB":
            image = image.convert("RGB")
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="JPEG")
        img_buffer.seek(0)
        pdf.image(img_buffer, x=10, y=10, w=190)
        pdf_output = io.BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        return {
            "status": "success",
            "pdf": pdf_output.getvalue().hex()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Para Vercel
import os
if "VERCEL" in os.environ:
    from mangum import Mangum
    handler = Mangum(app)
