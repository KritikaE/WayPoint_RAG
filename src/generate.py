import os
from google import genai

API_KEY = os.getenv("waypoint")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not found.")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.6-flash"


def generate_answer(prompt):
    """Generate an answer using Gemini."""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    return response.text