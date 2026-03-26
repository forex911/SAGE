# services/vision.py
# SAGE AI — Groq Vision API Service

import httpx
from prompts import SYSTEM_PROMPT, CHAT_PROMPT
from utils.helpers import image_to_base64, get_image_mime_type, resize_image_if_needed

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def analyze_screenshot(
    image_bytes: bytes,
    file_name: str,
    api_key: str,
    model: str = "meta-llama/llama-4-scout-17b-16e-instruct",
) -> str:
    """Send screenshot to Groq Vision API for analysis."""
    if not image_bytes:
        raise ValueError("No image data provided.")

    image_bytes = resize_image_if_needed(image_bytes)
    b64_image = image_to_base64(image_bytes)
    mime_type = get_image_mime_type(file_name)
    image_data_url = f"data:{mime_type};base64,{b64_image}"

    payload = {
        "model": model,
        "max_tokens": 2048,
        "temperature": 0.2,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_data_url}},
                    {
                        "type": "text",
                        "text": SYSTEM_PROMPT + "\n\nAnalyze this screenshot now.",
                    },
                ],
            }
        ],
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = httpx.post(GROQ_API_URL, json=payload, headers=headers, timeout=60.0)

    if response.status_code != 200:
        error_msg = response.json().get("error", {}).get("message", response.text)
        raise Exception(f"Groq API error ({response.status_code}): {error_msg}")

    return response.json()["choices"][0]["message"]["content"]


def chat_followup(
    image_bytes: bytes,
    file_name: str,
    initial_analysis: str,
    chat_history: list,
    question: str,
    api_key: str,
    model: str = "meta-llama/llama-4-scout-17b-16e-instruct",
) -> str:
    """Send a follow-up question about a previously analyzed screenshot."""
    if not image_bytes:
        raise ValueError("No image data provided.")

    image_bytes = resize_image_if_needed(image_bytes)
    b64_image = image_to_base64(image_bytes)
    mime_type = get_image_mime_type(file_name)
    image_data_url = f"data:{mime_type};base64,{b64_image}"

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": image_data_url}},
                {
                    "type": "text",
                    "text": CHAT_PROMPT
                    + f"\n\nHere is my initial analysis:\n\n{initial_analysis}",
                },
            ],
        },
        {
            "role": "assistant",
            "content": "I have the screenshot and my analysis ready. What would you like to know?",
        },
    ]

    for msg in chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": question})

    payload = {
        "model": model,
        "max_tokens": 1024,
        "temperature": 0.3,
        "messages": messages,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = httpx.post(GROQ_API_URL, json=payload, headers=headers, timeout=60.0)

    if response.status_code != 200:
        error_msg = response.json().get("error", {}).get("message", response.text)
        raise Exception(f"Groq API error ({response.status_code}): {error_msg}")

    return response.json()["choices"][0]["message"]["content"]
