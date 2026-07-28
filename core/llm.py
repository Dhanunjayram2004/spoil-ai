from openai import OpenAI
from pathlib import Path
from core.model_manager import best_model


class LLM:

    def __init__(
        self,
        model=None,
        base_url="http://localhost:11434/v1",
    ):

        if model is None:
            model = best_model()

        self.model = model

        self.client = OpenAI(
            base_url=base_url,
            api_key="ollama",
        )

        system_path = Path("prompts/system.txt")

        if system_path.exists():
            self.system_prompt = system_path.read_text(
                encoding="utf-8"
            )
        else:
            self.system_prompt = ""

    def chat(
        self,
        messages,
        tools=None,
        tool_choice="auto",
        temperature=0.2,
        stream=False,
    ):

        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
            *messages,
        ]

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
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

                        print(
                            delta.content,
                            end="",
                            flush=True,
                        )

                        full_response += delta.content

                print()

                return full_response

            except KeyboardInterrupt:

                print("\n\nInterrupted.")
                raise

        return response.choices[0].message
