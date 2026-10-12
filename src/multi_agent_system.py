"""
Sistema multiagente: orquestador -> agente especialista -> respuesta.

Uso:
    python -m src.multi_agent_system "¿Cuántos días de vacaciones me tocan?"
"""

import sys

from langfuse import propagate_attributes

from src import config
from src.agents.finance_agent import finance_agent
from src.agents.hr_agent import hr_agent
from src.agents.orchestrator import classify
from src.agents.rag_agent import RAGAgent
from src.agents.tech_agent import tech_agent
from src.schemas import AgentResponse
from src.tracing import get_langfuse

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


def handle_query(
    query: str,
    user_id: str = "demo-user",
    session_id: str | None = None,
    tags: list[str] | None = None,
) -> AgentResponse:
    """Clasifica la consulta, la delega al agente correspondiente y lo traza en Langfuse."""
    langfuse = get_langfuse()

    # Observación raíz = el Trace de esta consulta.
    with langfuse.start_as_current_observation(
        name="support-request", as_type="span", input={"query": query}
    ) as root:
        # Atributos de nivel trace: se aplican a todo lo que se cree dentro.
        with propagate_attributes(
            user_id=user_id,
            session_id=session_id,
            tags=["multi-agent-support", *(tags or [])],
        ):
            # Span del orquestador
            with langfuse.start_as_current_observation(
                name="orchestrator-routing", as_type="span", input={"query": query}
            ) as span:
                decision = classify(query)
                span.update(output=decision.model_dump())

            if decision.intent == config.OUT_OF_SCOPE:
                response = AgentResponse(
                    query=query, intent=decision.intent, answer=OUT_OF_SCOPE_MESSAGE
                )
            else:
                # Span del agente especialista: el nombre indica a quién se enrutó.
                with langfuse.start_as_current_observation(
                    name=f"{decision.intent}-agent", as_type="agent", input={"query": query}
                ) as span:
                    response = AGENTS[decision.intent].answer(query)
                    span.update(output={"answer": response.answer})

        root.update(output=response.model_dump())

    return response


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "¿Cuántos días de vacaciones me tocan?"
    response = handle_query(question)
    print(f"Consulta : {response.query}")
    print(f"Área     : {response.intent}")
    print(f"Respuesta: {response.answer}")
    for source in response.sources:
        print(f"  - {source.source} > {source.section} ({source.score})")
    get_langfuse().flush()