import discord
from discord.ext import commands
import datetime
import os

intents = discord.Intents.default()
intents.presences = True  # Видеть активность пользователей
intents.members = True  # Видеть участников сервера
intents.dm_messages = True  # Отправлять ЛС

bot = commands.Bot(command_prefix="/", intents=intents)

user_activities = {}
users_being_tracked = set()  # Множество для отслеживаемых пользователей

@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен!')

@bot.event
async def on_presence_update(before, after):
    user_id = after.id

    if user_id not in users_being_tracked:  # Бот отслеживает только выбранных пользователей
        return

    if after.activities:
        for activity in after.activities:
            if isinstance(activity, discord.Game) or isinstance(activity, discord.Streaming) or isinstance(activity, discord.CustomActivity) or isinstance(activity, discord.Spotify) or isinstance(activity, discord.Soundcloud):
                activity_name = activity.name
                if user_id not in user_activities or user_activities[user_id]["activity"] != activity_name:
                    user_activities[user_id] = {
                        "activity": activity_name,
                        "start_time": datetime.datetime.now(),
                        "user_name": after.name  # Сохраняем имя пользователя
                    }
    else:
        if user_id in user_activities:
            start_time = user_activities[user_id]["start_time"]
            activity_name = user_activities[user_id]["activity"]
            time_spent = datetime.datetime.now() - start_time
            end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
            total_time = str(time_spent).split('.')[0]  # Отформатируем общее время (без миллисекунд)
            user_name = user_activities[user_id]["user_name"]
            del user_activities[user_id]

            user = after
            try:
                await user.send(f'@{user_name} - @{activity_name} / {start_time_str} {end_time} {total_time}')
            except discord.Forbidden:
                print(f'Не удалось отправить ЛС {user.name}')

@bot.command()
async def start(ctx, member: discord.Member):
    """Команда для начала отслеживания пользователя"""
    if member.id in users_being_tracked:
        await ctx.send(f'Я уже слежу за участником {member.name}')
    else:
        users_being_tracked.add(member.id)
        await ctx.send(f'Начал следить за участником @{member.name}')

@bot.command()
async def stop(ctx, member: discord.Member):
    """Команда для остановки отслеживания пользователя"""
    if member.id not in users_being_tracked:
        await ctx.send(f'Я не слежу за участником {member.name}')
    else:
        users_being_tracked.remove(member.id)
        await ctx.send(f'Перестал следить за участником @{member.name}')

bot.run(os.getenv("MTM1NDk5OTc3ODUzNDEwMTI3NA.GGnPCV.s3-8erCPR0xHGgkDVoV6ge6mo3DcM2d9Hg3pIg"))