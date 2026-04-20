from typing import Any

import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    def __init__(self) -> None:
        self._base_url = settings.openrouter_base_url.rstrip("/")
        self._api_key = settings.openrouter_api_key
        self._model = settings.openrouter_model
        self._referer = settings.openrouter_referer
        self._title = settings.openrouter_title

    async def create_chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
    ) -> str:
        url = f"{self._base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "HTTP-Referer": self._referer,
            "X-Title": self._title,
            "Content-Type": "application/json",
        }
        payload = {
            "model": self._model,
            "messages": messages,
            "temperature": temperature,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    url,
                    headers=headers,
                    json=payload,
                )
        except httpx.HTTPError as exc:
            raise ExternalServiceError(
                "Failed to connect to OpenRouter"
            ) from exc

        if response.status_code >= 400:
            raise ExternalServiceError(
                f"OpenRouter returned error {response.status_code}: {response.text}"
            )

        data: dict[str, Any] = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ExternalServiceError(
                "Invalid response format from OpenRouter"
            ) from exc