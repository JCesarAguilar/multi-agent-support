"""
Configuración central del proyecto.

Único lugar donde se leen variables de entorno y se definen parámetros.
El resto del código importa desde aquí, nunca llama a os.environ directamente.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Rutas del proyecto
# ---------------------------------------------------------------------------
# Path(__file__) = .../multi-agent-support/src/config.py
# .parent        = .../multi-agent-support/src
# .parent.parent = .../multi-agent-support  (raíz del proyecto)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"          # vector store persistido (en .gitignore)
TEST_QUERIES_PATH = PROJECT_ROOT / "test_queries.json"

# Cargar el .env de la raíz del proyecto, sin importar desde dónde se ejecute
# (notebook, terminal o tests).
load_dotenv(PROJECT_ROOT / ".env")

# ---------------------------------------------------------------------------
# Dominios: una entrada por agente especialista
# ---------------------------------------------------------------------------
# La clave es el "intent" que devuelve el orquestador; el valor, la carpeta con
# su base de conocimiento. Agregar un agente nuevo = agregar una línea aquí.
DOMAINS: dict[str, Path] = {
    "hr": DATA_DIR / "hr_docs",
    "tech": DATA_DIR / "tech_docs",
    "finance": DATA_DIR / "finance_docs",
}

# Intent para consultas que ningún agente debe responder.
OUT_OF_SCOPE = "out_of_scope"

# ---------------------------------------------------------------------------
# Modelos (se pueden cambiar desde el .env sin tocar código)
# ---------------------------------------------------------------------------
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-5.4-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Temperatura 0: queremos respuestas consistentes, no creativas.
# Clasificar y responder políticas son tareas deterministas.
LLM_TEMPERATURE = 0.0

# ---------------------------------------------------------------------------
# Parámetros de RAG
# ---------------------------------------------------------------------------
# Chunking por sección "## " del Markdown; si una sección es muy larga,
# se subdivide con este tamaño máximo (en caracteres) y solapamiento.
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 150

# Cuántos chunks recupera cada agente por consulta.
TOP_K = 3

# ---------------------------------------------------------------------------
# Credenciales
# ---------------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", "")
# La consigna usa LANGFUSE_HOST. En Langfuse v4 el nombre nuevo es
# LANGFUSE_BASE_URL; aceptamos ambos y lo pasamos explícito al cliente.
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST") or os.getenv(
    "LANGFUSE_BASE_URL", "https://cloud.langfuse.com"
)

# Valores de ejemplo de .env.example: si siguen así, la clave no está configurada.
_PLACEHOLDERS = {"", "your-key-here", "pk-lf-xxx", "sk-lf-xxx"}


def validate_config(require_langfuse: bool = True) -> None:
    """
    Verifica que las credenciales necesarias estén configuradas.

    Falla rápido (fail-fast) con un mensaje claro, en vez de dejar que el error
    aparezca después como un 401 confuso en medio de una llamada a la API.
    Nunca imprime los valores de las claves.
    """
    required = {"OPENAI_API_KEY": OPENAI_API_KEY}
    if require_langfuse:
        required["LANGFUSE_PUBLIC_KEY"] = LANGFUSE_PUBLIC_KEY
        required["LANGFUSE_SECRET_KEY"] = LANGFUSE_SECRET_KEY

    missing = [name for name, value in required.items() if value.strip() in _PLACEHOLDERS]
    if missing:
        raise EnvironmentError(
            "Faltan variables de entorno o tienen valores de ejemplo: "
            + ", ".join(missing)
            + ". Revisa tu archivo .env (usa .env.example como guía)."
        )

    missing_dirs = [str(path) for path in DOMAINS.values() if not path.is_dir()]
    if missing_dirs:
        raise FileNotFoundError(f"No existen las carpetas de documentos: {missing_dirs}")
