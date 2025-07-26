from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pdf2image import convert_from_bytes
import tempfile
import os

app = FastAPI()

import base64
from io import BytesIO

@app.post("/pdf-to-images")
async def pdf_to_images(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    images = convert_from_bytes(pdf_bytes)
    
    # Convert each image to base64
    base64_images = []
    for i, img in enumerate(images):
        # Convert PIL image to base64
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        base64_images.append(img_base64)
    
    return {"images": base64_images, "num_pages": len(base64_images)}
