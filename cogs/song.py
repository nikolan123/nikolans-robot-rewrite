import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import aiohttp
import base64

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="song", description="Searches for a song on Spotify", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    @commands.cooldown(1, 3, BucketType.user)
    async def song(self, ctx, song_name: discord.Option(str, "The name of the song you want to look for")): # type: ignore
        #### get access token ####
        client_credentials = f"{self.bot.spotify_id}:{self.bot.spotify_secret}"
        encoded_credentials = base64.b64encode(client_credentials.encode()).decode()
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post("https://accounts.spotify.com/api/token", headers=headers, data=data) as response:
                response.raise_for_status()
                response_json = await response.json()
                accesstoken = response_json.get("access_token")
        ##########################
        async def gen_page(jsons, counter, total):
            embed = discord.Embed(color=discord.Color.blue(), title=jsons['name'], description=f"{'Explicit\n' if jsons['explicit'] is True else ''}")
            thumbnailurl = jsons.get('album', {}).get('images', [{}])[0].get('url', None)
            embed.set_thumbnail(url=thumbnailurl)
            artistfield = ''
            for artist in jsons['artists']:
                artistfield += f"[{artist['name']}]({artist['external_urls']['spotify']})\n"
            embed.add_field(name="Artists", value=artistfield)
            embed.set_footer(text=f"{counter+1}/{total}")
            return embed
        async def gen_view(jsons):
            view = discord.ui.View(timeout=None)
            view.add_item(discord.ui.Button(label="Spotify", url=jsons['external_urls']['spotify'], style=discord.ButtonStyle.url))
            if jsons['preview_url']:
                view.add_item(discord.ui.Button(label="Preview", url=jsons['preview_url'], style=discord.ButtonStyle.url))
            return view
        async def nextcb(interaction):
            nonlocal total
            nonlocal ctx
            nonlocal counter
            nonlocal allsongs
            await interaction.response.defer()
            counter += 1
            if counter == total:
                counter = 0
            embed = await gen_page(allsongs[counter], counter, total)
            view = await gen_view(allsongs[counter])
            await ctx.edit(embed=embed, view=view)
        async def backcb(interaction):
            nonlocal total
            nonlocal ctx
            nonlocal counter
            nonlocal allsongs
            await interaction.response.defer()
            counter -= 1
            if counter == -1:
                counter = total-1
            embed = await gen_page(allsongs[counter], counter, total)
            view = await gen_view(allsongs[counter])
            await ctx.edit(embed=embed, view=view)
        endpoint = "https://api.spotify.com/v1/search"
        headers = {
            "Authorization": f"Bearer {accesstoken}"
        }
        params = {
            "q": song_name,
            "type": "track",
            "limit": 25
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers, params=params) as response:
                response.raise_for_status()
                responsejson = await response.json()
                #print(responsejson)
        allsongs = responsejson['tracks']['items']

        total = responsejson['tracks']['limit']
        counter = 0

        control_view = discord.ui.View(timeout=None)

        backbutton = discord.ui.Button(label="Back", style=discord.ButtonStyle.blurple)
        nextbutton = discord.ui.Button(label="Next", style=discord.ButtonStyle.blurple)
        backbutton.callback = backcb
        nextbutton.callback = nextcb
        control_view.add_item(backbutton)
        control_view.add_item(nextbutton)

        await ctx.respond(embed=await gen_page(responsejson['tracks']['items'][0], counter, total), view=await gen_view(responsejson['tracks']['items'][0]))
        await ctx.respond(view=control_view, ephemeral=True)

def setup(bot):
    bot.add_cog(MusicCommands(bot))