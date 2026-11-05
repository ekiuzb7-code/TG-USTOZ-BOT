"""Notification xabarlarini chiroyli formatlash."""

from typing import Any


def format_notification(data: dict[str, Any]) -> str:
    """API'dan kelgan xabarni HTML formatda chiroyliroq qaytaradi.

    Agar API structured maydonlar (lesson_hour, subject, group, time) bersa —
    ularni emoji bilan ajratib chiqadi. Aks holda oddiy `text` maydonini
    qadorlarga bo'lib saralab qaytaradi.
    """
    text = data.get("text", "")

    # Structured ma'lumotlar borligini tekshiramiz
    lesson_hour = data.get("lesson_hour")
    group = data.get("group")
    subject = data.get("subject")
    lesson_time = data.get("time")

    if lesson_hour or group or subject or lesson_time:
        lines: list[str] = []
        if lesson_hour:
            lines.append(f"⏰ <b>Dars soati:</b> {lesson_hour}")
        if group:
            lines.append(f"📋 <b>Guruh:</b> {group}")
        if subject:
            lines.append(f"📖 <b>Fan:</b> {subject}")
        if lesson_time:
            lines.append(f"🕐 <b>Vaqt:</b> {lesson_time}")

        header = "\n".join(lines)
        return (
            "🔔 <b>Dars boshlandi!</b>\n\n"
            f"{header}\n\n"
            f"{text}\n\n"
            "✅ Iltimos, QR kodni skanerlang!"
        )

    # Oddiy matn — chiroyli saralash
    return (
        "🔔 <b>Yangi dars xabari!</b>\n\n"
        f"{text}\n\n"
        "✅ Iltimos, QR kodni skanerlang!"
    )
