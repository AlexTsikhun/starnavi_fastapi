import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def profanity_checker(text):
    prompt = f"Оціни, чи даний текст містить ненормативну лексику: {text}. Відповідай числом, 1 - якщо вона є чи 0 якщо немає"
    response = model.generate_content(prompt)
    return int(response.text)
