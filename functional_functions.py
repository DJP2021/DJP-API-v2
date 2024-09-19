ai_model = "gpt-4o"
from openai import OpenAI
client = OpenAI(api_key="none",
    base_url="")

def llm_request(prompt):
    completion = client.chat.completions.create(
      model=ai_model,
      messages=[
    {"role": "system", "content": "You are an assistant made to help your client."},
    {"role": "user", "content": prompt}
  ]
)

    return completion.choices[0].message.content
