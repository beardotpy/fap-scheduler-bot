import os
import discord
import sqlite3
from db_functions import *
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} is ready.")

@bot.command()
async def fap(ctx):
    add_user(ctx.author)
    await ctx.send("i did the thing")

bot.run(TOKEN)