from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from PIL import Image
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

UPLOAD_FOLDER = "uploads"
REDUCED_FOLDER = "reduced"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REDUCED_FOLDER, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/compress")
async def compress_image(file: UploadFile = File(...)):
    # Save the uploaded image
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Compress the image
    output_path = os.path.join(REDUCED_FOLDER, f"compressed_{file.filename}")
    with Image.open(input_path) as img:
        img = img.convert("RGB")
        img.save(output_path, "JPEG", quality=50)  # Reduce quality to compress

    return FileResponse(output_path, media_type="image/jpeg", filename=f"compressed_{file.filename}")

@app.get("/")
def root():
    return {"message": "Image compression server is running!"} 