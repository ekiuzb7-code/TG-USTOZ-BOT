"""Mini App API bilan ishlash — aiohttp async client.

Supabase'ga to'g'ridan-to'g'ri ulanish yo'q. Faqat API orqali
telegram_id bo'yicha ro'yxatdan o'tganlikni tekshiradi.
"""

from __future__ import annotations

from typing import Optional

import aiohttp

from .config import settings


class TeacherAPI:
    """Maktab API bilan bog'lanish."""

    def __init__(self) -> None:
        self._headers = {
            "Authorization": f"Bearer {settings.BOT_API_SECRET}",
        }

    async def fetch_notifications(
        self, session: aiohttp.ClientSession
    ) -> Optional[list[dict]]:
        """POST {API_BASE_URL}/api/public/telegram/notifications

        Returns:
            [{"telegram_id": int, "text": "..."}, ...] yoki None xatolik bo'lsa
        """
        url = f"{settings.API_BASE_URL}/api/public/telegram/notifications"
        try:
            async with session.post(
                url,
                headers=self._headers,
                timeout=aiohttp.ClientTimeout(total=10.0),
            ) as resp:
                if resp.status == 401:
                    return None
                if resp.status != 200:
                    return None
                data = await resp.json()
                return data.get("messages", [])
        except aiohttp.ClientError:
            return None

    async def check_telegram(
        self, session: aiohttp.ClientSession, telegram_id: int
    ) -> Optional[dict]:
        """GET {API_BASE_URL}/api/public/telegram/check?telegram_id=<id>

        Returns:
            {"registered": True, "first_name": "...", "last_name": "..."}
            {"registered": False}
            None — tarmoq xatosi yoki 401 bo'lsa
        """
        url = f"{settings.API_BASE_URL}/api/public/telegram/check"
        params = {"telegram_id": str(telegram_id)}
        try:
            async with session.get(
                url,
                params=params,
                headers=self._headers,
                timeout=aiohttp.ClientTimeout(total=10.0),
            ) as resp:
                if resp.status == 401:
                    return {"error": "unauthorized"}
                if resp.status != 200:
                    return None
                return await resp.json()
        except aiohttp.ClientError:
            return None

    async def create_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession()


api = TeacherAPI()
