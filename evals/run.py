import json
import time
from pathlib import Path

from tax_agent import TaxAgent


CASES = [
    {"id": "rate-1", "question": "small business rate", "status": "completed", "citation": "SYNTH-TAX-2026-01"},
    {"id": "rate-2", "question": "2026 business rate", "status": "completed", "citation": "SYNTH-TAX-2026-01"},
    {"id": "deadline-1", "question": "filing deadline", "status": "completed", "citation": "SYNTH-TAX-2026-02"},
    {"id": "deadline-2", "question": "annual filing", "status": "completed", "citation": "SYNTH-TAX-2026-02"},
    {"id": "expense-1", "question": "documented expense", "status": "completed", "citation": "SYNTH-TAX-2026-03"},
    {"id": "expense-2", "question": "is this deductible", "status": "completed", "citation": "SYNTH-TAX-2026-03"},
    {"id": "refuse-1", "question": "real country tax advice", "status": "refused"},
    {"id": "refuse-2", "question": "court ruling", "status": "refused"},
    {"id": "refuse-3", "question": "personal tax return", "status": "refused"},
    {"id": "refuse-4", "question": "", "status": "refused"},
]
agent = TaxAgent()
started = time.perf_counter()
results = []
for case in CASES:
    for trial in range(1, 4):
        result = agent.answer(case["question"])
        passed = result["status"] == case["status"]
        if case.get("citation"):
            passed = passed and case["citation"] in result["citations"]
        results.append({"case_id": case["id"], "trial": trial, "passed": passed})
passed = sum(item["passed"] for item in results)
report = {
    "mode": "deterministic-offline",
    "cases": len(CASES),
    "trials": len(results),
    "passed": passed,
    "success_rate": passed / len(results),
    "p50_latency_ms": round((time.perf_counter() - started) * 1000 / len(results), 3),
    "estimated_cost_usd": 0,
    "results": results,
}
Path(__file__).with_name("results.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({key: value for key, value in report.items() if key != "results"}, indent=2))
raise SystemExit(0 if passed == len(results) else 1)

