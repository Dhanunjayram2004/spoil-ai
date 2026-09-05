import json
import re
from core.llm import LLM
<<<<<<< HEAD
from core.model_manager import best_model
=======
from core.model_manager import best_model, installed_models
from core.registry import list_tools
>>>>>>> b1babbc (integrated rag pipeline)

class Planner:

    def __init__(self):
        models = installed_models()
        fast_model = next((m for m in models if "1.5b" in m or "3b" in m or "4b" in m), best_model())
        self.llm = LLM(model=fast_model)

    def plan(self, request):
<<<<<<< HEAD

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

=======
        user = request.lower().strip()

        # Smart Bypass - Skip the heavy AI entirely for basic greetings
        fast_chat_words = ["hi", "hello", "hey", "who are you", "what's up", "help"]
        if user in fast_chat_words:
            return {"action": "chat", "tool": "", "packages": [], "commands": []}

        available_tools = ""
        for name, tool_obj in list_tools().items():
            available_tools += f"- {name}: {tool_obj.description}\n"

	# core/planner.py lo prompt ni ila optimize cheyandi
	prompt = f"""
	Route user request to JSON.
	Schema: {{"action":"chat|run|tool", "tool":"", "packages":[], "commands":[]}}

	Available Tools:
	{available_tools}

	Rules:
	- Theory/Questions -> action: "chat"
	- System actions (IP, files, scans) -> action: "run"
	- Matching Custom Tool -> action: "tool"
	- Commands must be valid Linux (no sudo).

	User request: {request}
	"""	
        print("thinking...", end="\r", flush=True)

        messages = [
            {"role": "system", "content": "You are a JSON-only API. Output ONLY raw JSON. No conversational text. No markdown blocks."},
            {"role": "user", "content": prompt}
        ]

        reply = self.llm.chat(messages, temperature=0.0)
>>>>>>> b1babbc (integrated rag pipeline)
        text = reply.content.strip()

        print(" " * 20, end="\r", flush=True)

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
<<<<<<< HEAD

            return {
                "action": "chat",
                "packages": [],
                "commands": [],
                "message": reply.content,
            }
=======
            pass

        return {"action": "chat", "tool": "", "packages": [], "commands": []}
>>>>>>> b1babbc (integrated rag pipeline)
