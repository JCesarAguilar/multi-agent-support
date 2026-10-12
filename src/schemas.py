"""
Contratos de datos del sistema (Pydantic).

Convierten el texto libre del LLM en objetos con tipos garantizados.
Si el LLM devuelve algo fuera del contrato, Pydantic lanza un error claro
en vez de dejar pasar un valor inválido.
"""

from typing import Literal, TypeAlias, get_args

from pydantic import BaseModel, Field

from src import config

# Intents válidos. Se escriben explícitos para que el verificador de tipos
# (Pylance/mypy) pueda analizarlos sin ejecutar el código.
Intent: TypeAlias = Literal["hr", "tech", "finance", "out_of_scope"]

# Verificación al importar: si alguien agrega un dominio en config.DOMAINS
# y olvida agregarlo aquí (o al revés), el programa falla de inmediato.
_expected = {*config.DOMAINS, config.OUT_OF_SCOPE}
if set(get_args(Intent)) != _expected:
    raise RuntimeError(
        f"Intent {set(get_args(Intent))} no coincide con config.DOMAINS {_expected}. "
        "Actualiza el Literal en schemas.py."
    )


class RoutingDecision(BaseModel):
    """Salida del orquestador: a qué agente enviar la consulta."""

    intent: Intent = Field(description="Área responsable de responder la consulta.")
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confianza en la clasificación, entre 0 y 1."
    )
    reasoning: str = Field(description="Justificación breve (una oración) de la elección.")


class Source(BaseModel):
    """Un chunk recuperado, para citar de dónde salió la respuesta."""

    source: str = Field(description="Archivo de origen, ej. reembolsos_y_gastos.md")
    section: str = Field(description="Sección del documento")
    score: float | None = Field(default=None, description="Similitud con la consulta (0-1)")


class AgentResponse(BaseModel):
    """Respuesta final del sistema para una consulta."""

    query: str
    intent: Intent
    answer: str
    sources: list[Source] = Field(default_factory=list)


class Evaluation(BaseModel):
    """Salida del agente evaluador (bonus): calidad de una respuesta."""

    score: int = Field(ge=1, le=10, description="Calidad global de 1 (pésima) a 10 (excelente).")
    reasoning: str = Field(description="Justificación breve del puntaje.")
