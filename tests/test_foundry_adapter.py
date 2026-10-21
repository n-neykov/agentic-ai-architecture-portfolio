"""Offline tests for Foundry URL handling and response adapter (no Azure calls)."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from src.support_agent.azure_model import _foundry_base_url, FoundryResponsesModel


class FoundryAdapterTests(unittest.TestCase):
    def test_responses_endpoint(self):
        url = "https://demo.services.ai.azure.com/api/projects/sample/openai/v1/responses"
        self.assertEqual(_foundry_base_url(url),
                         "https://demo.services.ai.azure.com/api/projects/sample/openai/v1/")

    def test_project_endpoint(self):
        self.assertEqual(
            _foundry_base_url("https://demo.services.ai.azure.com/api/projects/sample"),
            "https://demo.services.ai.azure.com/api/projects/sample/openai/v1/")

    def test_v1_endpoint(self):
        self.assertEqual(
            _foundry_base_url("https://demo.services.ai.azure.com/api/projects/sample/openai/v1/"),
            "https://demo.services.ai.azure.com/api/projects/sample/openai/v1/")

    def test_reject_unsafe_url(self):
        for url in ("http://demo.services.ai.azure.com/api/projects/sample",
                    "https://example.com/api/projects/sample",
                    "https://demo.services.ai.azure.com/api/projects/sample/openai/v1/responses?key=secret",
                    "https://demo.services.ai.azure.com/other"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                _foundry_base_url(url)

    def test_invocation_contract(self):
        fake = SimpleNamespace(responses=SimpleNamespace(
            create=lambda **kwargs: SimpleNamespace(output_text='{"tool":"faq_lookup"}')))
        model = object.__new__(FoundryResponsesModel)
        model.client = fake
        model.deployment = "gpt-4.1-mini"
        from langchain_core.messages import HumanMessage, SystemMessage
        response = model.invoke([SystemMessage(content="Choose a tool"),
                                 HumanMessage(content="What are your hours?")])
        self.assertEqual(response.content, '{"tool":"faq_lookup"}')


if __name__ == "__main__":
    unittest.main()
