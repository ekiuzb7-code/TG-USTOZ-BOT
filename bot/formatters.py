"""Notification xabarlarini chiroyli formatlash."""

from typing import Any


def format_welcome(first_name: str | None, last_name: str | None) -> str:
    """Ro'yxatdan o'tgan ustoz uchun /start xabarini chiroyli formatda qaytaradi."""
    name = first_name or ""
    if last_name:
        name = f"{name} {last_name}".strip()
    name = name or "ustozjon"
    return (
        f"Assalomu alaykum, <b>{name}</b>! 👋\n\n"
        "Davomat uchun Mini App'ni oching. 📱\n\n"
        "✅ QR kodni skanerlang va davomatni belgilang."
    )


def format_notification(data: dict[str, Any]) -> str:
    """API'dan kelgan xabarni HTML formatda chiroyliroq qaytaradi.

    Turga qaracha emoji va sarlavha qo'shiladi, xabarlar bir xil ko'rinmasligi uchun.
    """
    text = data.get("text", "")
    notification_type = data.get("type", "")

    # Turga qaracha emoji va sarlavha
    if notification_type == "lesson_starting" or "boshlanadi" in text.lower():
        icon = "🕐"
        title = "Darsingiz tezroq boshlanadi!"
    elif notification_type == "lesson_started" or "boshlandi" in text.lower():
        icon = "🔔"
        title = "Darsingiz boshlandi!"
    elif notification_type == "attendance" or "qo'shingiz" in text.lower() or "davomat" in text.lower():
        icon = "✅"
        title = "Davomat belgilang!"
    else:
        icon = "📢"
        title = "Yangilanish!"

    # Structured ma'lumotlar borligini tekshiramiz
    lesson_hour = data.get("lesson_hour")
    group = data.get("group")
    subject = data.get("subject")
    lesson_time = data.get("time")

    details: list[str] = []
    if lesson_hour:
        details.append(f"⏰ Dars soati: {lesson_hour}")
    if group:
        details.append(f"📋 Guruh: {group}")
    if subject:
        details.append(f"📖 Fan: {subject}")
    if lesson_time:
        details.append(f"🕐 Vaqt: {lesson_time}")

    header = "\n".join(details) if details else ""
    details_block = f"\n{header}\n" if header else "\n"

    return (
        f"{icon} <b>{title}</b>\n\n"
        f"{details_block}"
        f"{text}\n\n"
        "📷 Iltimos, QR kodni skanerlang!"
    )
