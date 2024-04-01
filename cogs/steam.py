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

    @commands.slash_command(name="randomgame", description="Sends a random Steam game")
    async def randst(self, ctx):
        try:
            with open('steam.json', 'r') as steamfile:
                thejsons = json.load(steamfile)
                thegames = thejsons["applist"]["apps"]
                thegame = random.choice(thegames)
                embed = discord.Embed(title=f"{thegame['name']}", url=f"https://store.steampowered.com/app/{thegame['appid']}/", image=f"https://cdn.akamai.steamstatic.com/steam/apps/{thegame['appid']}/header.jpg")
                embed.set_footer(text=f"Requested by {ctx.author.name} | App ID {thegame['appid']}")
                
                async def callback(interaction: discord.Interaction):
                    try:
                        thegame = random.choice(thegames)
                        new_embed = discord.Embed(title=f"{thegame['name']}", url=f"https://store.steampowered.com/app/{thegame['appid']}/", image=f"https://cdn.akamai.steamstatic.com/steam/apps/{thegame['appid']}/header.jpg")
                        new_embed.set_footer(text=f"Requested by {interaction.user.name} | App ID {thegame['appid']}")
                        
                        await interaction.response.edit_message(embed=new_embed)

                    except Exception as e:
                        await interaction.response.edit_message(content=f"An error has occurred: ```{e}```Please DM @{self.bot.owner.name} or join [the Discord server]({self.bot.supportserver})")

                view = discord.ui.View()
                button = discord.ui.Button(label="Get Another Random Game", style=discord.ButtonStyle.primary)
                button.callback = callback
                view.add_item(button)

                await ctx.respond(embed=embed, view=view)

        except Exception as e:
            await ctx.respond(f"An error has occurred: ```{e}```Please DM @{self.bot.owner.name} or join [the Discord server]({self.bot.supportserver})")

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
