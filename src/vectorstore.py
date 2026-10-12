"""
Acceso a los vector stores de Chroma.

Una colección por dominio (hr, tech, finance) dentro del mismo directorio
persistido. Tanto la ingesta como los agentes usan esta función, así ambos
lados usan SIEMPRE el mismo modelo de embeddings y la misma métrica.
"""

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from pydantic import SecretStr

from src import config


def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=config.EMBEDDING_MODEL, api_key=SecretStr(config.OPENAI_API_KEY))


def get_vectorstore(domain: str) -> Chroma:
    """Devuelve la colección de Chroma de un dominio (la crea si no existe)."""
    if domain not in config.DOMAINS:
        raise ValueError(f"Dominio desconocido: {domain!r}. Válidos: {list(config.DOMAINS)}")

    return Chroma(
        collection_name=f"{domain}_docs",
        embedding_function=get_embeddings(),
        persist_directory=str(config.CHROMA_DIR),
        # Similitud coseno (por defecto Chroma usa distancia L2).
        collection_configuration={"hnsw": {"space": "cosine"}},
    )
