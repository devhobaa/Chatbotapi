from __future__ import annotations
import os
import asyncio
from typing import List, Dict, Any, Optional, AsyncGenerator

class GeminiMindAdapter:
    """
    هذا ملف "Adapter" للتوصيل بين API وبين البوت اللي عندك.
    كل المطلوب إنك تعدّل الاستيراد في __init__ و chat/chat_stream بحيث ينادوا كودك الحقيقي.
    """
    def __init__(self):
        # مثال: جلب مفاتيح/إعدادات من البيئة
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        # TODO: استبدل الأسطر التالية باستيراد وتهيئة البوت الحقيقي عندك
        # from GeminiMindBot.main import Bot
        # self.bot = Bot(api_key=self.gemini_api_key)
        self.bot = None  # placeholder

    def chat(
        self,
        message: str,
        history: Optional[List[Dict[str, str]]] = None,
        user_id: Optional[str] = None,
        temperature: Optional[float] = None,
        stream: bool = False,
    ) -> tuple[str, Dict[str, Any]]:
        """
        يجب أن تعيد: (النص_النهائي, احصائيات_الاستخدام)
        استبدل هذا المنطق بالمناداة على البوت الفعلي.
        """
        # مثال (وهمي):
        # reply = self.bot.ask(message, history=history, temperature=temperature)
        reply = f"[MOCK] You said: {message}"
        usage = {"prompt_tokens": None, "completion_tokens": None, "model": "gemini"}
        return reply, usage

    async def chat_stream(
        self,
        message: str,
        history: Optional[List[Dict[str, str]]] = None,
        user_id: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> AsyncGenerator[str, None]:
        """
        يجب أن تُرجِع أجزاء النص تدريجيًا (Streaming).
        لو SDK عندك غير متوافق مع Async، تقدر تولّد من الـ chat العادي زي المثال.
        """
        reply, _ = self.chat(message, history, user_id, temperature, stream=False)
        for ch in reply:
            # محاكاة ستريمنج حرف-بحرف
            await asyncio.sleep(0)  # إتاحة للدورة الحدثية
            yield ch

_adapter_singleton: Optional[GeminiMindAdapter] = None

def get_bot() -> GeminiMindAdapter:
    global _adapter_singleton
    if _adapter_singleton is None:
        _adapter_singleton = GeminiMindAdapter()
    return _adapter_singleton
