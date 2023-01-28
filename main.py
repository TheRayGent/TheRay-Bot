import disnake
from disnake.ext import commands

import os
from dotenv import dotenv_values

config = dotenv_values("token.env")

bot = commands.Bot(command_prefix="!", help_command=None, intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print("Бот готов!")

bot_token = config["bot_token"]
bot.run(bot_token)