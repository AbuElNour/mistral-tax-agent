import unittest

from tax_agent import TaxAgent


class TaxAgentTests(unittest.TestCase):
    def setUp(self):
        self.agent = TaxAgent()

    def test_grounded_answer_has_citation(self):
        result = self.agent.answer("small business rate")
        self.assertEqual(result["status"], "completed")
        self.assertIn(result["citations"][0], result["answer"])

    def test_unknown_question_refuses(self):
        self.assertEqual(self.agent.answer("real jurisdiction advice")["status"], "refused")

    def test_estimate_requires_approval(self):
        self.assertEqual(self.agent.estimate(1000)["status"], "approval_required")

    def test_estimate_is_fictional_currency(self):
        result = self.agent.estimate(1000, approved=True)
        self.assertEqual(result["currency"], "XCU")
        self.assertEqual(result["amount"], 100)

    def test_negative_amount_rejected(self):
        self.assertEqual(self.agent.estimate(-1, approved=True)["status"], "invalid")


if __name__ == "__main__":
    unittest.main()

