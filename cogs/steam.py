import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import aiohttp
import random
import json
import chunk

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
                embed = discord.Embed(title=f"{thegame['name']}", url=f"https://store.steampowered.com/app/{thegame['appid']}/", image=f"https://cdn.akamai.steamstatic.com/steam/apps/{thegame['appid']}/header.jpg", colour=0x00b0f4)
                embed.set_footer(text=f"Requested by {ctx.author.name} | App ID {thegame['appid']}")
                
                async def callback(interaction: discord.Interaction):
                    try:
                        thegame = random.choice(thegames)
                        new_embed = discord.Embed(title=f"{thegame['name']}", url=f"https://store.steampowered.com/app/{thegame['appid']}/", image=f"https://cdn.akamai.steamstatic.com/steam/apps/{thegame['appid']}/header.jpg", colour=0x00b0f4)
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

    @commands.slash_command(name="steamsearch", description="Searches for games on Steam")
    async def stsrg(self, ctx, thesearch: discord.Option(str, name='query', description='The game you want to look for')): # type: ignore
        try:
            with open('steam.json', 'r') as steamfile:
                thejsons = json.load(steamfile)
                thegames = thejsons["applist"]["apps"]
                
                # filter and sort games
                matched_games = [game for game in thegames if thesearch.lower() in game['name'].lower()]
                matched_games.sort(key=lambda x: x['name'].lower().index(thesearch.lower()))
                
                if not matched_games:
                    await ctx.respond("No games found.")
                    return
                
                # pagination
                chunk_size = 7
                chunks = [matched_games[i:i + chunk_size] for i in range(0, len(matched_games), chunk_size)]
                current_page = 0

                async def send_page(page_number):
                    games_on_page = chunks[page_number]
                    description = ""
                    for i, game in enumerate(games_on_page):
                        number = i + 1 + (page_number * chunk_size)
                        description += f"{number}. [{game['name']}](https://store.steampowered.com/app/{game['appid']}/)\n"
                    embed = discord.Embed(title=f"Search results for '{thesearch}':",
                                          description=description,
                                          color=discord.Color.blue())
                    embed.set_footer(text=f"Page {page_number + 1}/{len(chunks)}")
                    return embed

                embed = await send_page(current_page)
                message = await ctx.respond(embed=embed)

                # buttonsy add
                view = MyView(current_page, len(chunks), thesearch, chunks)
                await message.edit(view=view)

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
                embed = discord.Embed(title=f"{thegame['name']}", url=f"https://store.steampowered.com/app/{thegame['appid']}/", image=f"https://cdn.akamai.steamstatic.com/steam/apps/{thegame['appid']}/header.jpg", colour=0x00b0f4)
                embed.set_footer(text=f"Requested by {ctx.author.name} | App ID {thegame['appid']}")
                await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f"An error has occured: ```{e}```Please DM @{self.bot.ownername} or join [the Discord server]({self.bot.supportserver})")

class MyView(discord.ui.View):
    def __init__(self, current_page, total_pages, thesearch, chunks):
        super().__init__()
        self.current_page = current_page
        self.total_pages = total_pages
        self.thesearch = thesearch
        self.chunks = chunks

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.secondary)
    async def prev_button_callback(self, button, interaction):
        self.current_page -= 1
        if self.current_page < 0:
            self.current_page = self.total_pages - 1
        embed = await self.send_page(self.current_page)
        await interaction.response.edit_message(embed=embed, view=self)
    @discord.ui.button(label="➡️", style=discord.ButtonStyle.secondary)
    async def next_button_callback(self, button, interaction):
        self.current_page += 1
        if self.current_page >= self.total_pages:
            self.current_page = 0
        embed = await self.send_page(self.current_page)
        await interaction.response.edit_message(embed=embed, view=self)

    async def send_page(self, page_number):
        games_on_page = self.chunks[page_number]
        description = ""
        for i, game in enumerate(games_on_page):
            number = i + 1 + (page_number * len(self.chunks[0]))
            description += f"{number}. [{game['name']}](https://store.steampowered.com/app/{game['appid']}/)\n"
        embed = discord.Embed(title=f"Search results for '{self.thesearch}':",
                              description=description,
                              color=discord.Color.blue())
        embed.set_footer(text=f"Page {page_number + 1}/{self.total_pages}")
        return embed

def setup(bot):
    bot.add_cog(steams(bot))
