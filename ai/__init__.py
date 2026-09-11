"""
KavachNet AI & Entity Resolution Package
Implements Named Entity Recognition (NER), cross-source entity disambiguation,
and the rule-based AI Investigative Assistant engine.
"""

from .ner_extractor import MultiSourceNERExtractor, ExtractedEntity
from .entity_resolution import EntityResolver, ResolvedEntityLink
from .assistant_engine import InvestigativeAssistantEngine

__all__ = [
    "MultiSourceNERExtractor",
    "ExtractedEntity",
    "EntityResolver",
    "ResolvedEntityLink",
    "InvestigativeAssistantEngine",
]
