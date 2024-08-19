import discord
from discord.ext import commands
import requests

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="song", description="Fetches information about a specific song.", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def song(self, ctx, artist_name: discord.Option(str, "The artist's name"), song_name: discord.Option(str, "The song name")):
        # API endpoint for song information
        song_url = "https://api.whatdidyouexpect.eu/song"

        # Make a request to the API
        response = requests.get(song_url, params={"artist_name": artist_name, "song_name": song_name})

        # Check if the request was successful
        if response.status_code != 200:
            await ctx.respond("Error fetching data from the API.")
            return
        
        data = response.json()

        # Check for required fields in the API response
        if not all(key in data for key in ("album_name", "album_url", "artist_name", "preview_audio_base64", "track_name")):
            await ctx.respond("Incomplete data received from the API.")
            return

        # Extract information from the API response
        album_name = data.get("album_name")
        album_url = data.get("album_url")
        artist_name = data.get("artist_name")
        track_name = data.get("track_name")
        preview_audio_base64 = data.get("preview_audio_base64")
        track_url = data.get("track_url", "No URL")

        # Create the embed message
        embed = discord.Embed(title="Song Information", colour=0x00b0f4)
        embed.add_field(name="Track Name", value=track_name, inline=False)
        embed.add_field(name="Album Name", value=album_name, inline=False)
        embed.add_field(name="Artist", value=artist_name, inline=False)
        embed.add_field(name="Album URL", value=album_url, inline=False)
        if track_url != "No URL":
            embed.add_field(name="Preview URL", value=track_url, inline=False)

        # Set the thumbnail if preview_audio_base64 is valid or use a placeholder
        # Example placeholder, replace with a valid URL if available
        placeholder_thumbnail_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRYAhsy868LxycSZsR7pRTd_bL9IObry3WZA&s"
        embed.set_thumbnail(url=placeholder_thumbnail_url)

        # Send the response
        try:
            await ctx.respond(embed=embed)
        except discord.HTTPException as e:
            await ctx.respond(f"An error occurred: {e}")

# Setup function to add the cog to the bot
def setup(bot):
    bot.add_cog(MusicCommands(bot))
