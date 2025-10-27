import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import eventParser
import datetime
import zoneinfo

local_tz = zoneinfo.ZoneInfo("Europe/Zagreb")
morningNotif = datetime.time(hour=8, minute=0, second=0, tzinfo=local_tz)

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

def get_today_message(day):
    calendar = open("calendar.ics", "r")
    eventList = eventParser.parse_ics(calendar)
    calendar.close()
    target_date = datetime.datetime.now(local_tz) + datetime.timedelta(days=day)
    day_date = target_date.strftime("%d.%m.%y")
    day_of_week = target_date.strftime("%A")
    return f'For {day_of_week} ({day_date}): \n {eventParser.formatEvents(eventParser.getEventsInDay(eventList, day))}'

@bot.event
async def on_ready():
    print(f"Current local time: {datetime.datetime.now(local_tz)}")
    print(f"Task scheduled for: {morningNotif}")
    daily_notification.start()

@tasks.loop(time=morningNotif)
async def daily_notification():
    channel = bot.get_channel(1430302930556158002)
    await channel.send(get_today_message(0))

@bot.command()
async def day(ctx, arg):
    if ctx.author == bot.user:
        return
    try:
        day_offset = int(arg)
        await ctx.send(get_today_message(day_offset))
    except ValueError:
        await ctx.send("Please provide a valid number (e.g., !day 0)")
    
bot.run(token, log_handler=handler, log_level=logging.DEBUG)