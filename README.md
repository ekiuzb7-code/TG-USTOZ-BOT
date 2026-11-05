# UstozNazorat Telegram Bot

Maktab davomat tizimi uchun professional Telegram bot (aiogram 3.x, aiohttp, Railway).

## Loyiha tuzilishi

```text
telegram-bot/
├── bot/
│   ├── __init__.py
│   ├── api_client.py    # aiohttp orqali Maktab API bilan aloqa
│   ├── config.py        # pydantic-settings orqali .env o'qish
│   ├── handlers.py      # /start, /myid + on_startup
│   └── keyboards.py     # WebApp inline tugmalari
├── main.py              # Botni ishga tushirish, logger va graceful shutdown
├── start.bat            # Lokalda botni ishga tushirish (Windows)
├── stop.bat             # Lokalda botni to'xtatish (Windows)
├── requirements.txt
├── Procfile             # Railway worker: python main.py
├── runtime.txt          # python-3.11
├── .env.example
└── README.md
```

## O'zgaruvchilar (.env)

| O'zgaruvchi | Tavsiy qiymati |
|-------------|----------------|
| `BOT_TOKEN` | `@BotFather`dan olgan bot token |
| `WEBAPP_URL` | `https://maktabos370.lovable.app/scan` |
| `API_BASE_URL` | `https://maktabos370.lovable.app` |
| `BOT_API_SECRET` | Maktab API uchun secret kalit |

```bash
cp .env.example .env
# .env ichidagi qiymatlarni o'zingizning ma'lumotlaringiz bilan o'zgartiring
```

## Railway'da deploy qilish

1. Reponi Railway ga ulang (**Deploy from GitHub repo**).
2. **Variables** bo'limiga 4 ta o'zgaruvchini kiriting:
   - `BOT_TOKEN`
   - `WEBAPP_URL`
   - `API_BASE_URL`
   - `BOT_API_SECRET`
3. Railway avtomatik qurib, `python main.py` sifatida ishga tushiradi.

## @BotFather sozlash (menubutton tugmasi)

1. `@BotFather`ga `/setmenubutton` yuboring.
2. Botingizni tanlang.
3. Havola sifatida `https://maktabos370.lovable.app/scan` ni kiriting.
4. Tugma nomiga `📱 Mini App` deb yozing.

## Buyruqlar

- `/start` — API orqali ro'yxatdan o'tganligini tekshiradi. Ro'yxatdan o'tgan bo'lsa `📷 Skanerlash` tugmasi bilan Mini App'ga yollaydi. Ro'yxatdan o'tmagan bo'lsa Telegram ID bilan xabar beradi.
- `/myid` — Sizning Telegram ID raqamingiz.

## Lokal ishlatish (Windows)

```cmd
start.bat
```

To'xtatish uchun:

```cmd
stop.bat
```

## Xavfsizlik

- `BOT_API_SECRET` va `BOT_TOKEN` logga chiqarmaslik kerak.
- Supabase'ga to'g'ridan-to'g'ri ulanish yo'q — barcha so'rovlar Maktab API orqali o'tadi.
