import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import aiohttp
import base64
import io

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="song", description="Fetches information about a specific song.", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    @commands.cooldown(1, 3, BucketType.user)
    async def song(self, ctx, artist_name: discord.Option(str, "The artist's name"), song_name: discord.Option(str, "The song name")): # type: ignore

        song_url = "https://api.whatdidyouexpect.eu/song"

        async with aiohttp.ClientSession() as session:
            async with session.get(song_url, params={"artist_name": artist_name, "song_name": song_name}) as response:
                data = await response.json()
                if data.get('error'):
                    return await ctx.respond(embed=discord.Embed(color=discord.Color.red(), title="Error", description=data['error']))
                response.raise_for_status()
           
        if not all(key in data for key in ("album_name", "album_url", "artist_name", "preview_audio_base64", "track_name", "album_image_url")):
            await ctx.respond("Incomplete data received from the API.")
            return

        album_name = data.get("album_name")
        album_url = data.get("album_url")
        artist_name = data.get("artist_name")
        track_name = data.get("track_name")
        bpreview_audio_base64 = base64.b64decode(data.get("preview_audio_base64"))
        track_url = data.get("track_url")
        album_image_url = data.get("album_image_url")

        mp3t = io.BytesIO(bpreview_audio_base64)
    
        embed = discord.Embed(title=track_name, colour=0x00b0f4)
        embed.add_field(name="Album", value=album_name, inline=False)
        embed.add_field(name="Artist", value=artist_name, inline=False)

        if album_image_url:
            embed.set_thumbnail(url=album_image_url)

        view = discord.ui.View(timeout=None)
        view.add_item(discord.ui.Button(label="Album link", url=album_url, style=discord.ButtonStyle.url))
        if track_url is None:
            view.add_item(discord.ui.Button(label="Preview", url=track_url, style=discord.ButtonStyle.url))

        try:
            await ctx.respond(embed=embed, view=view, file=discord.File(fp=mp3t, filename="preview.mp3"))
        except discord.HTTPException as e:
            await ctx.respond(f"An error occurred: {e}")

def setup(bot):
    bot.add_cog(MusicCommands(bot))