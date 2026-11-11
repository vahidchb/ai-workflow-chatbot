# چت‌بات آموزشی AI Engineering

یک چت‌بات ساده که workflow کامل AI Engineering را نشان می‌دهد:
**tool calling، مدیریت توکن، compaction و eval با LangSmith.**

همه‌چیز ساده و قابل خواندن است؛ هر فایل یک کار مشخص می‌کند.

## ساختار پروژه

```
ai-workflow-chatbot/
├── main.py                  # شروع برنامه: python main.py
├── chatbot/
│   ├── config.py            # خواندن کلیدها از .env
│   ├── llm.py               # اتصال به مدل (توکن هاربور)
│   ├── tools.py             # ابزار سرچ مقاله با Tavily
│   ├── memory.py            # شمارش توکن + compaction
│   └── chat.py              # حلقه اصلی چت + tool calling
└── evals/
    ├── langsmith_eval.py    # اجرای تست‌ها و ثبت در LangSmith
    └── test_cases.json      # سوال‌های تست
```

## رابط کاربری Angular + API پایتون

پروژه حالا دو بخش دارد: ترمینال (بالا) و وب.

- بک‌اند: `api.py` با FastAPI — همان کدهای `chatbot/`، پشت `POST /api/chat`
- فرانت‌اند: `frontend/` با Angular — صفحه چت فارسی، نمایش توکن‌ها و نشان ابزار

```bash
# ترمینال 1 — بک‌اند پایتون
uvicorn api:app --reload --port 8000

# ترمینال 2 — فرانت‌اند Angular
cd frontend
npm install
npm start
# بعد باز کن: http://localhost:4200
```

جریان داده خیلی ساده است:
`Angular (پورت 4200) -> POST http://localhost:8000/api/chat -> chatbot/chat.py -> مدل توکن هاربور -> جواب برمی‌گردد`

## نصب و اجرا (5 دقیقه)

```bash
# 1) نصب
python -m venv .venv
source .venv/bin/activate   # ویندوز: .venv\Scripts\activate
pip install -r requirements.txt

# 2) تنظیم کلیدها
cp .env.example .env
# حالا .env را باز کن و پر کن:
# TOKEN_HARBOR_API_KEY و LLM_BASE_URL از پنل توکن هاربور
# TAVILY_API_KEY از سایت Tavily (رایگان)
# LANGSMITH_API_KEY از سایت LangSmith (رایگان، اختیاری)

# 3) اجرا
python main.py
```

بعد در ترمینال بنویس، مثلا:
> مقاله جدید درباره هوش مصنوعی در پزشکی پیدا کن

## مفاهیم، خیلی ساده

| مفهوم | کجاست؟ | یعنی چی؟ |
|---|---|---|
| **Tool calling** | `chatbot/tools.py` + `chatbot/chat.py` | مدل خودش تصمیم می‌گیرد مقاله سرچ کند و نتیجه را در جواب استفاده کند. |
| **Token management** | `chatbot/memory.py` | توکن‌های مکالمه را می‌شمارد تا از حد نگذرد. |
| **Compaction** | `chatbot/memory.py` | وقتی توکن زیاد شد، پیام‌های قدیمی را خلاصه می‌کند و فقط خلاصه + چند پیام آخر می‌ماند. |
| **Eval با LangSmith** | `evals/langsmith_eval.py` | سوال‌های تست را می‌پرسد، امتیاز می‌دهد و در LangSmith ثبت می‌کند. |

اجرای eval:
```bash
python -m evals.langsmith_eval
```

## نکته امنیتی

فایل `.env` واقعی را هرگز در گیت‌هاب نگذار؛ در `.gitignore` هست.
فقط `.env.example` در ریپو است.
