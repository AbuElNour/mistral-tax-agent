import json

from .agent import TaxAgent


def main():
    agent = TaxAgent()
    print(json.dumps(agent.answer("What is the 2026 small business rate?"), indent=2))
    print(json.dumps(agent.answer("What is the rule for a real country?"), indent=2))
    print(json.dumps(agent.estimate(10000, approved=True), indent=2))


if __name__ == "__main__":
    main()

