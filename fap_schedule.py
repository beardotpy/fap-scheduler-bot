import os
import discord
from tabulate import tabulate
from db_functions import *
from discord.ext import commands, menus
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
HEADERS = ["Fap Id", "Coomer", "Date", "Time"]
TABLEFMT = "fancy_grid"

class TableSource(menus.ListPageSource):
    async def format_page(self, menu, entries):
        return f"```{tabulate(entries, headers=HEADERS, tablefmt=TABLEFMT)}```"

def paginate(entries):
    for i in range(0, len(entries), 10): 
        yield entries[i:i + 10]

bot = commands.Bot(command_prefix=["c!", "cum"], intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} is ready.")

@bot.command(aliases=["cum", "nut"])
async def fap(ctx):
    add_fap(ctx.author)
    await ctx.reply("You did the deed. Nice.")

@bot.command(aliases=["unnut", "uncum"])
async def unfap(ctx, fap_id=None):
    try:
        remove_fap(ctx.author, fap_id)
    except:
        await ctx.send("No fap to remove, fap id doesn't exist, or you tried to unfap someone else's fap.")
    else:
        await ctx.send(f"Unfapped.")

@bot.command(aliases=["stat", "stats"])
async def faps(ctx, member:discord.Member=None):
    if member == None:
        member = ctx.author
    faps = get_faps(member)
    if not faps:
        await ctx.send("No fap data to show.")
        return
    formatter = TableSource(faps, per_page=10)
    menu = menus.MenuPages(formatter)
    await menu.start(ctx)

@bot.command()
async def allfaps(ctx):
    faps = get_faps()
    if not faps:
        await ctx.send("No fap data to show.")
        return
    formatter = TableSource(faps, per_page=10)
    menu = menus.MenuPages(formatter)
    await menu.start(ctx)

bot.run(TOKEN)