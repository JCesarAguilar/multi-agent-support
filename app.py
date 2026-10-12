import time
import uuid
from typing import Literal

import streamlit as st

from src.multi_agent_system import handle_query
from src.schemas import AgentResponse

st.set_page_config(page_title="Soporte interno · Andina Obras", page_icon="🏗️")

# Colores que acepta st.badge y que usamos en la app
BadgeColor = Literal["blue", "violet", "green", "gray"]

# Cómo se muestra cada área: nombre, color de la etiqueta e ícono
AREAS: dict[str, tuple[str, BadgeColor, str]] = {
    "hr": ("Recursos Humanos", "blue", ":material/groups:"),
    "tech": ("Mesa de Ayuda de TI", "violet", ":material/computer:"),
    "finance": ("Finanzas", "green", ":material/payments:"),
    "out_of_scope": ("Fuera de alcance", "gray", ":material/block:"),
}

# Consultas de ejemplo: priorizan los casos ambiguos, que son los más interesantes
EJEMPLOS = [
    "Compré unos guantes de seguridad con mi plata porque no había en almacén, ¿me lo devuelven?",
    "Me depositaron menos de lo normal este mes, ¿a quién reclamo?",
    "En Andina360 mi saldo de vacaciones aparece con menos días de los que tengo",
    "no me agarra la huella en el reloj de la obra",
    "¿Cómo calculo el volumen de concreto para una losa?",
]

MAX_CONSULTAS = 10  # por visita, para limitar el costo de la API
REPO_URL = "https://github.com/JCesarAguilar/multi-agent-support"

st.title("Asistente de soporte interno")
st.caption("Un orquestador enruta tu consulta al agente de RR. HH., TI o Finanzas.")

# Memoria de la visita: sobrevive a cada re-ejecución del script
if "historial" not in st.session_state:
    st.session_state.historial = []
    st.session_state.session_id = str(uuid.uuid4())


def mostrar_respuesta(respuesta: AgentResponse, segundos: float) -> None:
    nombre, color, icono = AREAS[respuesta.intent]
    st.badge(nombre, icon=icono, color=color)
    st.markdown(respuesta.answer)

    if respuesta.sources:
        with st.expander(f"Fuentes consultadas ({len(respuesta.sources)})"):
            for fuente in respuesta.sources:
                similitud = f"{fuente.score:.2f}" if fuente.score is not None else "—"
                st.markdown(f"**{fuente.section}**  \n`{fuente.source}` · similitud {similitud}")

    if respuesta.evaluation:
        e = respuesta.evaluation
        with st.expander(f"Evaluación de calidad: {e.score}/10"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Relevancia", f"{e.relevance}/10")
            col2.metric("Completitud", f"{e.completeness}/10")
            col3.metric("Precisión", f"{e.accuracy}/10")
            st.caption(e.reasoning)

    st.caption(f"Respondido en {segundos:.1f} s")


# Panel lateral
ejemplo = None
with st.sidebar:
    st.header("Andina Obras S.A.C.")
    st.write(
        "Constructora peruana **ficticia**. Pregunta como lo haría un colaborador: "
        "el sistema decide qué área debe responder."
    )

    st.subheader("Prueba un ejemplo")
    for texto in EJEMPLOS:
        if st.button(texto, width="stretch"):
            ejemplo = texto

    st.divider()
    evaluar = st.toggle("Evaluar la calidad de cada respuesta", value=True)
    st.caption(f"Consultas usadas: {len(st.session_state.historial)} de {MAX_CONSULTAS}")
    st.markdown(f"[Ver el código en GitHub]({REPO_URL})")


# 1. Volver a dibujar la conversación anterior
for pregunta_previa, respuesta_previa, segundos_previos in st.session_state.historial:
    with st.chat_message("user"):
        st.write(pregunta_previa)
    with st.chat_message("assistant"):
        mostrar_respuesta(respuesta_previa, segundos_previos)

# 2. Procesar la consulta nueva (escrita o elegida en un ejemplo)
limite_alcanzado = len(st.session_state.historial) >= MAX_CONSULTAS
pregunta = st.chat_input("Escribe tu consulta...", disabled=limite_alcanzado) or ejemplo

if limite_alcanzado:
    st.info("Llegaste al límite de consultas de esta demo. ¡Gracias por probarla!")
elif pregunta:
    with st.chat_message("user"):
        st.write(pregunta)
    with st.chat_message("assistant"):
        with st.spinner("Analizando tu consulta..."):
            inicio = time.perf_counter()
            respuesta = handle_query(
                pregunta,
                user_id="streamlit-demo",
                session_id=st.session_state.session_id,
                tags=["streamlit"],
                run_evaluation=evaluar,
            )
            segundos = time.perf_counter() - inicio
        mostrar_respuesta(respuesta, segundos)
    st.session_state.historial.append((pregunta, respuesta, segundos))
    st.rerun()