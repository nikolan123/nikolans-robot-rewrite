import discord
from discord.ext import commands
import requests

class MinecraftCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="mcversions", description="Fetches the 'latest' Minecraft version and its download link.", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def minecraft_version(self, ctx, version: discord.Option(str, "The Minecraft version to search for", required=False)):
        version_manifest_url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

        response = requests.get(version_manifest_url)
        if response.status_code != 200:
            await ctx.respond("Error fetching data from the Mojang API.")
            return

        data = response.json()

        if version:

            version_info = next((v for v in data["versions"] if v["id"] == version), None)
            if not version_info:
                await ctx.respond(f"Version '{version}' not found.")
                return
        else:
 
            latest_release = data.get("latest", {}).get("release")
            version_info = next((v for v in data["versions"] if v["id"] == latest_release), None)

        if not version_info:
            await ctx.respond("Could not find the version information.")
            return

        version_id = version_info["id"]
        release_date = version_info.get("releaseTime", "No release date available")
        version_url = version_info.get("url")

        version_details_response = requests.get(version_url)
        if version_details_response.status_code != 200:
            await ctx.respond("Error fetching version details.")
            return

        version_details = version_details_response.json()
        download_url = version_details.get("downloads", {}).get("server", {}).get("url", "No download link available")


        embed = discord.Embed(title=f"Minecraft Version: {version_id}", colour=0x00b0f4)
        embed.add_field(name="Version", value=version_id, inline=False)
        embed.add_field(name="Release Date", value=release_date, inline=False)
        embed.add_field(name="Download Link", value=download_url, inline=False)


        try:
            await ctx.respond(embed=embed)
        except discord.HTTPException as e:
            await ctx.respond(f"An error occurred: {e}")

# made by your dearest gabe/expect :3
def setup(bot):
    bot.add_cog(MinecraftCommands(bot))