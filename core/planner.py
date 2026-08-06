import json
import re
from core.llm import LLM
from core.model_manager import best_model
from core.registry import list_tools

class Planner:
    def __init__(self):
        self.llm = LLM(model=best_model())

    def plan(self, request):
        user = request.lower().strip()

        # 1. Dynamically load all available tools from plugins
        available_tools = ""
        for name, tool_obj in list_tools().items():
            available_tools += f"- {name}: {tool_obj.description}\n"

        prompt = f"""
You are the planning brain of SPOIL.
Return ONLY ONE valid JSON object.
Never explain.

Schema:
{{
    "action":"chat|run|tool",
    "tool": "",
    "packages":[],
    "commands":[]
}}

Available Custom Tools (for action="tool"):
{available_tools}

Rules:
1. If an Available Custom Tool perfectly matches the user request, set action to "tool" and put its name in "tool".
2. If the user wants to execute Linux commands directly, set action to "run".
3. If the Linux command requires an external package (e.g., nmap, cowsay, neofetch), YOU MUST include it in the "packages" array.
4. packages contains apt package names ONLY.
5. commands contains Linux commands. NO sudo.
6. If the user just wants to chat, action is "chat".

Examples:
User: scan my network
Output: {{"action":"tool", "tool":"network_scan", "packages":[], "commands":[]}}

User: show system info with cool ascii
Output: {{"action":"run", "tool":"", "packages":["neofetch"], "commands":["neofetch"]}}

User request:
{request}
"""
        reply = self.llm.chat([{"role": "user", "content": prompt}])
        text = reply.content.strip()

        try:
            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception:
            pass
            
        return {"action": "chat", "tool": "", "packages": [], "commands": []}
