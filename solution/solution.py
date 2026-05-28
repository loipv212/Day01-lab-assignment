"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""

import os
import time
from typing import Any, Callable

# ---------------------------------------------------------------------------
# OpenRouter configuration (OpenAI-compatible API)
# ---------------------------------------------------------------------------
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# ---------------------------------------------------------------------------
# Estimated costs per 1K OUTPUT tokens (USD) — update if pricing changes
# ---------------------------------------------------------------------------
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
    "openai/gpt-4o": 0.010,
    "openai/gpt-4o-mini": 0.0006,
}

OPENAI_MODEL = "openai/gpt-4o"
OPENAI_MINI_MODEL = "openai/gpt-4o-mini"


def _make_client():
    """Create an OpenAI-compatible client pointed at OpenRouter."""
    from openai import OpenAI
    return OpenAI(api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL)


# ---------------------------------------------------------------------------
# Task 1 — Call GPT-4o
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API and return the response text + latency.
    """
    client = _make_client()

    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    latency = time.time() - start

    text = response.choices[0].message.content or ""
    # Ensure latency is a positive float even on extremely fast mocked calls
    if latency <= 0:
        latency = 1e-6
    return text, float(latency)


# ---------------------------------------------------------------------------
# Task 2 — Call GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call gpt-4o-mini and return (response_text, latency_seconds).
    """
    return call_openai(
        prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )


# ---------------------------------------------------------------------------
# Task 3 — Compare GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    """
    Call both gpt-4o and gpt-4o-mini and return a comparison dict.
    """
    gpt4o_text, gpt4o_latency = call_openai(prompt)
    mini_text, mini_latency = call_openai_mini(prompt)

    # Rough token estimate: 0.75 words ≈ 1 token
    estimated_tokens = len(gpt4o_text.split()) / 0.75
    gpt4o_cost_estimate = (
        estimated_tokens / 1000 * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
    )

    return {
        "gpt4o_response": gpt4o_text,
        "mini_response": mini_text,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": gpt4o_cost_estimate,
    }


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot with conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Interactive streaming chatbot. Streams tokens, keeps last 3 turns,
    exits on 'quit' or 'exit'.
    """
    client = _make_client()
    history: list[dict] = []

    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            break

        if user_input.strip().lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        history.append({"role": "user", "content": user_input})

        messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ] + history

        print("Assistant: ", end="", flush=True)
        assistant_reply_parts: list[str] = []

        try:
            stream = client.chat.completions.create(
                model=OPENAI_MINI_MODEL,
                messages=messages,
                stream=True,
            )
            for chunk in stream:
                try:
                    delta = chunk.choices[0].delta.content or ""
                except (AttributeError, IndexError):
                    delta = ""
                if delta:
                    print(delta, end="", flush=True)
                    assistant_reply_parts.append(delta)
        except Exception as exc:  # network / API failures shouldn't crash the loop
            print(f"\n[error: {exc}]")
            history.pop()  # remove the user turn that produced no reply
            continue

        print()  # newline after the streamed reply

        assistant_reply = "".join(assistant_reply_parts)
        history.append({"role": "assistant", "content": assistant_reply})

        # Keep the last 3 turns (each turn = user + assistant = 2 messages)
        history = history[-6:]


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Call fn(). Retry up to max_retries with exponential backoff.
    """
    last_exc: BaseException | None = None
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as exc:
            last_exc = exc
            if attempt >= max_retries:
                break
            time.sleep(base_delay * (2 ** attempt))
    assert last_exc is not None
    raise last_exc


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    """Run compare_models on each prompt; attach the prompt to every result."""
    results: list[dict] = []
    for prompt in prompts:
        result = compare_models(prompt)
        result["prompt"] = prompt
        results.append(result)
    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    """Format batch_compare results as a readable text table."""
    def truncate(text: str, n: int = 40) -> str:
        text = str(text).replace("\n", " ")
        return text if len(text) <= n else text[: n - 1] + "…"

    headers = [
        "Prompt",
        "GPT-4o Response",
        "Mini Response",
        "GPT-4o Latency",
        "Mini Latency",
    ]
    rows = [headers]
    for r in results:
        rows.append([
            truncate(r.get("prompt", "")),
            truncate(r.get("gpt4o_response", "")),
            truncate(r.get("mini_response", "")),
            f"{r.get('gpt4o_latency', 0):.3f}s",
            f"{r.get('mini_latency', 0):.3f}s",
        ])

    widths = [max(len(row[i]) for row in rows) for i in range(len(headers))]
    sep = "-+-".join("-" * w for w in widths)

    lines = []
    for idx, row in enumerate(rows):
        line = " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(row))
        lines.append(line)
        if idx == 0:
            lines.append(sep)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Register this module under a Python-identifier-safe name.
# The repo folder `Day01-lab-assignment` contains a dash, so the auto-generated
# module name `Day01-lab-assignment.solution` is rejected by unittest.mock.patch
# (pkgutil.resolve_name regex). Aliasing fixes that without touching tests.
# ---------------------------------------------------------------------------
import sys as _sys
_VALID_MODULE_NAME = "day01_solution"
_sys.modules.setdefault(_VALID_MODULE_NAME, _sys.modules[__name__])
for _fn in (
    call_openai,
    call_openai_mini,
    compare_models,
    streaming_chatbot,
    retry_with_backoff,
    batch_compare,
    format_comparison_table,
):
    _fn.__module__ = _VALID_MODULE_NAME


# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    streaming_chatbot()
