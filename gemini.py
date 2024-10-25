
import google.generativeai as genai

from settings import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def profanity_checker(text):
    prompt = (
        f"Оціни, чи даний текст містить ненормативну лексику: {text}."
        f"Якщо тобі недостатньо контексту, то найбільш імовірно, текст не містить ненормативну лексику"
        f" Відповідай числом, 1 - якщо вона є чи 0 якщо немає"
    )
    response = model.generate_content(prompt)
    return int(response.text)


def gemini_auto_reply(post_content, comment_content):
    prompt = (
        f"I published a social media post with the following content '{post_content}'"
        f" and received a '{comment_content}'. I want you to respond to the comment,"
        f" don't ask questions back. Your goal is to be friendly."
        f"If you have a problem with a understanding, just write 'thank you'."
        f"Answer in the language in which the question was asked "
    )
    response = model.generate_content(prompt)
    return response.text
