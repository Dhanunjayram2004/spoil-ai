from openai import OpenAI
from core.model_manager import best_model

model=best_model()
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

response = client.chat.completions.create(
    model=best_model(),
    messages=[
        {
            "role":"user",
            "content":"Say Hello Linux"
        }
    ]
)

print(response.choices[0].message.content)
