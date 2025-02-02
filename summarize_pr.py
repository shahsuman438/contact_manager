import re
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

# Read the diff from the file
with open("code_diff.txt", "r", encoding="utf-8") as file:
    code_diff = file.readlines()

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
Generate the summarized PR Description with the following code mention in triple backticks and get the summary in following format and response in json
with key title:'Generate suatable PR Title' and body:'this should be markup text includes topics like summary(summarize the changes), changes(short description for each code file and code changes),screenshots('leave this blank just have heading') ,suggestion(suggest the improvements)', 
```{code_diff}```
"""

response = get_completion(prompt)
cleanedResponse = response.replace("`", "").replace("json", "")
responseJson = json.load(cleanedResponse)
with open("pr_summary.txt", "w", encoding="utf-8") as output_file:
    output_file.write(responseJson["body"])

with open("pr_title.txt", "w", encoding="utf-8") as output_file:
    output_file.write(responseJson["title"])

print(responseJson)
print(responseJson["body"])
print(responseJson["title"])
