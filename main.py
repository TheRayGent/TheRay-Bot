import disnake
from disnake.ext import commands

import os
from dotenv import dotenv_values

config = dotenv_values("config.env")

bot = commands.Bot(command_prefix=config["prefix"], intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print("Бот работает")

bot_token = config["bot_token"]
bot.run(bot_token)