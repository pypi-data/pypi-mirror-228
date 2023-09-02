from unidecode import unidecode
import re
from typing import List
from abc import abstractmethod
from langchain.schema import BaseOutputParser


def limpiar_texto(texto, **kwargs):

    texto_limpio = texto
    if "quitar_acentos" in kwargs and kwargs["quitar_acentos"] is True:
        texto_limpio = unidecode(texto_limpio)

    if "quitar_caracteres_especiales" in kwargs and kwargs["quitar_caracteres_especiales"] is True: # noqa
        texto_limpio = re.sub(r'[^\w\s]', '', texto_limpio)
        texto_limpio = texto_limpio.replace(",", "")

    texto_limpio = re.sub(r'\s+', ' ', texto_limpio)
    texto_limpio = texto_limpio.strip('\'\n".,[]*- ')

    if "minusculas" in kwargs and kwargs["minusculas"] is True:
        texto_limpio = texto_limpio.lower()

    return texto_limpio


class ListOutputParser(BaseOutputParser[List[str]]):
    """Parse the output of an LLM call to a list."""

    @property
    def _type(self) -> str:
        return "list"

    @abstractmethod
    def parse(self, text: str) -> List[str]:
        """Parse the output of an LLM call."""


class TripleHyphenSeparatedListOutputParser(ListOutputParser):
    """Parse the output of an LLM call to a triple hyphen separated list."""

    @property
    def lc_serializable(self) -> bool:
        return True

    def get_format_instructions(self) -> str:
        return (
            "Your response should be a list of triple hyphen separated values,"
            "eg: `foo --- bar --- baz`"
        )

    def parse(self, text: str) -> List[str]:
        """Parse the output of an LLM call."""
        return text.strip().split(" --- ")
