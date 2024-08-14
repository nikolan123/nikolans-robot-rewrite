import discord
from discord.ext import commands
import random
import json
import re
import aiohttp
import html

class steams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    steamgroup = discord.SlashCommandGroup(name="steam", integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install})

    @steamgroup.command(integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install}, name="random", description="Sends a random Steam game.")
    async def randst(self, ctx):
        try:
            with open('data/steam.json', 'r', encoding='latin-1') as steamfile:
                thejsons = json.load(steamfile)
                thegames = thejsons["applist"]["apps"]
                thegame = random.choice(thegames)
                appid = thegame['appid']
                
                # Fetch game data
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=eur") as response:
                        appinfo1 = await response.json()
                        appinfo = appinfo1[str(appid)]['data']
                
                try:
                    if "nudity" in appinfo['content_descriptors']['notes'] or "sex" in appinfo['content_descriptors']['notes']:
                        return await ctx.respond("No NSFW, please.")
                except:
                    pass
                
                appdisc = f"**{appinfo['achievements']['total'] if 'achievements' in appinfo else 'No'} achievements\nReleased {appinfo['release_date']['date']}\n{'Free' if appinfo.get('is_free') else appinfo.get('price_overview', {}).get('final_formatted', 'unknown')}**"
                embed = discord.Embed(title=f"{appinfo['name']}", description=html.unescape(appinfo['short_description']), url=f"https://store.steampowered.com/app/{appid}/", image=f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg", colour=0x00b0f4)
                embed.add_field(name="", value=appdisc)
                
                # Add button to get another random game
                async def random_game_callback(interaction: discord.Interaction):
                    try:
                        thegame = random.choice(thegames)
                        appid = thegame['appid']
                        
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=eur") as response:
                                appinfo1 = await response.json()
                                appinfo = appinfo1[str(appid)]['data']
                        
                        try:
                            if "nudity" in appinfo['content_descriptors']['notes'] or "sex" in appinfo['content_descriptors']['notes']:
                                return await interaction.response.edit_message(content="No NSFW, please.")
                        except:
                            pass

                        appdisc = f"**{appinfo['achievements']['total'] if 'achievements' in appinfo else 'No'} achievements\nReleased {appinfo['release_date']['date']}\n{'Free' if appinfo.get('is_free') else appinfo.get('price_overview', {}).get('final_formatted', 'unknown')}**"
                        new_embed = discord.Embed(title=f"{appinfo['name']}", description=html.unescape(appinfo['short_description']), url=f"https://store.steampowered.com/app/{appid}/", image=f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg", colour=0x00b0f4)
                        new_embed.add_field(name="", value=appdisc)
                        new_embed.set_footer(text=f"Requested by {interaction.user.name} | App ID {appid}")
                        
                        await interaction.response.edit_message(embed=new_embed)
                    
                    except Exception as e:
                        error_embed = discord.Embed(title="Error", description=f"An error occurred while fetching Steam data. Please DM @{self.bot.ownername} or join [the Discord server]({self.bot.supportserver})")
                        error_embed.add_field(name="Error Info", value=e)
                        error_embed.color = discord.Colour.red()
                        await interaction.response.edit_message(embed=error_embed)
                
                view = discord.ui.View(timeout=None)
                button = discord.ui.Button(label="Get Another Random Game", style=discord.ButtonStyle.primary)
                button.callback = random_game_callback
                view.add_item(button)
                
                if appinfo.get('website'):
                    view.add_item(discord.ui.Button(label="Website", url=appinfo['website'], style=discord.ButtonStyle.url))
                
                embed.set_footer(text=f"Requested by {ctx.author.name} | App ID {appid}")
                await ctx.respond(embed=embed, view=view)
        
        except Exception as e:
            embed = discord.Embed(title="Error", description=f"An error occurred while fetching Steam data. Please DM @{self.bot.ownername} or join [the Discord server]({self.bot.supportserver})")
            embed.add_field(name="Error Info", value=e)
            embed.color = discord.Colour.red()
            await ctx.respond(embed=embed)

    @steamgroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="search", description="Searches for games on Steam.")
    async def stsrg(self, ctx, thesearch: discord.Option(str, name='query', description='The game you want to look for')): # type: ignore
        try:
            with open('data/steam.json', 'r', encoding='latin-1') as steamfile:
                thejsons = json.load(steamfile)
                thegames = thejsons["applist"]["apps"]
                
                # filter and sort games
                matched_games = [game for game in thegames if thesearch.lower() in game['name'].lower()]
                matched_games.sort(key=lambda x: x['name'].lower().index(thesearch.lower()))
                
                if not matched_games:
                    embed = discord.Embed(title = "Error", description = f"Couldn't find any results.")
                    embed.color = discord.Colour.red()
                    await ctx.respond(embed=embed)
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
            embed = discord.Embed(title = "Error", description = f"An error occurred while fetching Steam data. Please DM @{self.bot.ownername} or join [the Discord server]({self.bot.supportserver})")
            embed.add_field(name = "Error Info", value = e)
            embed.color = discord.Colour.red()
            await ctx.respond(embed=embed)
    
    @steamgroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="game", description="Searches for a game on Steam.")
    async def stsr(self, ctx, thesearch: discord.Option(str, name='name', description='The game you want to look for')): # type: ignore
        try:
            with open('data/steam.json', 'r', encoding='latin-1') as steamfile:
                thejsons = json.load(steamfile)
                thegames = thejsons["applist"]["apps"]
                thegame = "uknoy :()"
                for game in thegames:
                    if game['name'].lower() == thesearch.lower():
                        thegame = game
                if thegame == 'uknoy :()':
                    embed = discord.Embed(title = "Error", description = f"Couldn't find that game. Please enter the exact name.")
                    embed.color = discord.Colour.red()
                    await ctx.respond(embed=embed)
                    return
                # fetch data
                appid = thegame['appid']
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=eur") as response:
                        appinfo1 = await response.json()
                        appinfo = appinfo1[str(appid)]['data']
                try:
                    if "nudity" in appinfo['content_descriptors']['notes'] or "sex" in appinfo['content_descriptors']['notes']:
                        return await ctx.respond("No NSFW, please.")
                except:
                    pass
                appdisc = f"**{appinfo['achievements']['total'] if 'achievements' in appinfo else "No"} achievements\nReleased {appinfo['release_date']['date']}\n{'Free' if appinfo.get('is_free') else appinfo.get('price_overview', {}).get('final_formatted', 'unknown')}**"
                embed = discord.Embed(title=f"{appinfo['name']}", description=html.unescape(appinfo['short_description']), url=f"https://store.steampowered.com/app/{thegame['appid']}/", image=f"https://cdn.akamai.steamstatic.com/steam/apps/{thegame['appid']}/header.jpg", colour=0x00b0f4)
                embed.add_field(name="", value=appdisc)
                view = discord.ui.View(timeout=None)
                view.add_item(discord.ui.Button(label = "Steam Page", url = f"https://store.steampowered.com/app/{thegame['appid']}/", style = discord.ButtonStyle.url))
                if appinfo['website']:
                    view.add_item(discord.ui.Button(label = "Website", url = appinfo['website'], style = discord.ButtonStyle.url))
                embed.set_footer(text=f"Requested by {ctx.author.name} | App ID {appid}")
                await ctx.respond(embed=embed, view=view)
        except Exception as e:
            embed = discord.Embed(title = "Error", description = f"An error occurred while fetching Steam data. Please DM @{self.bot.ownername} or join [the Discord server]({self.bot.supportserver})")
            embed.add_field(name = "Error Info", value = e)
            embed.color = discord.Colour.red()
            await ctx.respond(embed=embed)

    @steamgroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="user", description="Searches for users on Steam.")
    async def steamlookup(self, ctx, user: discord.Option(str, name='id', description='The Steam ID you want to lookup')): # type: ignore
        pattern = r'^\d{17}$'
        if not re.match(pattern, user):
            return await ctx.respond("Please, input a valid Steam ID.")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.bot.steamkey}&steamids={user}") as response:
                if response.status == 200:
                    thing = await response.json()
                else:
                    return await ctx.respond(embed=discord.Embed(title="An error occured :("))
        if not thing['response']['players']:
            return await ctx.respond("User not found.")
        userinfo = thing['response']['players'][0]
        description = ""
        if 'loccountrycode' in userinfo:
            description += f":flag_{userinfo['loccountrycode'].lower()}: {userinfo['loccountrycode']}\n"
        if 'lastlogoff' in userinfo:
            description += f"Last seen <t:{userinfo['lastlogoff']}>\n"
        if 'timecreated' in userinfo:
            description += f"Account Created <t:{userinfo['timecreated']}>\n"
        embed = discord.Embed(
            title=userinfo['personaname'],
            description=description,
            url=userinfo['profileurl'],
        )
        embed.set_thumbnail(url=userinfo['avatarfull'])
        embed.set_footer(text=userinfo['steamid'])
        await ctx.respond(embed=embed)

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
