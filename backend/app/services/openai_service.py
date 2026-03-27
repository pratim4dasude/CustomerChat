from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from app.config import settings
from typing import List, Dict, Any, Optional, Union


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.embedding_model = settings.openai_embedding_model

    def get_embedding(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    def generate_chat_response(
        self,
        user_message: str,
        context_items: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        system_message = """You are CustomerChat, an internal IT support assistant.

Your role is to help users with their IT-related questions using ONLY the provided knowledge items.
If the answer cannot be found in the provided knowledge items, politely state that you are not sure 
and suggest the user contact IT support for further assistance.

Be helpful, concise, and professional in your responses."""

        context_section = self._build_context_section(context_items)
        
        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_message},
            {"role": "system", "content": f"\n\nKnowledge Base Context:\n{context_section}"}
        ]

        if conversation_history:
            for msg in conversation_history[-6:]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        messages.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content or ""

    def _build_context_section(self, items: List[Dict[str, Any]]) -> str:
        if not items:
            return "No relevant knowledge items found."

        context_parts = []
        for i, item in enumerate(items, 1):
            title = item.get("title", "Untitled")
            content = item.get("content", "")
            category = item.get("category", "General")
            
            truncated_content = content[:1500] + "..." if len(content) > 1500 else content
            
            context_parts.append(
                f"[Item {i}] Category: {category}\n"
                f"Title: {title}\n"
                f"Content: {truncated_content}"
            )

        return "\n\n---\n\n".join(context_parts)


openai_service = OpenAIService()
