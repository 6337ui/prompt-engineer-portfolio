"""
An example LangChain chain for the prompt-engineer portfolio.

This module illustrates how to use a prompt template with a simple LLM
chain. The underlying language model call is abstracted through the
httpx-client wrapper, making this chain easy to swap for different
providers.
"""

from typing import Any
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms.base import LLM


class HTTPXLLM(LLM):
    """A minimal LangChain LLM wrapper around the httpx-client model."""

    async def _call(self, prompt: str, stop: list[str] | None = None) -> str:
        from httpx_client.model_client import call_model  # type: ignore

        result = await call_model(prompt)
        return result.get("output", "")

    @property
    def _identifying_params(self) -> dict[str, Any]:
        return {}


async def run_chain(prompt: str) -> str:
    """Run a simple summarisation chain using a prompt template."""
    template = PromptTemplate(
        input_variables=["text"],
        template="Summarise the following text in one sentence:\n\n{text}",
    )
    llm = HTTPXLLM()
    chain = LLMChain(llm=llm, prompt=template)
    return await chain.arun(text=prompt)