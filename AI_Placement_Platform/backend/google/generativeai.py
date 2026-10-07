_api_key = None

def configure(api_key=None):
    global _api_key
    _api_key = api_key


class _Response:
    def __init__(self, text: str):
        self.text = text


class _Model:
    def __init__(self, name: str):
        self.name = name


class GenerativeModel:
    def __init__(self, name: str):
        self.name = name

    def generate(self, *args, **kwargs):
        return {"candidates": [{"content": ""}], "metadata": {}}

    def generate_content(self, prompt, *args, **kwargs):
        text = (
            "Local stub response from "
            f"{self.name}. Configure a real GEMINI_API_KEY to get live answers.\n\n"
            f"Prompt preview:\n{str(prompt).strip()[:400]}"
        )
        return _Response(text)


def list_models():
    return [
        _Model("models/gemini-2.0-flash"),
        _Model("models/gemini-1.5-flash"),
    ]
