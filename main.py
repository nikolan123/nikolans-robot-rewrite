import discord
from discord.ext import commands
import logging

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

bot = discord.Bot(intents=discord.Intents.all())

bot.rulers = ["767780952436244491", "1118973285766533250"]
bot.logginghook = "https://discord.com/api/webhooks/f"
bot.logginghookname = "nikolan's robot logging"
bot.supportserver = "https://discord.gg/rgYmNt5BSg"
bot.ownername = "nikolan"

@bot.check
async def blacklist_check(ctx):
    with open('data/blusers', "r") as bllist:
        blacklisted = bllist.readlines()
    embed = discord.Embed(color=0xff0000, title="You have been blocked from using this bot!", description=f"If you think this was a mistake, join the [Discord Server]({bot.supportserver}) or DM @{bot.ownername}.")
    if str(ctx.author.id) in str(blacklisted):
        await ctx.respond(embed=embed, ephemeral=True)
        return False
    return True
cogs = ['ping', 'ai', 'gimsa', 'dbg', 'apicmds', 'logging', "animals", 'steam', 'winkeys']
for h in cogs:
    try:
        bot.load_extension(f"cogs.{h}")
        print(f"Loaded extension {h}")
    except Exception as e:
        print(f"Failed to load extension {h}: {e}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

bot.run("f")
