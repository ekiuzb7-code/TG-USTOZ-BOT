"""Inline klaviatura tugmalari (WebApp mini-ilova bilan)."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

WEBAPP_URL: str  # sozlanadi main.py dan


def menu_button_webapp(webapp_url: str) -> InlineKeyboardMarkup:
    """Start buyrug'i javobida ko'rsatiladigan WebApp tugmasi."""
    keyboard = [
        [InlineKeyboardButton(text="📱 Dars va Davomat (Mini App)", web_app=WebAppInfo(url=webapp_url))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def login_button_webapp(webapp_url: str) -> InlineKeyboardMarkup:
    """Ro'yxatdan o'tmagan foydalanuvchilar uchun WebApp tugmasi."""
    keyboard = [
        [InlineKeyboardButton(text="🔑 Tizimga kirish (Mini App)", web_app=WebAppInfo(url=webapp_url))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def chat_menu_button(webapp_url: str):
    """Botning chap pastki menyusiga o'rnatiladigan WebApp tugmasi (SetChatMenuButton)."""
    from aiogram.types import MenuButtonWebApp

    return MenuButtonWebApp(text="📱 Mini App", web_app=WebAppInfo(url=webapp_url))
