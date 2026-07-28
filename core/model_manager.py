import json
import subprocess


PREFERRED_FAMILIES = [
    "deepseek-r1",
    "qwen3",
    "qwen2.5-coder",
    "qwen2.5",
    "llama3.3",
    "llama3.2",
    "gemma3",
    "mistral",
    "phi",
]


def installed_models():
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
        )

        lines = result.stdout.splitlines()[1:]

        models = []

        for line in lines:
            if not line.strip():
                continue

            name = line.split()[0]

            models.append(name)

        return models

    except Exception:
        return []


def score(model):

    model = model.lower()

    family_score = 0

    for i, family in enumerate(PREFERRED_FAMILIES):

        if family in model:
            family_score = 100 - i
            break

    size = 0

    import re

    m = re.search(r'(\d+)b', model)

    if m:
        size = int(m.group(1))

    return family_score * 1000 + size


def best_model():

    models = installed_models()

    if not models:
        raise RuntimeError(
             "No ollama Models  installed. Run 'ollama pull <model> ' first,"
    )

    return sorted(
        models,
        key=score,
        reverse=True,
    )[0]
