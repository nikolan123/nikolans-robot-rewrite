import discord
from discord.ext import commands
import csv
import aiofiles

async def getoss(ctx):
    data = []
    async with aiofiles.open('data/winkeys.csv', mode='r') as csvfile:
        reader = csv.reader(await csvfile.readlines())
        for row in reader:
            if ctx.options['version'].lower() == 'windows':
                return ['Ubuntu 20.04', 'Debian Bookworm', 'Linux Mint 21.3']
            if row and ctx.options['version'].lower() in row[0].lower():
                data.append(row[0])
        return data

class winkeyss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="winkey", description="Returns a Generic Windows Key.")
    async def winkeycmd(self, ctx, the: discord.Option(str, name="version", description="The Windows version to get a key for", autocomplete=getoss)): # type: ignore
        async with aiofiles.open('data/winkeys.csv', mode='r') as csvfile:
            reader = csv.reader(await csvfile.readlines())
            for row in reader:
                if row and the == row[0]:
                    embed = discord.Embed(colour=0x00b0f4, title=row[0], description=f"Your key is **{row[1]}**")
                    embed.set_footer(text='All information provided by this command is legal and not considered piracy, the keys do not activate Windows and are taken from an official Microsoft page (learn.microsoft.com/windows-server/get-started/kms-client-activation-keys).')
                    await ctx.respond(embed=embed)
                    return
        
        embed = discord.Embed(title = "Not Found", description = f"Please use an available option.")
        embed.color = discord.Colour.red()
        await ctx.respond(embed=embed, ephemeral=True)
                    

def setup(bot):
    bot.add_cog(winkeyss(bot))
