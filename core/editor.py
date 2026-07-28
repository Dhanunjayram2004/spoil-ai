from pathlib import Path

from core.llm import LLM


class Editor:

    def __init__(self):
        self.llm = LLM()

    def edit(self, filename, instruction):

        path = Path(filename)

        code = path.read_text(encoding="utf-8")

        prompt = f"""
You are editing an existing file.

Instruction:

{instruction}

Return ONLY the complete updated file.

Current file:

{code}
"""

        reply = self.llm.chat(
            [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

        path.write_text(reply.content, encoding="utf-8")

        return path
