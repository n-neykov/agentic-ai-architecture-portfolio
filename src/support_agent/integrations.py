"""Approved fictional customer-support knowledge and read-only account fixtures.

Each document has a stable evidence ID and narrowly scoped retrieval patterns.
This is deterministic retrieval, not semantic search or production policy.
"""
import re
from dataclasses import dataclass
from .core import BALANCES


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    text: str
    category: str = "general"


DOCUMENTS = (
    Document("faq-hours", "Support hours",
             "Support is available Monday through Friday, 9:00–17:00 (fictional).", "support"),
    Document("faq-fees", "Account fees",
             "Fees depend on the fictional account product. Review the published fee schedule or contact support for a specific charge.", "accounts"),
    Document("faq-cards", "Card replacement",
             "For a damaged or expired card, contact a human support specialist to request a replacement (fictional).", "cards"),
    Document("faq-lost-card", "Lost or stolen card",
             "If your card is lost or stolen, contact a human support specialist immediately. This demo cannot freeze or replace a card.", "cards"),
    Document("faq-statements", "Account statements",
             "In this fictional service, statements are available through the account portal. Contact support if a statement is missing.", "accounts"),
    Document("faq-deposits", "Direct deposit",
             "Direct-deposit setup requires the fictional provider's approved instructions. This demo cannot change deposit details.", "payments"),
    Document("faq-payment-times", "Payment processing times",
             "Payment processing times vary by payment type and cutoff. A human specialist can confirm timing for a specific payment (fictional).", "payments"),
    Document("faq-opening", "Opening an account",
             "Account opening requires an approved application and identity verification. This demo cannot open accounts.", "accounts"),
    Document("faq-contact", "Contacting support",
             "Contact a human support specialist through the fictional provider's official support channel. No real contact details are provided.", "support"),
    Document("faq-online-access", "Online account access",
             "For online access issues, use the fictional provider's official support process. This demo cannot reset credentials.", "digital"),
    Document("faq-atm", "ATM withdrawals",
             "ATM withdrawal limits depend on the fictional account and card terms. Contact support for the applicable limit.", "cards"),
    Document("faq-disputes", "Transaction disputes",
             "To dispute an unrecognized transaction, contact a human support specialist. This demo cannot file or resolve disputes.", "payments"),
)

# Specific terms take precedence over broad terms such as 'card' or 'open'.
_PATTERNS = {
    "faq-hours": r"\b(hours?|opening hours|business hours|when (?:do|are) you open|when (?:do|are) you close)\b",
    "faq-fees": r"\b(fees?|charges?|service charge|monthly cost)\b",
    "faq-cards": r"\b(replace(?:ment)? (?:my |a |the )?card|card replacement|damaged card|expired card)\b",
    "faq-lost-card": r"\b(lost (?:my |a |the )?card|stolen (?:my |a |the )?card|card (?:is )?(?:lost|stolen)|missing card)\b",
    "faq-statements": r"\b(statements?|transaction history|account history)\b",
    "faq-deposits": r"\b(direct deposit|payroll deposit|salary deposit)\b",
    "faq-payment-times": r"\b(payment (?:processing|time|timing)|how long (?:does|will) (?:a |my )?payment|payment cutoff)\b",
    "faq-opening": r"\b(open (?:an? |my )?account|opening (?:an? |my )?account|new account application)\b",
    "faq-contact": r"\b(contact (?:support|you|a specialist)|customer service|support (?:number|channel|contact)|reach (?:support|you))\b",
    "faq-online-access": r"\b(online (?:access|banking|login)|sign[ -]?in (?:issue|problem)|login (?:issue|problem)|locked out)\b",
    "faq-atm": r"\b(atm|cash withdrawal limit|withdrawal limits?)\b",
    "faq-disputes": r"\b(disput(?:e|ing) (?:a |my |the )?transaction|unrecognized transaction|unauthorized charge)\b",
}


def retrieve_approved(query: str) -> list[Document]:
    """Return matching approved records, excluding broad-topic collisions."""
    q = query.lower()
    matched = {key for key, pattern in _PATTERNS.items() if re.search(pattern, q)}
    if re.search(r"\bopen\b", q) and "faq-opening" not in matched:
        matched.add("faq-hours")
    if re.search(r"\bcard\b", q) and not ({"faq-cards", "faq-lost-card"} & matched):
        matched.add("faq-cards")
    return [doc for doc in DOCUMENTS if doc.doc_id in matched]


def scoped_balance(*, principal_id: str | None, authenticated: bool) -> str | None:
    """Caller cannot select an arbitrary account; identity is simulated."""
    if not authenticated or not principal_id:
        return None
    return BALANCES.get(principal_id)
