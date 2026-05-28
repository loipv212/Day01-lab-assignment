"""
Scripts hỗ trợ Phần 2 — Bài Tập Mở Rộng

Chạy:
    python solution/run_exercises.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from solution import call_openai, COST_PER_1K_OUTPUT_TOKENS, OPENAI_MODEL, OPENAI_MINI_MODEL


def exercise_2_1():
    """Bài 2.1 — Độ nhạy temperature."""
    print("=" * 70)
    print("Bài 2.1 — Độ Nhạy Của Temperature")
    print("=" * 70)
    prompt = "Hãy kể cho tôi một sự thật thú vị về Việt Nam."

    for temp in [0.0, 0.5, 1.0, 1.5]:
        print(f"\n--- temperature = {temp} ---")
        text, latency = call_openai(prompt, temperature=temp, max_tokens=120)
        print(text)
        print(f"(latency: {latency:.2f}s)")


def exercise_2_2():
    """Bài 2.2 — Đánh đổi chi phí."""
    print("\n" + "=" * 70)
    print("Bài 2.2 — Đánh Đổi Chi Phí")
    print("=" * 70)
    users = 10_000
    calls_per_user = 3
    tokens_per_call = 350

    total_tokens = users * calls_per_user * tokens_per_call
    total_k_tokens = total_tokens / 1000

    cost_4o = total_k_tokens * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
    cost_mini = total_k_tokens * COST_PER_1K_OUTPUT_TOKENS["gpt-4o-mini"]
    ratio = cost_4o / cost_mini

    print(f"Tổng số token / ngày: {total_tokens:,}")
    print(f"Chi phí GPT-4o:      ${cost_4o:.2f} / ngày")
    print(f"Chi phí GPT-4o-mini: ${cost_mini:.2f} / ngày")
    print(f"GPT-4o đắt hơn GPT-4o-mini: ~{ratio:.1f} lần")


def exercise_2_3():
    """Bài 2.3 — chỉ cần phản ánh, không chạy code."""
    print("\n" + "=" * 70)
    print("Bài 2.3 — Streaming UX (câu hỏi phản ánh)")
    print("=" * 70)
    print("Không cần chạy code — viết 1 đoạn văn vào exercises.md.")


if __name__ == "__main__":
    exercise_2_1()
    exercise_2_2()
    exercise_2_3()
