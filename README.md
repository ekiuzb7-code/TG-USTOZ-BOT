# UstozNazorat Telegram Bot

Maktab davomat tizimi uchun professional Telegram bot (aiogram 3.x, Supabase, Railway).

## Loyiha tuzilishi

```text
telegram-bot/
├── bot/
│   ├── __init__.py
│   ├── config.py         # pydantic-settings orqali .env o'qish
│   ├── database.py       # Supabase REST client (httpx async)
│   ├── handlers.py       # /start, /status, /myid, /help + on_startup
│   └── keyboards.py      # WebApp inline tugmalari
├── main.py               # Botni ishga tushirish, logger va graceful shutdown
├── requirements.txt
├── Procfile              # Railway worker: python main.py
├── runtime.txt           # python-3.11.9
├── .env.example
└── README.md
```

## Railway'da deploy qilish

1. Reponi Railway ga ulang (**Deploy from GitHub repo**).
2. **Variables** bo'limiga quyidagini kiriting:
   - `BOT_TOKEN` — `@BotFather`dan olgan token
   - `WEBAPP_URL` — `https://maktabos370.lovable.app`
   - `SUPABASE_URL` — `https://jmjwvvdooaosgldzvmdv.supabase.co`
   - `SUPABASE_KEY` — Supabase publishable (anon) kalit
3. Railway avtomatik qurib, `python main.py` sifatida ishga tushiradi.

## @BotFather sozlash (menubutton tugmasi)

1. `@BotFather`ga `/setmenubutton` yuboring.
2. Botingizni tanlang.
3. Havola sifatida `https://maktabos370.lovable.app` ni kiriting.
4. Tugma nomiga `📱 Mini App` deb yozing.

Shundan so'ng botning chap pastki menyusida WebApp tugmasi chiqadi.

## Buyruqlar

- `/start` — botni ishga tushirish va Mini App'ni ochish (foydalanuvchi tizimda bo'lsa ism bilan, bo'lmasa kirish tugmasi bilan)
- `/status` — Telegram ID, username va tizimga bog'lanish holati
- `/myid` — Telegram ID nusxalash quvvatli formatda
- `/help` — qisqa foydalanish qo'llanmasi

## .env tayyorlash

```bash
cp .env.example .env
# .env ichidagi qiymatlarni o'zingizning ma'lumotlaringiz bilan o'zgartiring
```

## Lokal ishlatish

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# yoki: source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
python main.py
```

## Ma'lumotlar bazasi jadvallari

Supabase'da quyidagi jadvallar bo'lishi kerak:

- `public.telegram_links(user_id UUID PK, telegram_id BIGINT UNIQUE NOT NULL, username TEXT, linked_at TIMESTAMPTZ)`
- `public.profiles(id UUID, full_name TEXT, avatar_url TEXT)`

`/start` handleri `telegram_links` jadvalidan `telegram_id` bo'yicha qidiradi va `profiles` bilan JOIN qilib `full_name` oladi.
