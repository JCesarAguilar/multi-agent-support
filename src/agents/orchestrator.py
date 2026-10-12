"""
Orquestador: clasifica la intención de la consulta del usuario.

No responde la consulta; solo decide qué agente especialista debe atenderla.
"""

from functools import lru_cache

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from src import config
from src.schemas import RoutingDecision
from src.tracing import get_langchain_handler


def _format_domains() -> str:
    """Convierte DOMAIN_DESCRIPTIONS en una lista para el prompt."""
    lines = [f'- "{name}": {desc}' for name, desc in config.DOMAIN_DESCRIPTIONS.items()]
    lines.append(f'- "{config.OUT_OF_SCOPE}": la consulta no corresponde a ninguna área.')
    return "\n".join(lines)


@lru_cache(maxsize=1)
def build_orchestrator():
    """Construye la cadena LCEL: prompt -> LLM con salida estructurada."""
    system_prompt = (config.PROMPTS_DIR / "orchestrator_system.txt").read_text(encoding="utf-8")

    prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", "{query}")]
    ).partial(domains=_format_domains())

    llm = ChatOpenAI(
        model=config.LLM_MODEL,
        api_key=SecretStr(config.OPENAI_API_KEY),
        reasoning_effort="none",
        temperature=config.LLM_TEMPERATURE,
    )

    return prompt | llm.with_structured_output(RoutingDecision)


def classify(query: str) -> RoutingDecision:
    """Clasifica una consulta y devuelve un RoutingDecision validado por Pydantic."""
    result = build_orchestrator().invoke(
        {"query": query},
        config={"callbacks": [get_langchain_handler()]},
    )
    if not isinstance(result, RoutingDecision):
        raise TypeError(f"Salida inesperada del orquestador: {type(result).__name__}")
    return result