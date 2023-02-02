#from keep_alive import keep_alive
#import time

import disnake
from disnake.ext import commands

import os
from dotenv import dotenv_values
from datetime import datetime

config = dotenv_values("config.env")

bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())

CENSORED_WORDS = ['даун','пидор','пидар','гандон','петушар', 'ебальник']


@bot.event
async def on_ready():
    print("Бот работает")
    """while True:
                     time_t=str(datetime.now())
                     time_t=time_t[11:16]
                     await bot.change_presence(activity = disnake.Activity(name = f'время {time_t}', type = disnake.ActivityType.watching))
                     time.sleep(60)"""

@bot.event
async def on_message(message):
    count=False
    content = message.content
    for censored_words in CENSORED_WORDS:
        content_l=content.lower()
        if content_l.count(censored_words)>0 and count==False:
            count=True
            await message.delete()
            await message.channel.send(f'{message.author.mention} написал в сообщении плохое слово!')

@bot.event
async def on_message_edit(before, after):
    count=False
    content = after.content
    for censored_words in CENSORED_WORDS:
        content_l=content.lower()
        if content_l.count(censored_words)>0 and count==False:
            count=True
            await after.delete()
            await after.channel.send(f'{after.author.mention} написал в сообщении плохое слово!')



@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel

    embed = disnake.Embed(
        title="Новый участник!",
        description=f"{member.mention}",
        color=0xDA5B00,
        timestamp=datetime.now()
    )
    embed.set_author(
        name=f"{member.name}#{member.discriminator}",
        icon_url=str(member.display_avatar.url)
    )

    embed.set_thumbnail(url=str(member.display_avatar.url))
    await channel.send(embed=embed)



@bot.slash_command(description='Удаление нужного кол-ва сообщений')
async def clear(inter, amount: int = commands.Param(name='кол-во', description='Напишите нужное кол-во')):
    await inter.channel.purge(limit=amount)
    amount=str(amount)
    am=amount[-2::]
    am1=amount[-1]
    if am=='11' or am=='12' or am =='13' or am=='14':
        end='ий'
    else:
        if am1=='1': end='ие'
        elif am1=='2' or am1=='3' or am1=='4': end='ия'
        else: end='ий'
    await inter.response.send_message(f"Удалено {amount} сообщен{end}", ephemeral=True, delete_after=5)


@bot.slash_command(description='Выбор статуса/активности для бота')
async def activity(inter: disnake.AppCmdInter,
    a_type: str = commands.Param(None, name='активность', description='Выберите активность', 
        choices=['"Слушает"', '"Играет"', '"Смотрит"', '"Без активности"']),
    a_text: str = commands.Param(None, name='текст', description='Напишите текст статуса')
):
    if a_type=='"Слушает"': a_type=disnake.ActivityType.listening, a_name=name
    elif a_type=='"Играет"': a_type=disnake.ActivityType.playing
    elif a_type=='"Смотрит"': a_type=disnake.ActivityType.watching
    elif a_type=='"Без активности"': a_type=disnake.ActivityType.unknown

    await bot.change_presence(activity = disnake.Activity(name = f'{a_text}', type = a_type))
    await inter.response.send_message('Статус бота изменён!', ephemeral=True, delete_after=3)



@bot.slash_command(description='Отправка любого сообщения в любой канал данного сервера от имени бота')
async def message(ctx,
    text_message: str = commands.Param(name='сообщение', description = 'Напишите текст сообщения'),
    channel_mention: disnake.abc.GuildChannel = commands.Param(None, name='канал', description = 'Выберите канал, в который хотите отправить сообщение')
):
    if channel_mention!=None:
        if channel_mention == bot.get_channel(ctx.channel.id):
            await ctx.response.send_message('Сообщение отправленно!', ephemeral=True, delete_after=1)
        else:
            channel = disnake.utils.get(ctx.guild.channels, name = str(channel_mention))
            await ctx.response.send_message(f'Сообщение ***"{text_message}"*** отправленно в канал {channel.mention}', ephemeral=True)
        await channel_mention.send(text_message)

    elif channel_mention==None:
        channel_send = bot.get_channel(ctx.channel.id)
        await ctx.response.send_message('Сообщение отправленно!', ephemeral=True, delete_after=1)
        await channel_send.send(text_message)



"""@bot.slash_command(description='Отправка любого сообщения в любой канал данного сервера от имени бота')
async def old_message(ctx,
    text_message: str = commands.Param(name='сообщение', description = 'Напишите текст сообщения'),
    channel_name = commands.Param(None, name='канал', description = 'Напишите название канала, в который хотите отправить сообщение')
):
    for channel in ctx.guild.channels:
        if channel.name == channel_name:
            channel_id = channel.id
            break
    if channel_name!=None:   
        channel_send = bot.get_channel(channel_id)
        await ctx.response.send_message(f'Сообщение "{text_message}" отправленно в канал "{channel_send}"', ephemeral=True)
        await channel_send.send(text_message)
    elif channel_name==None:    
        channel_send = bot.get_channel(ctx.channel.id)
        await ctx.response.send_message('Сообщение отправленно!', ephemeral=True)
        await channel_send.send(text_message)"""



#keep_alive()
bot_token = config["bot_token"]
bot.run(bot_token)