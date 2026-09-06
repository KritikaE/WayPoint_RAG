"""Thin service layer bridging the FastAPI app to the existing RAG pipeline.

All actual RAG logic (retrieval, reranking, prompting, LLM calls) lives in
src/rag_pipeline.py (and the modules it wraps: retrieve.py, prompt.py,
generate.py). This module only adapts that pipeline for use by the API layer
and translates pipeline errors into a shape the API layer can handle.
"""

import sys
from pathlib import Path

# Ensure src/ is importable regardless of the current working directory the
# API is launched from.
_SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from rag_pipeline import ask_question as _ask_question  # noqa: E402


class RagServiceError(Exception):
    """Raised when the underlying RAG pipeline fails unexpectedly."""


def ask(question: str) -> dict:
    """Run the RAG pipeline for a question and return the answer + sources.

    Raises:
        ValueError: If the question is empty/blank (propagated from the
            pipeline's own validation).
        RagServiceError: If the pipeline raises any other unexpected error
            (e.g. retrieval/LLM failure).
    """
    try:
        return _ask_question(question)
    except ValueError:
        # Let empty/blank question validation errors propagate as-is so the
        # API layer can map them to a 400 response.
        raise
    except Exception as exc:  # noqa: BLE001 - intentionally broad at the boundary
        raise RagServiceError(f"RAG pipeline failed: {exc}") from exc
