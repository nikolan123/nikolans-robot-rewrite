import discord
from discord.ext import commands
import csv
import aiofiles
import random

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
                    
    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="95cdkey", description="Generates a Windows 95 CD Key.")
    async def nfcdkey(self, ctx):
        #gen site num
        forbidden_site_numbers = [333, 444, 555, 666, 777, 888, 999]
        site_number = str(random.choice([x for x in range(999) if x not in forbidden_site_numbers])).zfill(3)
        #gen 2nd segment
        valid_last_digit = False
        while not valid_last_digit:
            second_segment = str(random.randint(0, 999999)).zfill(7)
            digit_sum = sum(int(digit) for digit in second_segment)
            valid_last_digit = digit_sum % 7 == 0 and int(second_segment[-1]) not in [0, 8, 9]
        cd_key = f"{site_number}-{second_segment}"

        #check
        s = cd_key.split('-')

        if len(cd_key) > 1 and s[0].isdigit() and s[1].isdigit():
            forbidden_site_numbers = ['333', '444', '555', '666', '777', '888', '999']
            if s[0] not in forbidden_site_numbers:
                digit_sum = sum(int(digit) for digit in s[1])
                if digit_sum % 7 == 0:
                    if cd_key[-1] != '0' and cd_key[-1] not in ['8', '9']:
                        embed = discord.Embed(title="Windows 95 CD Key", color=0x2494A1, description=f"{cd_key}")
                        embed.set_footer(text=f"Requested by {ctx.author.name} | api.nikolan.xyz/95cdkey")
                        embed.set_thumbnail(url="https://64.media.tumblr.com/f0b0786998dc2e44bfe179e9da3fa116/39dad773e2bb50bc-4c/s540x810/3534cc436c2b90f526bd483f632d0ff804a80e7b.gif")
                        return await ctx.respond(embed=embed)
        return await ctx.respond(discord.Embed(color=discord.Color.red(), title="Error", description="Error validating key, please try again"))

def setup(bot):
    bot.add_cog(winkeyss(bot))
