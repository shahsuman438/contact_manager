import re
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

with open("code_diff.txt", "r", encoding="utf-8") as file:
    code_diff = file.readlines()

load_dotenv()

open_ai_key = os.getenv("OPEN_AI_KEY")

client = OpenAI(api_key=open_ai_key)


def feed_and_get_content(prompt, model="gpt-4o-mini", temperature=1):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


prompt = f"""
Generate a summarized PR description based on the provided code snippet. The response should be in JSON format with the following keys:
    title: A suitable PR title.
    body: A structured markdown text including:
        Summary: A concise overview of the changes.
        Changes: A breakdown of modifications per file, describing key updates.
        Screenshots: (Leave this blank, just include the heading.)
        Suggestions: Recommendations for improvements, including potential code enhancements.
        Possible Breakage: Identify any potential code-breaking changes and suggest fixes.
        The code snippet will be enclosed within triple backticks.
```{code_diff}```
"""

response = feed_and_get_content(prompt)
cleaned_response = response.replace("`", "").replace("json", "")
try:
    responseJson = (
        json.loads(cleaned_response)
        if isinstance(cleaned_response, str)
        else cleaned_response
    )
except json.JSONDecodeError as e:
    print(f"Failed to decode JSON: {e}")
    raise

with open("pr_summary.txt", "w", encoding="utf-8") as output_file:
    output_file.write(responseJson["body"])

with open("pr_title.txt", "w", encoding="utf-8") as output_file:
    output_file.write(responseJson["title"])

print(responseJson)
print(responseJson["body"])
print(responseJson["title"])
