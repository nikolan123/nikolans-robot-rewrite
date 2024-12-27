import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import aiohttp
import random
import json
import aiofiles
import urllib.parse

class animalz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    animalgroup = discord.SlashCommandGroup(name="animals", integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install})

    @animalgroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="doggo", description="Sends a random dog picture.")
    @commands.cooldown(1, 3, BucketType.user)
    async def doggo_command(self, ctx):
        endpoint = "https://dog.ceo/api/breeds/image/random"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    doglink = data["message"]
                    embed = discord.Embed(title="Doggo found!", image=doglink)
                    embed.set_footer(text=f"Requested by {ctx.author.name}")
                    await ctx.respond(embed=embed)
                else:
                    embed = discord.Embed(title = "Error", description = "Failed to fetch data from the API.")
                    embed.add_field(name = "Status Code", value = response.status)
                    embed.color = discord.Colour.red()
                    await ctx.respond(embed=embed)
    
    @animalgroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="dogfact", description="Sends a random dog fact.")
    @commands.cooldown(1, 3, BucketType.user)
    async def dogfact_command(self, ctx):
        endpoint = "https://dogapi.dog/api/v2/facts"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    fact = data["data"][0]["attributes"]["body"]
                    embed = discord.Embed(title="Dog fact", description=fact)
                    embed.set_footer(text=f"Requested by {ctx.author.name}")
                    await ctx.respond(embed=embed)
                else:
                    embed = discord.Embed(title = "Error", description = "Failed to fetch data from the API.")
                    embed.add_field(name = "Status Code", value = response.status)
                    embed.color = discord.Colour.red()
                    await ctx.respond(embed=embed)

    @animalgroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="sandcar", description="Sends a sand car. :3 :3 :3 :3")
    async def sandcarrmeoww(self, ctx):
        cat_titles = ["meowww :3", "mreowwww :33", "mrrrp :3", "meow :3", "nyaa~ :3", "nyaa~", ":3", "rawr :3"]
        endpoint = "https://beta.sandcat.pics/sand/random"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    carlink = data["name"]
                    embed = discord.Embed(title=random.choice(cat_titles), image=carlink)
                    embed.set_footer(text=f"Requested by {ctx.author.name}")
                    await ctx.respond(embed=embed)
                else:
                    embed = discord.Embed(title = "Error", description = "Failed to fetch data from the API.")
                    embed.add_field(name = "Status Code", value = response.status)
                    embed.color = discord.Colour.red()
                    await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(animalz(bot))
