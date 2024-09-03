import discord
from discord.ext import commands
import csv
import aiofiles
import random
from datetime import datetime, timedelta


class winkeyss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        with open('data/winkeys.csv', mode='r') as csvfile:
            self.winkeyreader = list(csv.reader(csvfile))

    async def getoss(self, ctx):
        data = []
        for row in self.winkeyreader:
            if row and ctx.options['version'].lower() in row[0].lower():
                data.append(row[0])
        return data

    keygroup = discord.SlashCommandGroup(name="key", integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install})

    @keygroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="windows", description="Returns a Generic Windows Key.")
    async def windows_key_command(self, ctx, the: discord.Option(str, name="version", description="The Windows version to get a key for", autocomplete=getoss)): # type: ignore
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
                    
    @keygroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="windows95cd", description="Generates a Windows 95 CD Key.")
    async def win95cd_command(self, ctx):
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
    
    @keygroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="windows95oem", description="Generates a Windows 95 OEM Key.")
    async def win95oem_command(self, ctx):
        #gen first segment
        day_of_year = random.randint(1, 366)
        year_suffix = random.randint(95, 103)
        first_segment = f"{day_of_year:03d}{year_suffix:02d}"

        year_full = 1900 + year_suffix if year_suffix >= 95 else 2000 + year_suffix
        date = datetime(year_full, 1, 1) + timedelta(days=day_of_year - 1)
        readable_date = date.strftime("%d %B %Y")

        #gen 3rd segment
        valid_last_digit = False
        while not valid_last_digit:
            third_segment = str(random.randint(0, 999999)).zfill(6)
            third_segment = '0' + third_segment
            digit_sum = sum(int(digit) for digit in third_segment)
            valid_last_digit = digit_sum % 7 == 0 and int(third_segment[-1]) not in [0, 8, 9]
        
        cd_key = f"{first_segment}-OEM-{third_segment}-{''.join(str(random.randint(0, 9)) for _ in range(5))}"

        embed = discord.Embed(title="Windows 95 OEM Key", color=0x2494A1, description=f"{cd_key}\nKey printed on {readable_date}")
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        embed.set_thumbnail(url="https://64.media.tumblr.com/f0b0786998dc2e44bfe179e9da3fa116/39dad773e2bb50bc-4c/s540x810/3534cc436c2b90f526bd483f632d0ff804a80e7b.gif")
        return await ctx.respond(embed=embed)

    @keygroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="office97", description="Generates an Office 97 Key.")
    async def office97_command(self, ctx):
        #gen 1st segment
        digit3 = random.randint(0, 9)
        digit4 = (digit3 + random.choice([1, 2])) % 10
        first_segment=f"{random.randint(0, 9)}{random.randint(0, 9)}{digit3}{digit4}"
        #gen 2nd segment
        valid_last_digit = False
        while not valid_last_digit:
            second_segment = str(random.randint(0, 999999)).zfill(7)
            digit_sum = sum(int(digit) for digit in second_segment)
            valid_last_digit = digit_sum % 7 == 0 and int(second_segment[-1]) not in [0, 8, 9]
        cd_key = f"{first_segment}-{second_segment}"

        embed = discord.Embed(title="Office 97 Key", color=0x2494A1, description=f"{cd_key}")
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Office_95_and_97_logo.svg/800px-Office_95_and_97_logo.svg.png")
        return await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(winkeyss(bot))
