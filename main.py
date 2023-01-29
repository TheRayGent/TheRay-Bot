import disnake
from disnake.ext import commands

import os
from dotenv import dotenv_values

config = dotenv_values("config.env")

bot = commands.Bot(command_prefix=config["prefix"], intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print("Бот работает")

@bot.slash_command(name='пинг', description='хз')
async def ping(inter):
    await inter.response.send_message("Понг!", ephemeral=True)

bot_token = config["bot_token"]
bot.run(bot_token)