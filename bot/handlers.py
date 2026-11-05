"""Bot handlerlari: /start, /myid."""

from __future__ import annotations

import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import MenuButtonWebApp

from .api_client import api
from .config import settings
from .keyboards import chat_menu_button, scan_button

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    """Bot ishga tushganda: chap pastki menyuga WebApp tugmasi o'rnatadi."""
    try:
        await bot.set_chat_menu_button(
            menu_button=chat_menu_button(settings.WEBAPP_URL)
        )
        logger.info("Chat menu button o'rnatildi.")
    except Exception as exc:  # noqa: BLE001
        logger.exception("Chat menu button o'rnatilmadi: %s", exc)

    commands = [
        types.BotCommand(command="start", description="Botni ishga tushirish va Mini App'ni ochish"),
        types.BotCommand(command="myid", description="Sizning Telegram ID raqamingiz"),
    ]
    try:
        await bot.set_my_commands(commands)
        logger.info("Bot buyruqlari o'rnatildi.")
    except Exception as exc:  # noqa: BLE001
        logger.exception("Buyruqlar o'rnatilmadi: %s", exc)


async def cmd_start(message: types.Message) -> None:
    """/start — API orqali ro'yxatdan o'tganligini tekshiradi."""
    telegram_id = message.from_user.id

    async with await api.create_session() as session:
        result = await api.check_telegram(session, telegram_id)

    # Tarmoq xatosi yoki 401
    if result is None:
        await message.answer("Server bilan aloqa yo'q, keyinroq urinib ko'ring.")
        logger.error("API tarmoq xatosi: telegram_id=%s", telegram_id)
        return

    if result.get("error") == "unauthorized":
        await message.answer("Server bilan aloqa yo'q, keyinroq urinib ko'ring.")
        logger.error("API 401 unauthorized: BOT_API_SECRET tekshiring")
        return

    if result.get("registered"):
        first_name = result.get("first_name") or "foydalanuvchi"
        text = f"Assalomu alaykum, {first_name}! Davomat uchun Mini App'ni oching."
        await message.answer(text, reply_markup=scan_button(settings.WEBAPP_URL))
    else:
        text = (
            f"❌ Siz ro'yxatdan o'tmagansiz. Telegram ID: <code>{telegram_id}</code>.\n"
            "Bu raqamni maktab ma'muriyatiga yuboring."
        )
        await message.answer(text, parse_mode="HTML")


async def cmd_myid(message: types.Message) -> None:
    """/myid — Telegram ID'ni qaytaradi."""
    await message.answer(
        f"Sizning Telegram ID'ingiz: <code>{message.from_user.id}</code>",
        parse_mode="HTML",
    )


def register_handlers(dp: Dispatcher) -> None:
    """Barcha handlerlarni dispatcherga ro'yxatdan o'tkazadi."""
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_myid, Command("myid"))
