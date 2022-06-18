import os
from re import L
import discord
from tabulate import tabulate
from db_functions import *
from discord.ext import commands, menus
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
HEADERS = ["Fap Id", "Coomer", "Date", "Time"]
TABLEFMT = "fancy_grid"
TIMEZONES = {
    "GMT":  "",
    "UTC":  "",
    "ECT":  "+1:00",
    "EET":  "+2:00",
    "ART":  "+2:00",
    "EAT":  "+3:00",
    "MET":  "+3:30",
    "NET":  "+4:00",
    "PLT":  "+5:00",
    "IST":  "+5:30",
    "BST":  "+6:00",
    "VST":  "+7:00",
    "CTT":  "+8:00",
    "JST":  "+9:00",
    "ACT":  "+9:30",
    "AET": "+10:00",
    "SST": "+11:00",
    "NST": "+12:00",
    "NST": "+12:00",
    "MIT": "-11:00",
    "HST": "-10:00",
    "AST": "-9:00",
    "PST": "-8:00",
    "PNT": "-7:00",
    "MST": "-7:00",
    "CST": "-6:00",
    "EST": "-5:00",
    "IET": "-5:00",
    "PRT": "-4:00",
    "CNT": "-3:30",
    "AGT": "-3:00",
    "BET": "-3:00",
    "CAT": "-1:00"
}

class TableSource(menus.ListPageSource):
    async def format_page(self, menu, entries):
        return f"```{tabulate(entries, headers=HEADERS, tablefmt=TABLEFMT)}```"

bot = commands.Bot(command_prefix=["c!", "cum", "cum "], intents=discord.Intents.all())

def convert_to_sqlite_modifier(offset):
    if not offset:
        return None
    sign = offset.lstrip()
    offset = offset.lstring()
    hours, minutes = offset.split(":")
    return (sign, hours, minutes)

def paginate(entries):
    for i in range(0, len(entries), 10): 
        yield entries[i:i + 10]

async def user_check(ctx):
    if get_user(ctx.author):
        return True
    await ctx.send("Please first set your timezone with the `timezone` command.\nExample: `c!timezone [your_timezone]`\nRefer to this website for a list of timezones if needed: https://publib.boulder.ibm.com/tividd/td/TWS/SC32-1274-02/en_US/HTML/SRF_mst273.htm")
    return False

@bot.event
async def on_ready():
    print(f"{bot.user} is ready.")

@bot.command()
async def timezone(ctx, timezone):
    if get_user(ctx.author):
        change_timezone(ctx.author, timezone)
        await ctx.send("Updated your timezone.")
        return
    elif timezone.upper() not in TIMEZONES.keys():
        await ctx.send("Invalid timezone. Refer to this for a list of valid timezeons.\nhttps://publib.boulder.ibm.com/tividd/td/TWS/SC32-1274-02/en_US/HTML/SRF_mst273.htm")
        return
    add_user(ctx.author, timezone)
    await ctx.reply("Officially registered coomer.")

@bot.command(aliases=["cum", "nut"])
async def fap(ctx):
    user_check = await user_check(ctx)
    if not user_check:
        return
    add_fap(ctx.author)
    await ctx.reply("You did the deed. Nice.")

@bot.command(aliases=["unnut", "uncum"])
async def unfap(ctx, fap_id=None):
    user_check = await user_check(ctx)
    if not user_check:
        return
    try:
        remove_fap(ctx.author, fap_id)
    except:
        await ctx.send("No fap to remove, fap ID doesn't exist, or you tried to unfap someone else's fap.")
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

@bot.command(aliases=["allstat", "allstats"])
async def allfaps(ctx):
    faps = get_faps()
    if not faps:
        await ctx.send("No fap data to show.")
        return
    formatter = TableSource(faps, per_page=10)
    menu = menus.MenuPages(formatter)
    await menu.start(ctx)

bot.run(TOKEN)