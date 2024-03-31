import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import aiohttp
import random
import json

class steams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # @commands.slash_command(name="randomgame", description="Sends a random Steam game")
    # @commands.cooldown(1, 3, BucketType.user)
    # async def randst(self, ctx):
    #     endpoint = "http://api.steampowered.com/ISteamApps/GetAppList/v0002"
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(endpoint) as response:
    #             if response.status == 200:
    #                 try:
    #                     data = await response.json()
    #                     doglink = data['applist']['apps']
    #                     game = random.choice(doglink)
    #                     embed = discord.Embed(title=f"{game['name']}", url=f"https://store.steampowered.com/app/{game['appid']}/", image=f"https://cdn.akamai.steamstatic.com/steam/apps/{game['appid']}/header.jpg")
    #                     embed.set_footer(text=f"Requested by {ctx.author.name} | App ID {game['appid']}")
    #                     await ctx.respond(embed=embed)
    #                 except Exception as e:
    #                     await ctx.respond(e)
    #             else:
    #                 await ctx.respond(f"Failed to fetch data from the API. Status code: {response.status}")

    @commands.slash_command(name="randomgame", description="Sends a random Steam game")
    async def randst(self, ctx):
        try:
            with open('steam.json', 'r') as steamfile:
                thejsons = json.load(steamfile)
                thegames = thejsons["applist"]["apps"]
                thegame = random.choice(thegames)
                embed = discord.Embed(title=f"{thegame['name']}", url=f"https://store.steampowered.com/app/{thegame['appid']}/", image=f"https://cdn.akamai.steamstatic.com/steam/apps/{thegame['appid']}/header.jpg")
                embed.set_footer(text=f"Requested by {ctx.author.name} | App ID {thegame['appid']}")
                await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f"An error has occured: ```{e}```Please DM @{self.bot.ownername} or join [the Discord server]({self.bot.supportserver})")


    @commands.slash_command(name="steamgame", description="Searches for a game on Steam")
    async def stsr(self, ctx, thesearch: discord.Option(str, name='name', description='The game you want to look for')): # type: ignore
        try:
            with open('steam.json', 'r') as steamfile:
                thejsons = json.load(steamfile)
                thegames = thejsons["applist"]["apps"]
                thegame = "uknoy :()"
                for game in thegames:
                    if game['name'].lower() == thesearch.lower():
                        thegame = game
                if thegame == 'uknoy :()':
                    await ctx.respond('Game not found. Please enter exact name')
                    return
                embed = discord.Embed(title=f"{thegame['name']}", url=f"https://store.steampowered.com/app/{thegame['appid']}/", image=f"https://cdn.akamai.steamstatic.com/steam/apps/{thegame['appid']}/header.jpg")
                embed.set_footer(text=f"Requested by {ctx.author.name} | App ID {thegame['appid']}")
                await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f"An error has occured: ```{e}```Please DM @{self.bot.ownername} or join [the Discord server]({self.bot.supportserver})")


def setup(bot):
    bot.add_cog(steams(bot))