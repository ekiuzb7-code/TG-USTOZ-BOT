"""UstozNazorat Telegram bot — kirish nuqta (Railway worker: python main.py)."""

from __future__ import annotations

import asyncio
import logging
import signal
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.api_client import api
from bot.config import settings
from bot.handlers import on_startup, register_handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("ustoz-nazorat")

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

_registered = False
_stop_event = asyncio.Event()


async def _ensure_startup() -> None:
    global _registered
    if not _registered:
        register_handlers(dp)
        _registered = True
    await on_startup(bot)


async def _notification_poller(bot: Bot) -> None:
    """Har 60 soniyada yangilanishlarni API'dan olib, foydalanuvchilarga yuboradi."""
    while not _stop_event.is_set():
        try:
            async with await api.create_session() as session:
                messages = await api.fetch_notifications(session)
            if messages:
                for msg in messages:
                    try:
                        await bot.send_message(msg["telegram_id"], msg["text"])
                    except Exception as exc:  # noqa: BLE001
                        logger.exception(
                            "Xabar yuborilmadi (telegram_id=%s): %s",
                            msg.get("telegram_id"),
                            exc,
                        )
        except Exception as exc:  # noqa: BLE001
            logger.exception("Notifications so'rovida xatolik: %s", exc)
        await asyncio.sleep(60)


async def _run_polling() -> None:
    await _ensure_startup()
    asyncio.create_task(_notification_poller(bot))
    logger.info("Bot long-polling rejimida ishga tushmoqda...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


async def _shutdown(signame: str | None = None) -> None:
    if signame:
        logger.info("Signal qabul qilindi: %s — bot to'xtatilmoqda...", signame)
    _stop_event.set()
    try:
        await dp.stop_polling()
    finally:
        await bot.session.close()
        logger.info("Bot to'xtatildi.")


def main() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(_shutdown(s.name)))
        except NotImplementedError:  # pragma: no cover - Windows fallback
            pass

    try:
        loop.run_until_complete(_run_polling())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(_shutdown())
        loop.close()


if __name__ == "__main__":
    main()
