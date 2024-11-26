from typing import Sequence

import ollama
from ollama import GenerateResponse
from ollama import Options


class OllamaClientManager:
  def __init__(self):
    self.client = ollama.Client(host="http://localhost:11434")
    self._model = "llama3.1:8b"
    self._context_size = 128_000

  def embed(self, content: str) -> Sequence[Sequence[float]]:
    """Returns the LLM's embedding for the given input text.

    Args:
      content: The input textual content to embed.

    Returns:
      The embedding vector for the corresponding segment of the input content.
    """
    response = self.client.embed(
      model=self._model,
      input=content,
      options=Options(num_ctx=self._context_size),
    )
    return response.embeddings

  def chat(self, prompt: str) -> str:
    """Generates a response to the input prompt.

    Args:
        prompt: The input text to generate a response for.

    Returns:
        The generated response.
    """
    response: GenerateResponse = self.client.generate(
      model=self._model,
      prompt=prompt,
      options=Options(
        num_ctx=self._context_size,
        temperature=0,
      ),
    )
    return response.response
