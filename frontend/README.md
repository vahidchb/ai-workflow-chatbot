# فرانت‌اند Angular — چت‌بات آموزشی

صفحه چت ساده فارسی که به API پایتون وصل می‌شود.

## اجرا

```bash
# اول بک‌اند را در یک ترمینال جدا اجرا کن:
# uvicorn api:app --reload --port 8000

npm install
npm start
# باز کن: http://localhost:4200
```

## فایل‌های مهم

- `src/app/app.ts` — منطق چت (پیام‌ها، توکن‌ها، loading)
- `src/app/app.html` / `app.css` — ظاهر صفحه چت
- `src/app/chat.service.ts` — صدا زدن `POST http://localhost:8000/api/chat`
- `src/app/app.config.ts` — فعال کردن HttpClient

فرانت‌اند هیچ کلیدی ندارد؛ همه کلیدها فقط در `.env` بک‌اند پایتون است.
