import os
from pyrogram import Client as Bot

from ZeroTwo.config import API_HASH, API_ID, BOT_TOKEN
from ZeroTwo.services.callsmusic import run


bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="ZeroTwo.modules"),
)

bot.start()
run()
