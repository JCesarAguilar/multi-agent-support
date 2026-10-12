"""
Agente RAG genérico: busca en la colección de su dominio y responde con fuentes.

Los agentes especialistas (hr_agent, tech_agent, finance_agent) son instancias
de esta clase con distinto dominio y rol. La lógica se escribe una sola vez.
"""

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from src.schemas import AgentResponse, Intent, Source
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from src import config
from src.schemas import AgentResponse, Intent, Source
from src.vectorstore import get_vectorstore


class RAGAgent:
    def __init__(self, domain: Intent, role: str) -> None:
        self.domain: Intent = domain
        self.vectorstore = get_vectorstore(domain)

        system_prompt = (config.PROMPTS_DIR / "rag_agent_system.txt").read_text(encoding="utf-8")
        prompt = ChatPromptTemplate.from_messages(
            [("system", system_prompt), ("human", "{query}")]
        ).partial(role=role)

        llm = ChatOpenAI(
            model=config.LLM_MODEL,
            api_key=SecretStr(config.OPENAI_API_KEY),
            reasoning_effort="none",
            temperature=config.LLM_TEMPERATURE,
        )

        # Cadena LCEL: prompt -> LLM -> texto plano
        self.chain = prompt | llm | StrOutputParser()

    def retrieve(self, query: str) -> list[tuple[Document, float]]:
        """Busca los TOP_K chunks más parecidos en la colección de este dominio."""
        return self.vectorstore.similarity_search_with_relevance_scores(query, k=config.TOP_K)

    @staticmethod
    def _format_context(results: list[tuple[Document, float]]) -> str:
        """Une los chunks en un solo texto, cada uno con su procedencia."""
        blocks = []
        for i, (doc, _score) in enumerate(results, start=1):
            header = f"[{i}] {doc.metadata['source']} > {doc.metadata['section']}"
            blocks.append(f"{header}\n{doc.page_content}")
        return "\n\n".join(blocks)

    def answer(self, query: str) -> AgentResponse:
        """Recupera contexto, genera la respuesta y la devuelve con sus fuentes."""
        results = self.retrieve(query)
        text = self.chain.invoke({"query": query, "context": self._format_context(results)})

        sources = [
            Source(
                source=doc.metadata["source"],
                section=doc.metadata["section"],
                score=round(score, 3),
            )
            for doc, score in results
        ]
        return AgentResponse(query=query, intent=self.domain, answer=text, sources=sources)