import openai

from .client_factory import OpenAIClientFactory
from .settings import OpenAIAPISettings


class OpenAIRepository:
    def __init__(self, client: openai.ChatCompletion = OpenAIClientFactory.get_client()):  # type: ignore
        self.client = client
        self.settings = OpenAIAPISettings()

    def _send_request(self, model: str, prompt: str, max_tokens: int = 60):
        return self.client.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )

    def text_prompt(self, prompt: str, max_tokens: int = 100):
        response = self._send_request(
            model=self.settings.MODEL, prompt=prompt, max_tokens=max_tokens
        )
        return dict(response["choices"][0])["message"]["content"]  # type: ignore
