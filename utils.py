# utils.py
# Helper functions for the AI Screenshot Explainer

import base64
import os
from pathlib import Path
from PIL import Image
import io


# Ensure the uploads directory exists
def ensure_uploads_dir():
    """Create the uploads/ directory if it doesn't exist."""
    Path("uploads").mkdir(exist_ok=True)


def image_to_base64(image_bytes: bytes) -> str:
    """
    Convert raw image bytes to a base64-encoded string.
    This is required by the OpenAI vision API.
    """
    return base64.b64encode(image_bytes).decode("utf-8")


def get_image_mime_type(file_name: str) -> str:
    """
    Determine the MIME type from the file extension.
    Defaults to jpeg if unknown.
    """
    ext = Path(file_name).suffix.lower()
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return mime_map.get(ext, "image/jpeg")


def save_uploaded_image(image_bytes: bytes, file_name: str) -> str:
    """
    Save the uploaded image to the uploads/ directory.
    Returns the path where the file was saved.
    """
    ensure_uploads_dir()
    save_path = os.path.join("uploads", file_name)
    with open(save_path, "wb") as f:
        f.write(image_bytes)
    return save_path


def resize_image_if_needed(image_bytes: bytes, max_size_mb: float = 4.0) -> bytes:
    """
    Resize image if it exceeds the max size limit (in MB).
    OpenAI has a ~20MB limit, but we keep it well under for speed.
    Returns the (possibly resized) image bytes.
    """
    size_mb = len(image_bytes) / (1024 * 1024)
    if size_mb <= max_size_mb:
        return image_bytes  # No resizing needed

    # Open image with Pillow and scale it down
    img = Image.open(io.BytesIO(image_bytes))
    scale_factor = (max_size_mb / size_mb) ** 0.5  # Approximate scaling
    new_width = int(img.width * scale_factor)
    new_height = int(img.height * scale_factor)
    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Save back to bytes
    output = io.BytesIO()
    img_format = img.format or "PNG"
    img.save(output, format=img_format)
    return output.getvalue()


def format_file_size(size_bytes: int) -> str:
    """Return a human-readable file size string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 ** 2):.1f} MB"
