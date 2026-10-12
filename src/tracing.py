"""
Configuración de Langfuse (v4).

Un único cliente para todo el proyecto. Las llamadas a LangChain se registran
como "generations" mediante el CallbackHandler.
"""

from functools import lru_cache

from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

from src import config


@lru_cache(maxsize=1)
def get_langfuse() -> Langfuse:
    """Crea (una sola vez) el cliente de Langfuse con las claves del .env."""
    return Langfuse(
        public_key=config.LANGFUSE_PUBLIC_KEY,
        secret_key=config.LANGFUSE_SECRET_KEY,
        base_url=config.LANGFUSE_HOST,
    )


@lru_cache(maxsize=1)
def get_langchain_handler() -> CallbackHandler:
    """Handler que registra cada llamada de LangChain al LLM como una generation."""
    get_langfuse()  # asegura que el cliente exista antes de crear el handler
    return CallbackHandler()