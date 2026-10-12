"""
Pipeline de ingesta (offline): documentos .md -> chunks -> embeddings -> Chroma.

Uso:
    python -m src.ingest            # construye (o reconstruye) los 3 índices
    python -m src.ingest --dry-run  # solo muestra los chunks, sin llamar a OpenAI
"""

import argparse
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from src import config

# 1) Cortar por títulos del Markdown: "#" = título del documento, "##" = sección.
header_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "title"), ("##", "section")],
    strip_headers=True,  # los títulos pasan a metadata; los volvemos a anteponer abajo
)

# 2) Red de seguridad: si una sección supera CHUNK_SIZE, se subdivide.
size_splitter = RecursiveCharacterTextSplitter(
    chunk_size=config.CHUNK_SIZE,
    chunk_overlap=config.CHUNK_OVERLAP,
)


def chunk_file(path: Path, domain: str) -> list[Document]:
    """Convierte un archivo .md en chunks con metadata de procedencia."""
    text = path.read_text(encoding="utf-8")
    sections = header_splitter.split_text(text)

    chunks: list[Document] = []
    for section in sections:
        title = section.metadata.get("title", path.stem)
        section_name = section.metadata.get("section")

        # El párrafo introductorio (antes del primer "##") solo dice que la
        # política es ficticia: no aporta para responder, así que se omite.
        if not section_name:
            continue

        # "Contextual chunk header": se antepone título y sección al texto que se
        # embebe, para que el vector "sepa" de qué tema trata el fragmento.
        content = f"{title}\n## {section_name}\n{section.page_content.strip()}"

        for piece in size_splitter.split_text(content):
            chunks.append(
                Document(
                    page_content=piece,
                    metadata={
                        "domain": domain,
                        "source": path.name,
                        "title": title,
                        "section": section_name,
                    },
                )
            )

    # IDs deterministas: re-ejecutar la ingesta reemplaza en vez de duplicar.
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"{domain}/{path.stem}/{i:03d}"
    return chunks


def load_domain_chunks(domain: str) -> list[Document]:
    folder = config.DOMAINS[domain]
    chunks: list[Document] = []
    for path in sorted(folder.glob("*.md")):
        chunks.extend(chunk_file(path, domain))
    return chunks


def build_index(domain: str, chunks: list[Document]) -> None:
    """Reconstruye desde cero la colección del dominio (idempotente)."""
    from src.vectorstore import get_vectorstore  # import aquí: --dry-run no necesita OpenAI

    store = get_vectorstore(domain)
    store.reset_collection()  # borra lo anterior para no mezclar versiones
    store.add_documents(chunks, ids=[c.metadata["chunk_id"] for c in chunks])


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingesta de documentos a Chroma")
    parser.add_argument("--dry-run", action="store_true", help="No genera embeddings")
    args = parser.parse_args()

    if not args.dry_run:
        config.validate_config(require_langfuse=False)

    for domain in config.DOMAINS:
        chunks = load_domain_chunks(domain)
        sizes = [len(c.page_content) for c in chunks]
        print(
            f"[{domain}] {len(chunks)} chunks | "
            f"caracteres min={min(sizes)} prom={sum(sizes) // len(sizes)} max={max(sizes)}"
        )
        if len(chunks) < 50:
            print(f"  ATENCIÓN: {domain} tiene menos de 50 chunks (requisito de la consigna)")

        if not args.dry_run:
            build_index(domain, chunks)
            print(f"  -> indexado en Chroma (colección '{domain}_docs')")

    if args.dry_run:
        print("\nDry run: no se generaron embeddings ni se escribió en Chroma.")


if __name__ == "__main__":
    main()
