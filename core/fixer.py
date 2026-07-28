from core.router import Router


SYSTEM_PROMPT = """
You are an expert debugger.

Return ONLY corrected code.

No markdown.

No explanations.

No triple backticks.
"""


class Fixer:

    def __init__(self):

        self.router = Router()

    def fix(self, code, error):

        llm = self.router.code()

        reply = llm.chat([
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content":
f"""
Fix this code.

Code:

{code}

Error:

{error}
"""
            }
        ])

        fixed = reply.content.strip()

        if fixed.startswith("```"):

            lines = fixed.splitlines()

            if lines:
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines.pop()

            fixed = "\n".join(lines)

        return fixed
