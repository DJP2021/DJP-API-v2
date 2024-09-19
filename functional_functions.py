
from openai import OpenAI
client = OpenAI(api_key="none",
    base_url="http://51.195.176.136:8150")

def llm_request(prompt):
    completion = client.chat.completions.create(
      model="mistral-7b-instruct-v0.3",
      messages=[
    {"role": "system", "content": "You are an assistant made to help your client."},
    {"role": "user", "content": prompt}
  ]
)

    return completion.choices[0].message.content