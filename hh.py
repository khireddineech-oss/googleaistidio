# -*- coding: utf-8 -*-
"""
بوت تلغرام لحل الصناديق الخضراء (Google Play Points)
يشغل على VPS بشكل دائم بدون بروكسي
"""

import asyncio
import logging
import os
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message

# ============ الإعدادات ============
API_ID = 37519095
API_HASH = "e488aa7ef4d13488389a2d40ae991824"
BOT_TOKEN = "9111783827:AAGHhCuPmvNjhpTW527zRnEEUtpp7oCCmkc"

# ============ تشغيل اللوج ============
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ============ إنشاء البوت ============
app = Client(
    "play_points_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=100,
    in_memory=True,
)


# ============ أوامر البوت ============
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    text = (
        "**👋 أهلاً بك في بوت حل الصناديق الخضراء**\n\n"
        "🎁 هذا البوت مخصص لمساعدة مستخدمي **Google Play Points**\n"
        "على متابعة وحل الصناديق الخضراء.\n\n"
        "**الأوامر المتاحة:**\n"
        "• `/start` - بدء البوت\n"
        "• `/help` - المساعدة\n"
        "• `/status` - حالة البوت\n"
        "• `/time` - التوقيت الحالي\n\n"
        f"🆔 **آيدي الخاص بك:** `{message.from_user.id}`"
    )
    await message.reply_text(text)


@app.on_message(filters.command("help") & filters.private)
async def help_cmd(client: Client, message: Message):
    text = (
        "**📖 المساعدة**\n\n"
        "هذا البوت يساعدك في متابعة صناديق **Play Points** الخضراء.\n\n"
        "**خطوات الاستخدام:**\n"
        "1. افتح تطبيق Google Play\n"
        "2. ادخل على قسم Play Points\n"
        "3. ابحث عن الصناديق الخضراء\n"
        "4. استخدم البوت للتفاعل معها\n\n"
        "**ملاحظة:** البوت يعمل 24/7 على VPS."
    )
    await message.reply_text(text)


@app.on_message(filters.command("status") & filters.private)
async def status_cmd(client: Client, message: Message):
    uptime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    me = await client.get_me()
    text = (
        "**🟢 البوت يعمل بشكل طبيعي**\n\n"
        f"🤖 **اسم البوت:** @{me.username}\n"
        f"🆔 **آيدي البوت:** `{me.id}`\n"
        f"⏰ **الوقت:** `{uptime}`\n"
        "💻 **الاستضافة:** VPS\n"
        "🔌 **البروكسي:** بدون"
    )
    await message.reply_text(text)


@app.on_message(filters.command("time") & filters.private)
async def time_cmd(client: Client, message: Message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await message.reply_text(f"⏰ **الوقت الحالي:** `{now}`")


@app.on_message(filters.text & filters.private)
async def echo_handler(client: Client, message: Message):
    if message.text.startswith("/"):
        return
    await message.reply_text(
        f"📩 استلمت رسالتك:\n\n`{message.text}`\n\n"
        "استخدم /help لمعرفة الأوامر المتاحة."
    )


# ============ التشغيل ============
async def main():
    logger.info("🚀 بدء تشغيل البوت...")
    await app.start()
    me = await app.get_me()
    logger.info(f"✅ البوت شغال: @{me.username} (ID: {me.id})")
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        app.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 تم إيقاف البوت")