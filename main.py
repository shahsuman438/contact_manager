import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

open_ai_key = os.getenv("OPEN_AI_KEY")

client = OpenAI(api_key=open_ai_key)


def get_completion(prompt, model="gpt-4o-mini", temperature=1):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


prompt = f"""
Generate a list of three made-up book titles along \
with their authors and genres.
Provide them in JSON format with the following keys:
book_id, title, author, genre.
"""
response = get_completion(prompt)
print(response)
