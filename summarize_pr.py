import re
import os
from dotenv import load_dotenv
from openai import OpenAI

# Read the diff from the file
with open("code_diff.txt", "r", encoding="utf-8") as file:
    code_diff = file.readlines()

# Extract changed files and modifications
# changed_files = set()
# summary = []

# for line in code_diff:
#     if line.startswith("diff --git"):
#         file_name = re.findall(r"b/(.*)", line)
#         if file_name:
#             changed_files.add(file_name[0])
#     elif line.startswith("+") and not line.startswith("+++"):
#         summary.append(f"🟢 Added: {line.strip()}")
#     elif line.startswith("-") and not line.startswith("---"):
#         summary.append(f"🔴 Removed: {line.strip()}")

# # Format summary
# summary_text = f"**Changed Files:** {', '.join(changed_files)}\n\n"
# summary_text += "\n".join(summary[:10])  # Limit to 10 changes for readability

# # Save summary to a file
# with open("pr_summary.txt", "w", encoding="utf-8") as output_file:
#     output_file.write(summary_text)

# print("✅ PR Summary Generated!")

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
Generate the summarized PR Description with the following code mention in triple backticks differents and get the summary in following format
1. heading
2. description of changes
```{code_diff}```
"""

response = get_completion(prompt)

with open("pr_summary.txt", "w", encoding="utf-8") as output_file:
    output_file.write(response)

print(response)
