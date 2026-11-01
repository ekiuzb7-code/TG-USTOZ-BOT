"""Supabase PostgreSQL bilan ishlash — httpx async client orqali REST API."""

from __future__ import annotations

from typing import Optional

import httpx

from .config import settings


class SupabaseDB:
    """Minimal Supabase REST client (async)."""

    def __init__(self) -> None:
        self._headers = {
            "apikey": settings.SUPABASE_KEY,
            "Authorization": f"Bearer {settings.SUPABASE_KEY}",
            "Content-Type": "application/json",
        }

    async def get_teacher_by_telegram_id(
        self, client: httpx.AsyncClient, telegram_id: int
    ) -> Optional[dict]:
        """telegram_links jadvalidan telegram_id bo'yicha qidiradi, profiles bilan JOIN qiladi.

        Topsa -> {"telegram_id": int, "username": str|None, "full_name": str}
        Topmasa -> None
        """
        url = (
            f"{settings.SUPABASE_URL}/rest/v1/telegram_links"
            f"?telegram_id=eq.{telegram_id}"
            f"&select=telegram_id,username,linked_at,profiles(full_name)"
        )
        try:
            resp = await client.get(url, headers=self._headers, timeout=10.0)
        except httpx.RequestError:
            return None
        if resp.status_code != 200:
            return None
        rows = resp.json()
        if not rows:
            return None
        row = rows[0]
        profiles = row.get("profiles") or []
        full_name = profiles[0].get("full_name") if profiles else None
        return {
            "telegram_id": row.get("telegram_id"),
            "username": row.get("username"),
            "full_name": full_name,
        }

    async def link_telegram(
        self, client: httpx.AsyncClient, user_id: str, telegram_id: int, username: Optional[str]
    ) -> bool:
        """Mini App'dan kelgan so'rov orqali Telegram hisobini profilingga bog'laydi."""
        url = f"{settings.SUPABASE_URL}/rest/v1/telegram_links"
        payload = {
            "user_id": user_id,
            "telegram_id": telegram_id,
            "username": username,
        }
        try:
            resp = await client.post(url, headers=self._headers, json=payload, timeout=10.0)
        except httpx.RequestError:
            return False
        return resp.status_code in (200, 201)


db = SupabaseDB()
