"""ابزارها (Tools) — کاری که مدل خودش نمی‌تواند انجام دهد.

اینجا فقط یک ابزار داریم: سرچ مقاله در وب با Tavily.
مدل وقتی لازم بداند، خودش این ابزار را صدا می‌زند.
"""
import json
from . import config

# معرفی ابزار به مدل، با فرمت OpenAI function calling
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_articles",
            "description": "در وب مقاله پیدا کن. وقتی کاربر مقاله جدید یا خبر می‌خواهد از این استفاده کن.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "موضوع سرچ، مثلا 'هوش مصنوعی در پزشکی'",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "چند نتیجه برگردان (پیش‌فرض 3)",
                    },
                },
                "required": ["query"],
            },
        },
    }
]


def search_articles(query: str, max_results: int = 3) -> str:
    """با Tavily در وب مقاله سرچ کن و نتیجه را به صورت متن ساده بده."""
    if not config.TAVILY_API_KEY:
        return "کلید Tavily تنظیم نشده است؛ نمی‌توانم مقاله سرچ کنم."

    from tavily import TavilyClient

    client = TavilyClient(api_key=config.TAVILY_API_KEY)
    result = client.search(query=query, max_results=max_results, search_depth="basic")

    lines = []
    for item in result.get("results", []):
        lines.append(f"- {item.get('title')}\n  {item.get('url')}\n  {item.get('content', '')[:300]}")
    if not lines:
        return "مقاله‌ای پیدا نشد."
    return "\n".join(lines)


def run_tool(name: str, arguments: str) -> str:
    """ابزار را با آرگومان‌های مدل اجرا کن."""
    args = json.loads(arguments or "{}")
    if name == "search_articles":
        return search_articles(
            query=args.get("query", ""),
            max_results=args.get("max_results", 3),
        )
    return f"ابزار ناشناخته: {name}"
