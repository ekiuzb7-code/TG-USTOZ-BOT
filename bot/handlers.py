"""Bot handlerlari: /start, /status, /myid, /help va bot ishga tushganda."""

from __future__ import annotations

import logging
from typing import Optional

import httpx

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import MenuButtonWebApp, WebAppInfo

from .config import settings
from .database import db
from .keyboards import chat_menu_button, login_button_webapp, menu_button_webapp

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    """Bot ishga tushganda: menyu tugmasi va buyruqlarni sozlaydi."""
    # Chap pastki menyuga WebApp tugmasi
    try:
        await bot.set_chat_menu_button(
            menu_button=chat_menu_button(settings.WEBAPP_URL)
        )
        logger.info("Chat menu button o'rnatildi.")
    except Exception as exc:  # noqa: BLE001
        logger.exception("Chat menu button o'rnatilmadi: %s", exc)

    # Bot buyruqlari ro'yxati
    commands = [
        types.BotCommand(command="start", description="Botni ishga tushirish va Mini App'ni ochish"),
        types.BotCommand(command="status", description="Telegram hisobingiz holatini tekshirish"),
        types.BotCommand(command="myid", description="Sizning Telegram ID raqamingiz"),
        types.BotCommand(command="help", description="Foydalanish bo'yicha yordam"),
    ]
    try:
        await bot.set_my_commands(commands)
        logger.info("Bot buyruqlari o'rnatildi.")
    except Exception as exc:  # noqa: BLE001
        logger.exception("Buyruqlar o'rnatilmadi: %s", exc)


async def cmd_start(message: types.Message) -> None:
    """/start — foydalanuvchi holatiga qarab javob qaytaradi."""
    telegram_id = message.from_user.id
    username = message.from_user.username

    async with httpx.AsyncClient() as client:
        teacher = await db.get_teacher_by_telegram_id(client, telegram_id)

    if teacher and teacher.get("full_name"):
        full_name = teacher["full_name"]
        text = (
            f"Assalomu alaykum, {full_name} ustoz! 👨‍🏫\n\n"
            "UstozNazorat tizimiga xush kelibsiz.\n\n"
            "Dars jadvalingizni ko'rish, o'z davomatingizni tekshirish va "
            "xona QR-kodini skanerlash uchun quyidagi tugmani bosing:"
        )
        await message.answer(text, reply_markup=menu_button_webapp(settings.WEBAPP_URL))
    else:
        text = (
            "Assalomu alaykum! ⚠️\n\n"
            "Siz hali UstozNazorat tizimida ro'yxatdan o'tmagansiz yoki "
            "Telegram hisobingiz profilingizga bog'lanmagan.\n\n"
            "Iltimos, maktab ma'muriyati (super admin yoki zavuch) bergan login va "
            "parolingiz bilan tizimga kirish uchun quyidagi tugmani bosing. "
            "Kirganingizdan so'ng Telegram hisobingiz avtomatik biriktiriladi:"
        )
        await message.answer(text, reply_markup=login_button_webapp(settings.WEBAPP_URL))


async def cmd_status(message: types.Message) -> None:
    """/status — foydalanuvchi holatini chiroyli formatda ko'rsatadi."""
    user = message.from_user
    telegram_id = user.id
    username = user.username or "mavjud emas"

    async with httpx.AsyncClient() as client:
        teacher = await db.get_teacher_by_telegram_id(client, telegram_id)

    if teacher:
        boglangan = "ha ✅"
        ism = teacher.get("full_name") or "nomlum"
    else:
        boglangan = "yo'q ❌"
        ism = "ro'yxatdan o'tmagan"

    text = (
        f"🆔 Telegram ID: <code>{telegram_id}</code>\n"
        f"👤 Username: @{username}\n"
        f"📚 Ism: {ism}\n"
        f"🔗 Tizimga bog'langan: {boglangan}"
    )
    await message.answer(text, parse_mode="HTML")


async def cmd_myid(message: types.Message) -> None:
    """/myid — Telegram ID'ni nusxalash quvvatli formatda chiqaradi."""
    await message.answer(
        f"Sizning Telegram ID'ingiz: <code>{message.from_user.id}</code>",
        parse_mode="HTML",
    )


async def cmd_help(message: types.Message) -> None:
    """/help — qisqa qo'llanma."""
    text = (
        "📖 <b>UstozNazorat botidan foydalanish qo'llanmasi:</b>\n\n"
        "1. Tugmani bosing va login/parolingizni kiriting.\n"
        "2. Mini App ochilganda lokatsiya (GPS) va kamera ruxsatini tasdiqlang.\n"
        "3. Dars xonasidagi QR-kodni skanerlang.\n\n"
        "Buyruqlar:\n"
        "/start - Botni ishga tushirish va Mini App'ni ochish\n"
        "/status - Telegram hisobingiz holatini tekshirish\n"
        "/myid - Sizning Telegram ID raqamingiz\n"
        "/help - Foydalanish bo'yicha yordam"
    )
    await message.answer(text, parse_mode="HTML")


def register_handlers(dp: Dispatcher) -> None:
    """Barcha handlerlarni dispatcherga ro'yxatdan o'tkazadi."""
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_status, Command("status"))
    dp.message.register(cmd_myid, Command("myid"))
    dp.message.register(cmd_help, Command("help"))
