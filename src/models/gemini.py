import google.generativeai as genai


class GeminiLLM:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.api_key = api_key

    def generate_content(self, prompt: str, model_name: str = "gemini-2.5-flash"):
        model = genai.GenerativeModel(model_name)
        return model.generate_content(prompt)
