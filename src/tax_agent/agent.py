from __future__ import annotations

import re


DOCUMENTS = [
    {
        "id": "SYNTH-TAX-2026-01",
        "title": "Synthetic small-business rate",
        "text": "For the fictional 2026 Example Jurisdiction, qualifying small businesses use a 10 percent illustrative rate.",
        "terms": {"small", "business", "rate", "2026"},
    },
    {
        "id": "SYNTH-TAX-2026-02",
        "title": "Synthetic filing deadline",
        "text": "The fictional annual filing deadline is 30 June 2027 for the illustrative 2026 period.",
        "terms": {"filing", "deadline", "annual", "2026"},
    },
    {
        "id": "SYNTH-TAX-2026-03",
        "title": "Synthetic expense rule",
        "text": "Only documented business-purpose expenses are deductible in this fictional example.",
        "terms": {"expense", "expenses", "deductible", "documented"},
    },
]


class TaxAgent:
    def answer(self, question: str) -> dict:
        tokens = set(re.findall(r"[a-z0-9]+", question.lower()))
        matches = [document for document in DOCUMENTS if tokens & document["terms"]]
        trace = [{"step": "query.received"}, {"step": "retrieval.completed", "citations": [item["id"] for item in matches]}]
        if not matches:
            trace.append({"step": "answer.refused", "reason": "no grounded source"})
            return {
                "status": "refused",
                "answer": "I do not have a synthetic source supporting that answer. Consult a qualified professional.",
                "citations": [],
                "trace": trace,
            }
        answer = " ".join(f"{item['text']} [{item['id']}]" for item in matches)
        trace.append({"step": "answer.completed", "grounded": True})
        return {"status": "completed", "answer": answer, "citations": [item["id"] for item in matches], "trace": trace}

    def estimate(self, taxable_amount: int, approved: bool = False) -> dict:
        if taxable_amount < 0:
            return {"status": "invalid", "reason": "taxable amount cannot be negative"}
        if not approved:
            return {"status": "approval_required", "reason": "confirm before calculating an illustrative estimate"}
        return {
            "status": "completed",
            "amount": round(taxable_amount * 0.10),
            "currency": "XCU",
            "citation": "SYNTH-TAX-2026-01",
            "disclaimer": "Fictional illustration; not tax advice.",
        }

