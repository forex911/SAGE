# vision.py
# Calls Groq API directly via HTTP — no SDK, no proxy issues

import httpx
from prompts import SYSTEM_PROMPT
from utils import image_to_base64, get_image_mime_type, resize_image_if_needed

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def analyze_screenshot(
    image_bytes: bytes,
    file_name: str,
    api_key: str,
    model: str = "meta-llama/llama-4-scout-17b-16e-instruct",
) -> str:
    """
    Send screenshot to Groq Vision API using a direct HTTP request.
    No SDK used — avoids all version/proxy compatibility issues.
    """
    if not image_bytes:
        raise ValueError("No image data provided.")

    # 1. Resize if needed
    image_bytes = resize_image_if_needed(image_bytes)

    # 2. Convert to base64 data URL
    b64_image = image_to_base64(image_bytes)
    mime_type = get_image_mime_type(file_name)
    image_data_url = f"data:{mime_type};base64,{b64_image}"

    # 3. Build request payload
    payload = {
        "model": model,
        "max_tokens": 2048,
        "temperature": 0.2,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": image_data_url},
                    },
                    {
                        "type": "text",
                        "text": SYSTEM_PROMPT + "\n\nAnalyze this screenshot now.",
                    },
                ],
            }
        ],
    }

    # 4. Send HTTP POST directly to Groq API
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = httpx.post(
        GROQ_API_URL,
        json=payload,
        headers=headers,
        timeout=60.0,
    )

    # 5. Handle errors
    if response.status_code != 200:
        error_msg = response.json().get("error", {}).get("message", response.text)
        raise Exception(f"Groq API error ({response.status_code}): {error_msg}")

    # 6. Return the response text
    return response.json()["choices"][0]["message"]["content"]