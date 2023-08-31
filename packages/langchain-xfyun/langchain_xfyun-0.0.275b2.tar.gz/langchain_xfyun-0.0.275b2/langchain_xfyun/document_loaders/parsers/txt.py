"""Module for parsing text files.."""
from typing import Iterator

from langchain_xfyun.document_loaders.base import BaseBlobParser
from langchain_xfyun.document_loaders.blob_loaders import Blob
from langchain_xfyun.schema import Document


class TextParser(BaseBlobParser):
    """Parser for text blobs."""

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """Lazily parse the blob."""
        yield Document(page_content=blob.as_string(), metadata={"source": blob.source})
