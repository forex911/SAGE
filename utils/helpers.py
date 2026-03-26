# utils/helpers.py
# SAGE AI — Utility Functions

import base64
import io
import os
import re
from pathlib import Path
from PIL import Image

try:
    import markdown

    def md_to_html(text: str) -> str:
        """Convert markdown text to HTML using the markdown library."""
        return markdown.markdown(
            text, extensions=["fenced_code", "tables", "nl2br", "sane_lists"]
        )

except ImportError:

    def md_to_html(text: str) -> str:
        """Fallback: basic markdown-to-HTML conversion."""
        import html as html_lib

        text = html_lib.escape(text)
        text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"`(.*?)`", r"<code>\1</code>", text)
        text = re.sub(r"^### (.*?)$", r"<h3>\1</h3>", text, flags=re.MULTILINE)
        text = re.sub(r"^## (.*?)$", r"<h2>\1</h2>", text, flags=re.MULTILINE)
        text = re.sub(r"^# (.*?)$", r"<h1>\1</h1>", text, flags=re.MULTILINE)
        text = re.sub(
            r"^&gt; (.*?)$", r"<blockquote>\1</blockquote>", text, flags=re.MULTILINE
        )
        text = text.replace("\n", "<br>")
        return text


def image_to_base64(image_bytes: bytes) -> str:
    """Convert raw image bytes to a base64-encoded string."""
    return base64.b64encode(image_bytes).decode("utf-8")


def get_image_mime_type(file_name: str) -> str:
    """Determine the MIME type from file extension."""
    ext = Path(file_name).suffix.lower()
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return mime_map.get(ext, "image/jpeg")


def resize_image_if_needed(image_bytes: bytes, max_size_mb: float = 4.0) -> bytes:
    """Resize image if it exceeds the max size limit."""
    size_mb = len(image_bytes) / (1024 * 1024)
    if size_mb <= max_size_mb:
        return image_bytes

    img = Image.open(io.BytesIO(image_bytes))
    scale_factor = (max_size_mb / size_mb) ** 0.5
    new_width = int(img.width * scale_factor)
    new_height = int(img.height * scale_factor)
    img = img.resize((new_width, new_height), Image.LANCZOS)

    output = io.BytesIO()
    img_format = img.format or "PNG"
    img.save(output, format=img_format)
    return output.getvalue()


def format_file_size(size_bytes: int) -> str:
    """Return a human-readable file size string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 ** 2):.1f} MB"


def extract_code_blocks(text: str) -> list:
    """Extract fenced code blocks from markdown text."""
    pattern = r"```(\w*)\n(.*?)```"
    blocks = re.findall(pattern, text, re.DOTALL)
    return [{"language": lang or "text", "code": code.strip()} for lang, code in blocks]
