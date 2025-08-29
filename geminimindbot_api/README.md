# GeminiMindBot API Wrapper

واجهـة REST سريعة (FastAPI) تلتف حول البوت بتاعك **GeminiMindBot** عشان تقدر تربطه بأي حاجة بسهولة (ويب/موبايل/خدمة أخرى).

## التركيب

```bash
cd geminimindbot_api
python -m venv .venv && source .venv/bin/activate  # على ويندوز: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # عدّل SERVICE_API_KEY و مفاتيح البوت
python app.py
```

هيشتغل على: `http://localhost:8000`  
صحـة الخدمة: `GET /health`

## الاستخدام

### طلب عادي
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: change-me" \
  -d '{ "message": "Hello", "history": [] }'
```

### ستريمنج (SSE)
من المتصفح:
```js
const es = new EventSource("/chat/stream", { withCredentials: false });
// ملاحظة: لازم تضيف الهيدر X-API-Key بنفسك باستخدام Proxy أو تحويل لfetch+ReadableStream لو عايز هيدر مخصص
```

أو من Node (باستخدام fetch + ReadableStream) — شوف ملف `clients/js_fetch_example.md`.

## التوصيل بالبـوت الحقيقي

عدّل الملف: `adapters/gemini_mind_adapter.py`
- غيّر الاستيراد في `__init__` عشان يهيّأ البوت الحقيقي.
- في `chat`: استبدل الـ MOCK بمناداة دالة البوت (مثل: `self.bot.ask(...)`) وأرجع `(reply_text, usage_dict)`.
- في `chat_stream`: لو SDK يدعم تدفق، خلّيه يولّد أجزاء النص. لو لا، استخدم التفكيك زي المثال.

## Docker

```bash
docker build -t gemini-mind-api .
docker run -p 8000:8000 --env-file .env gemini-mind-api
```

## أمان مختصر
- الهيدر `X-API-Key` مطلوب. غيّر `SERVICE_API_KEY` في `.env` لقيمة قوية.
- فعّل CORS بقائمة Origins مناسبة لو هتستدعي من متصفح.
- لو محتاج OAuth/JWT، ده سهل إضافته لاحقًا.

بالتوفيق!🚀
