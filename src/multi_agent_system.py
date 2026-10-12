"""
Sistema multiagente: orquestador -> agente especialista -> respuesta.

Uso:
    python -m src.multi_agent_system "¿Cuántos días de vacaciones me tocan?"
"""

import sys

from src import config
from src.agents.finance_agent import finance_agent
from src.agents.hr_agent import hr_agent
from src.agents.orchestrator import classify
from src.agents.rag_agent import RAGAgent
from src.agents.tech_agent import tech_agent
from src.schemas import AgentResponse

# Registro de agentes: intent -> agente que lo atiende.
AGENTS: dict[str, RAGAgent] = {
    "hr": hr_agent,
    "tech": tech_agent,
    "finance": finance_agent,
}

OUT_OF_SCOPE_MESSAGE = (
    "Lo siento, solo puedo ayudarte con consultas de Recursos Humanos, "
    "Mesa de Ayuda de TI y Finanzas de Andina Obras. "
    "Para otros temas, consulta con el área correspondiente."
)


def handle_query(query: str) -> AgentResponse:
    """Clasifica la consulta y la delega al agente correspondiente."""
    decision = classify(query)

    if decision.intent == config.OUT_OF_SCOPE:
        return AgentResponse(query=query, intent=decision.intent, answer=OUT_OF_SCOPE_MESSAGE)

    agent = AGENTS[decision.intent]
    return agent.answer(query)


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "¿Cuántos días de vacaciones me tocan?"
    response = handle_query(question)
    print(f"Consulta : {response.query}")
    print(f"Área     : {response.intent}")
    print(f"Respuesta: {response.answer}")
    for source in response.sources:
        print(f"  - {source.source} > {source.section} ({source.score})")