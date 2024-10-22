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


def gemini_auto_reply(post_content, comment_content):
    prompt = (
        f"I published a social media post with the following content '{post_content}'"
        f" and received a comment. I want you to respond to the comment, taking "
        f"into account its content and emotions. Your goal is to be friendly, "
        f"and provide helpful responses. "
        f"Here's the comment: '{comment_content}'. Answer in the language in which the question was asked "
    )
    response = model.generate_content(prompt)
    return response.text
