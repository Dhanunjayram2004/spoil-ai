from core.llm import LLM
from core.model_manager import best_model

class Router:

    def __init__(self):

        self.models = {
            model=best_model()
            "chat": LLM(model=model),
            "code": LLM(model=model),
            "fast": LLM(model=model),
        }

    def chat(self):
        return self.models["chat"]

    def code(self):
        return self.models["code"]

    def fast(self):
        return self.models["fast"]
