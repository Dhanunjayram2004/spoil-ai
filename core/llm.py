import os
from openai import OpenAI
from pathlib import Path
from core.model_manager import best_model

_MODEL_CACHE = None

def get_cached_model():
    global _MODEL_CACHE
    if _MODEL_CACHE is None:
        _MODEL_CACHE = best_model()
    return _MODEL_CACHE


class LLM:
    def __init__(self, model=None, base_url="http://localhost:11434/v1"):
        self.model = model or "qwen2.5-coder:7b"
        self.client = OpenAI(base_url=base_url, api_key="ollama")

        base_dir = Path(__file__).parent.parent
        system_path = base_dir / "prompts" / "system.txt"
         # core/llm.py lo self.system_prompt ni ila replace cheyandi
        self.system_prompt = "You are SPOIL, a fast Linux cybersecurity terminal assistant. Execute tool actions immediately or answer concisely."  
    def chat(self, messages, tools=None, tool_choice="auto", temperature=0.2, stream=False):
        messages = [{"role": "system", "content": self.system_prompt}, *messages]

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
            "max_tokens": 150,
            "extra_body": {"keep_alive": -1, "think": False},
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = tool_choice

        response = self.client.chat.completions.create(**kwargs)

        if stream:
            full_response = ""
            try:
                for chunk in response:
                    if not chunk.choices:
                        continue
                    delta = chunk.choices[0].delta
                    if delta.content:
                        print(delta.content, end="", flush=True)
                        full_response += delta.content
                print()
                return full_response
            except KeyboardInterrupt:
                print("\n[AI stopped by user]")
                return full_response

        return response.choices[0].message
