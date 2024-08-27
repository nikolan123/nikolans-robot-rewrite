import discord

bot = discord.Bot(intents=discord.Intents.all())

def readconfigfile(path):
    #Make dicts global
    global hooks_dict, options_dict

    # Set up reader
    import configparser
    config = configparser.RawConfigParser()

    # Read options section of config file, add it to dict
    try:
        config.read(path)
        hooks_dict = dict(config.items('WEBHOOKS'))
    except Exception:
        print("[INIT] Config file malformed: Error while reading Tokens section! The file may be missing or malformed.")
        exit()

    # Read path section of config file, add it to dict
    try:
        config.read(path)
        options_dict = dict(config.items('OPTIONS'))
    except Exception:
        print("[INIT] Config file malformed: Error while reading Options section! The file may be missing or malformed.")
        exit()

print("[INIT] Reading config files.")

# Read config files
readconfigfile('config.cfg')

# Config File Vars
try:
    bot.logginghook = hooks_dict['logging-hook']
    bot.logginghookname = hooks_dict['logging-hook-name']
    bot.suggestionshook = hooks_dict['suggestions-hook']
    
    bot.botToken = str(options_dict['bot-token'])
    bot.dbgAccess = options_dict['dbg-access'].split(",")
    bot.supportserver = options_dict['support-server']
    bot.ownername = options_dict['owner-name']
    bot.steamkey = options_dict['steam-key']
    bot.spotify_id = options_dict['spotify-id']
    bot.spotify_secret = options_dict['spotify-secret']
except Exception as error:
    print("[INIT] Bad value in config file! Exiting.")
    print(error)
    exit()

# code for the blacklist check
blacklisted = []

def reloadbl(): # function to refresh the blacklisted user list
    global blacklisted
    with open("data/blusers", 'r') as blfiles:
        blacklisted = blfiles.readlines()
bot.reloadbl = reloadbl
reloadbl() # run once before bot startup

@bot.check # will run before every command is executed
async def blacklist_check(ctx):
    global blacklisted
    if str(ctx.author.id) in str(blacklisted): # checks if user is blacklisted
        embed = discord.Embed(color=0xff0000, title="You have been blocked from using this bot!", description=f"If you think this was a mistake, join the [Discord Server]({bot.supportserver}) or DM @{bot.ownername}.")
        await ctx.respond(embed=embed, ephemeral=True)
        return False # tells command not to execute
    return True

cogs = ['ping', 'ai', 'gimsa', 'dbg', 'apicmds', 'logging', "animals", 'steam', 'winkeys', 'help', 'suggestions', 'mc', 'song']
for h in cogs:
    try:
        bot.load_extension(f"cogs.{h}")
        print(f"Loaded extension {h}")
    except Exception as e:
        print(f"Failed to load extension {h}: {e}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

try:
    bot.run(bot.botToken)
except Exception as e:
    print(f"Error starting bot: {e}")