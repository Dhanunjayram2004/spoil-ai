import json
import re
from core.llm import LLM
from core.model_manager import best_model

class Planner:

    def __init__(self):
        self.llm = LLM(model=best_model())

    def plan(self, request):

        prompt = f"""
You are the planning brain of SPOIL.

Return ONLY ONE valid JSON object.

Never use markdown.
Never use ```json.
Never explain.
Never wrap the JSON.

Schema:

{{
    "action":"",
    "packages":[],
    "commands":[],
    "message":""
}}

Rules:

1. action is either:
   - "chat"
   - "run"

2. packages contains apt package names ONLY.

3. commands contains Linux commands in execution order.

4. NEVER include "sudo" in any command.
NEVER output commands beginning with sudo.

NEVER include sudo anywhere.

The agent will automatically decide whether sudo is required.

If you output sudo, your answer is invalid.
5. Return normal Linux commands only.

6. The agent will decide whether sudo is required.

7. If the task needs Linux tools, decide which packages are required.

8. If no extra package is required, packages must be [].

Examples

User:
show my ip

Output:
{{
    "action":"run",
    "packages":[],
    "commands":[
        "ip addr"
    ],
    "message":""
}}

User:
scan my network

Output:
{{
    "action":"run",
    "packages":["nmap"],
    "commands":[
        "nmap -sn $(ip route | awk '/src/ {{print $1}}')"
    ],
    "message":""
}}

User:
capture packets

Output:
{{
    "action":"run",
    "packages":["tcpdump"],
    "commands":[
        "sudo tcpdump -i any"
    ],
    "message":""
}}

User:
inspect wifi

Output:
{{
    "action":"run",
    "packages":["aircrack-ng"],
    "commands":[
        "airmon-ng"
    ],
    "message":""
}}

User:
hello

Output:
{{
    "action":"chat",
    "packages":[],
    "commands":[],
    "message":"Hello!"
}}

User request:

{request}
"""

        reply = self.llm.chat(
            [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

        text = reply.content.strip()

        try:

            if text.startswith("```"):
                text = text.replace("```json", "")
                text = text.replace("```", "")
                text = text.strip()

            match = re.search(r"\{.*\}", text, re.DOTALL)

            if match:
                text = match.group(0)

            return json.loads(text)

        except Exception:

            return {
                "action": "chat",
                "packages": [],
                "commands": [],
                "message": reply.content,
            }
