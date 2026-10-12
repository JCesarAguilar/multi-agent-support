"""Agente especialista de la Mesa de Ayuda de TI."""

from src.agents.rag_agent import RAGAgent

tech_agent = RAGAgent(domain="tech", role="asistente de la Mesa de Ayuda de TI")