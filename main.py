import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import eventParser

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    
@bot.command()
async def today(ctx):
    if ctx.author == bot.user:
        return

    await ctx.send(f'For Today You have: ') #eventParser.get_today() not finished yet

    
    
bot.run(token, log_handler=handler, log_level=logging.DEBUG)