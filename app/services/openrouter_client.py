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
        if not self._api_key:
            raise ExternalServiceError("OPENROUTER_API_KEY is not set")

        url = f"{self._base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "HTTP-Referer": self._referer,
            "X-OpenRouter-Title": self._title,
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
                f"Failed to connect to OpenRouter: {exc}"
            ) from exc

        if response.status_code >= 400:
            raise ExternalServiceError(
                f"OpenRouter returned error {response.status_code}: "
                f"{response.text}"
            )

        try:
            data: dict[str, Any] = response.json()
        except ValueError as exc:
            raise ExternalServiceError(
                "OpenRouter returned invalid JSON"
            ) from exc

        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ExternalServiceError(
                "Invalid response format from OpenRouter"
            ) from exc

        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):
            text_parts: list[str] = []

            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text = item.get("text")
                    if isinstance(text, str) and text.strip():
                        text_parts.append(text.strip())

            if text_parts:
                return "\n".join(text_parts)

        raise ExternalServiceError(
            "OpenRouter response does not contain text content"
        )
