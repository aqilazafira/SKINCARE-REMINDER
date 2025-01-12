from ast import Bytes
import io
import os
from datetime import datetime as dt

from PIL import Image

UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__name__)) + "/app/static"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def compress_image(image_bytes: bytes) -> bytes:
    target_size = 640
    max_file_size = 100 * 1024

    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("RGB")

    # resize the image
    image.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)

    # Crop the image to a square
    width, height = image.size
    min_dim = min(width, height)
    left = (width - min_dim) / 2
    top = (height - min_dim) / 2
    right = (width + min_dim) / 2
    bottom = (height + min_dim) / 2
    image = image.crop((left, top, right, bottom))

    # Compress the image
    output = io.BytesIO()
    quality = 85
    while True:
        output.seek(0)
        image.save(output, format="JPEG", quality=quality)
        if output.tell() <= max_file_size or quality <= 10:
            break
        quality -= 5

    return output.getvalue()


def upload_image(image_bytes: Bytes, filename: str, path: str):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(f"{UPLOAD_FOLDER}/{path}", exist_ok=True)

    processed_image = compress_image(image_bytes)

    with open(f"{UPLOAD_FOLDER}/{path}/{filename}.jpg", "wb") as f:
        try:
            f.write(processed_image)
            print(f"File {filename} uploaded successfully")
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
