"""Inline klaviatura tugmalari (WebApp mini-ilova bilan)."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp, WebAppInfo


def scan_button(webapp_url: str) -> InlineKeyboardMarkup:
    """Ro'yxatdan o'tgan foydalanuvchi uchun '📷 Skanerlash' tugmasi."""
    keyboard = [
        [InlineKeyboardButton(text="📷 Skanerlash", web_app=WebAppInfo(url=webapp_url))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def chat_menu_button(webapp_url: str) -> MenuButtonWebApp:
    """Botning chap pastki menyusiga o'rnatiladigan WebApp tugmasi."""
    return MenuButtonWebApp(text="📱 Mini App", web_app=WebAppInfo(url=webapp_url))
