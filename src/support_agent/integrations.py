"""Synthetic data adapters; not connected to a production CRM."""
from dataclasses import dataclass
from .core import BALANCES

@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    text: str

DOCUMENTS = (
    Document("faq-hours", "Support hours", "Support is available Monday through Friday, 9:00–17:00 (fictional)."),
    Document("faq-fees", "Fees", "Consult the published fee schedule. Fees vary by product (fictional)."),
    Document("faq-cards", "Card replacement", "To replace a card, contact a human support specialist (fictional)."),
)

def retrieve_approved(query: str) -> list[Document]:
    """Deterministic keyword retrieval; NOT semantic/vector RAG."""
    q=query.lower()
    matches=[]
    for d in DOCUMENTS:
        tokens={'hours': ('hour','open'), 'fees': ('fee','charge'), 'cards': ('card','replace')}[d.doc_id.split('-')[1]]
        if any(t in q for t in tokens): matches.append(d)
    return matches

def scoped_balance(*, principal_id: str | None, authenticated: bool) -> str | None:
    """Caller cannot supply an arbitrary account id; principal comes from trusted context."""
    if not authenticated or not principal_id: return None
    return BALANCES.get(principal_id)
