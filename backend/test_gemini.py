from backend.config import GEMINI_API_KEY, GEMINI_MODEL
from google import genai


client = genai.Client(
    api_key=GEMINI_API_KEY
)


response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents="Responda apenas: Gemini conectado ao Draco AI."
)


print(response.text)