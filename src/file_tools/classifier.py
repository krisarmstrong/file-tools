"""Lightweight file classification module."""

from __future__ import annotations

import json
from typing import Iterable

try:  # pragma: no cover - optional
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None  # type: ignore


PROMPT = """You are a file librarian. For each file entry (name + snippet), assign a concise category slug.
Respond with compact JSON: [{"name": "file.ext", "category": "ebooks"}, ...]."""


def classify_files(files: Iterable[dict], *, model: str = "gpt-4o-mini") -> list[dict]:
    if OpenAI is None:  # pragma: no cover
        raise RuntimeError(
            "Install required dependencies (openai, httpx) to enable file classification."
        )

    client = OpenAI()
    payload = json.dumps(list(files))
    response = client.responses.create(
        model=model,
        input=[{"role": "system", "content": PROMPT}, {"role": "user", "content": payload}],
    )
    content = response.output[0].content[0].text  # type: ignore[attr-defined]
    return json.loads(content)
