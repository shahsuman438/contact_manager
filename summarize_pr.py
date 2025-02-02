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


def feed_and_get_content(prompt, model="gpt-4o-mini", temperature=1):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


prompt = f"""
Generate the summarized PR Description with the following code mention in triple backticks and get the summary in following format and response in json
with key title:'Generate suatable PR Title' and body:'this should be markup text includes topics like summary(summarize the changes), 
changes(short description for each code file and code changes),screenshots('leave this blank just have heading') ,
suggestion(suggest the improvements also include the code improvement), 
possible breakage(check for possible breakage of the code if there is then point out that code and suggestion to fix)',
 
```{code_diff}```
"""

response = feed_and_get_content(prompt)
cleaned_response = response.replace("`", "").replace("json", "")
try:
    responseJson = json.loads(cleaned_response) if isinstance(cleaned_response, str) else cleaned_response
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
