from app.db.models import ChatMessage
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    def __init__(
        self,
        chat_repository: ChatMessageRepository,
        openrouter_client: OpenRouterClient,
    ) -> None:
        self._chat_repository = chat_repository
        self._openrouter_client = openrouter_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: str | None = None,
        max_history: int = 10,
        temperature: float = 0.7,
    ) -> str:
        messages: list[dict[str, str]] = []

        if system:
            messages.append(
                {
                    "role": "system",
                    "content": system,
                }
            )

        history = await self._chat_repository.get_last_messages(
            user_id=user_id,
            limit=max_history,
        )

        for message in history:
            messages.append(
                {
                    "role": message.role,
                    "content": message.content,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        answer = await self._openrouter_client.create_chat_completion(
            messages=messages,
            temperature=temperature,
        )

        await self._chat_repository.add_message(
            user_id=user_id,
            role="user",
            content=prompt,
        )
        await self._chat_repository.add_message(
            user_id=user_id,
            role="assistant",
            content=answer,
        )

        return answer

    async def get_history(
        self,
        user_id: int,
        limit: int = 20,
    ) -> list[ChatMessage]:
        return await self._chat_repository.get_last_messages(
            user_id=user_id,
            limit=limit,
        )

    async def clear_history(self, user_id: int) -> None:
        await self._chat_repository.delete_all_for_user(user_id)
