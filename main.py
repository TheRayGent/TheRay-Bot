import disnake
from disnake.ext import commands

import os
from dotenv import dotenv_values

config = dotenv_values("config.env")

bot = commands.Bot(command_prefix=config["prefix"], intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print("Бот работает")

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel

    embed = disnake.Embed(
        title="Новый участник!",
        description=f"{member.mention}",
        color=0xDA5B00
    )

    embed.set_thumbnail(url=str(member.display_avatar.url))

    await channel.send(embed=embed)

@bot.slash_command(name='пинг', description='хз')
async def ping(inter):
    await inter.response.send_message("Понг!", ephemeral=True)

@bot.slash_command(name='сообщение', description='Отправка сообщения в любой канал от имени бота')
async def channel_message(member, *, channel_name=None, message=None):
    for channel in member.guild.channels:
        if channel.name == channel_name:
            channel_id = channel.id

    if channel_name!=None:
        channel_send = bot.get_channel(channel_id)

        if message==None:
            await member.response.send_message("Нельзя отправить пустое сообщение!", ephemeral=True)
        else:
            await member.response.send_message(f'Сообщение "{message}" отправленно в канал "{channel_send}"', ephemeral=True)
            await channel_send.send(message)
    elif channel_name==None:
        if message==None:
            await member.response.send_message("Нельзя отправить пустое сообщение!", ephemeral=True)
        else:
            await member.send(message)

bot_token = config["bot_token"]
bot.run(bot_token)