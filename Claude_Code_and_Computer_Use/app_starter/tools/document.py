from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pathlib import Path
from pydantic import Field


def document_path_to_markdown(
    file_path: str = Field(description="Absolute or relative path to a PDF or DOCX file"),
) -> str:
    """Convert a PDF or DOCX file at a given path to markdown-formatted text.

    Reads the file at the specified path and converts its contents to markdown.
    Supports .pdf and .docx file formats.

    When to use:
    - When you have a local file path and want its contents as markdown
    - When processing a single document on disk

    When not to use:
    - When you already have the file contents as bytes (use binary_document_to_markdown instead)
    - When the file is not a PDF or DOCX

    Examples:
    >>> document_path_to_markdown("/docs/report.pdf")
    '# Report Title\\n\\nContent...'
    >>> document_path_to_markdown("/docs/notes.docx")
    '# Notes\\n\\n- Item one...'
    """
    path = Path(file_path)
    binary_data = path.read_bytes()
    return binary_document_to_markdown(binary_data, path.suffix.lstrip("."))


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content
