from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pdf2image import convert_from_bytes
import tempfile
import os

app = FastAPI()

@app.post("/pdf-to-images")
async def pdf_to_images(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    images = convert_from_bytes(pdf_bytes)
    image_paths = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for i, img in enumerate(images):
            path = os.path.join(tmpdir, f"page_{i+1}.png")
            img.save(path, "PNG")
            image_paths.append(path)
        # For demo: return number of images/pages
        return JSONResponse({"num_pages": len(image_paths)})