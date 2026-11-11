"""حلقه اصلی چت — workflow کامل اینجاست.

جریان هر پیام کاربر:
1. توکن‌ها را بشمار، اگر زیاد بود compaction کن.
2. پیام را به مدل بده.
3. اگر مدل ابزار خواست، ابزار را اجرا کن و نتیجه را برگردان به مدل.
4. جواب نهایی را نشان بده.
"""
from . import config
from .llm import ask
from .memory import count_messages_tokens, needs_compaction, compact_messages
from .tools import TOOLS, run_tool

SYSTEM_PROMPT = "تو یک چت‌بات آموزشی ساده هستی. کوتاه، واضح و به فارسی جواب بده. اگر کاربر مقاله خواست، از ابزار search_articles استفاده کن."


def run_chat() -> None:
    """چت ترمینالی را اجرا کن؛ با exit یا quit خارج شو."""
    missing = config.check_config()
    for msg in missing:
        print("⚠️", msg)
    if not config.LLM_API_KEY or not config.LLM_BASE_URL:
        print("اول فایل .env را کامل کن (راهنما در README است).")
        return

    messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("چت‌بات آماده است. برای خروج بنویس: exit")
    print("-" * 40)

    while True:
        user_text = input("\nتو: ").strip()
        if user_text.lower() in ("exit", "quit", "خروج"):
            print("خداحافظ!")
            break
        if not user_text:
            continue

        messages.append({"role": "user", "content": user_text})

        # 1) مدیریت توکن + compaction
        if needs_compaction(messages):
            print(f"[compaction] توکن‌ها زیاد شد ({count_messages_tokens(messages)})، خلاصه می‌کنم...")
            messages = compact_messages(messages)

        # 2) و 3) مدل + ابزار، حداکثر 3 دور
        answer = chat_one_turn(messages)
        print(f"\nبات: {answer}")
        print(f"[توکن‌ها: {count_messages_tokens(messages)} / {config.MAX_TOKENS}]")


def chat_one_turn(messages: list[dict]) -> str:
    """یک پیام کاربر را جواب بده؛ ابزار را هم در همین تابع مدیریت کن."""
    for _ in range(3):  # حداکثر 3 بار ابزار
        response = ask(messages, tools=TOOLS)
        msg = response.choices[0].message
        messages.append(msg.model_dump(exclude_none=True))

        # اگر مدل ابزار نخواست، جواب نهایی همین است
        if not msg.tool_calls:
            return msg.content or ""

        # اگر ابزار خواست، اجراش کن و نتیجه را به مکالمه اضافه کن
        for call in msg.tool_calls:
            print(f"[tool] {call.function.name} را صدا می‌زنم...")
            result = run_tool(call.function.name, call.function.arguments)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )

    return "متاسفم، نتوانستم جواب کامل بدهم."
