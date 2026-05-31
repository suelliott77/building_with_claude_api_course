# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Set up environment
uv venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# Install in development mode
uv pip install -e .

# Start the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_docx_conversion
```

## Architecture

This project exposes Python functions as tools via a [FastMCP](https://github.com/jlowin/fastmcp) server.

**Entry point:** `main.py` creates a `FastMCP` instance named `"docs"`, imports tool functions, registers them, and runs the server. All tool registration happens here.

**Tools** live in `tools/` as plain Python functions. Currently:
- `tools/math.py` — `add()`: registered in `main.py`
- `tools/document.py` — `binary_document_to_markdown()`: implemented and tested but **not yet registered** in `main.py`

**Tests** in `tests/` use real fixture files (`tests/fixtures/*.docx`, `*.pdf`) rather than mocks.

## Defining MCP Tools

Tools are regular Python functions registered with:
```python
mcp.tool()(my_function)
```

Use `Field` from pydantic for parameter descriptions (these are exposed to AI assistants):
```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does")
) -> ReturnType:
    """
    One-line summary.

    Detailed explanation of functionality.
    When to use (and when NOT to use) this tool.
    Usage examples with expected input/output.
    """
    # Implementation
```

Docstrings should explain *when* to use the tool and include input/output examples — this is what the AI assistant sees when deciding whether to call the tool.
