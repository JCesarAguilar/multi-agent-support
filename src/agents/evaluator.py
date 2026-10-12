"""
Agente evaluador (bonus): puntúa la calidad de cada respuesta del sistema (LLM-as-a-judge).
"""

from functools import lru_cache

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from src import config
from src.schemas import AgentResponse, Evaluation
from src.tracing import get_langchain_handler


@lru_cache(maxsize=1)
def build_evaluator():
    """Construye la cadena LCEL: prompt -> LLM con salida estructurada (Evaluation)."""
    system_prompt = (config.PROMPTS_DIR / "evaluator_system.txt").read_text(encoding="utf-8")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "Consulta del colaborador:\n{query}\n\nRespuesta del asistente:\n{answer}"),
        ]
    )

    llm = ChatOpenAI(
        model=config.LLM_MODEL,
        api_key=SecretStr(config.OPENAI_API_KEY),
        reasoning_effort="none",
        temperature=config.LLM_TEMPERATURE,
    )

    return prompt | llm.with_structured_output(Evaluation)


def evaluate(response: AgentResponse) -> Evaluation:
    """Evalúa la respuesta final del sistema para su consulta original."""
    result = build_evaluator().invoke(
        {"query": response.query, "answer": response.answer},
        config={"callbacks": [get_langchain_handler()]},
    )
    if not isinstance(result, Evaluation):
        raise TypeError(f"Salida inesperada del evaluador: {type(result).__name__}")
    return result