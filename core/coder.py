from core.router import Router


SYSTEM_PROMPT = """
You are an expert software engineer.

Return ONLY executable source code.

No markdown.

No explanations.

No triple backticks.

The program must be complete.

If writing a Python program, make it runnable without requiring user input unless the user explicitly asks for an interactive program.
"""


class Coder:

    def __init__(self):

        self.router = Router()

    def generate(self, task):

        llm = self.router.code()

        reply = llm.chat([
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": task,
            }
        ])

        code = reply.content.strip()

        if code.startswith("```"):

            lines = code.splitlines()

            if lines:
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines.pop()

            code = "\n".join(lines)

        return code
