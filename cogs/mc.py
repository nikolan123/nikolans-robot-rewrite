import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import aiohttp
import urllib.parse

class MinecraftCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    mcgroup = discord.SlashCommandGroup(name="minecraft", integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install})

    # made by your dearest gabe/expect :3
    @mcgroup.command(name="version", description="Fetches the 'latest' Minecraft version and its download link.", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    @commands.cooldown(1, 5, BucketType.user)
    async def minecraft_version(self, ctx, version: discord.Option(str, "The Minecraft version to search for", required=False)): # type: ignore
        version_manifest_url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

        async with aiohttp.ClientSession() as session:
            async with session.get(version_manifest_url) as response:
                response.raise_for_status()
                data = await response.json()

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
        release_date = version_info.get("releaseTime")
        version_url = version_info.get("url")

        async with aiohttp.ClientSession() as session:
            async with session.get(version_url) as response:
                response.raise_for_status()
                version_details = await response.json()

        server_url = version_details.get("downloads", {}).get("server", {}).get("url")
        client_url = version_details.get("downloads", {}).get("client", {}).get("url")

        embed = discord.Embed(title=f"Minecraft {version_id}", colour=0x00b0f4, description=f'`{version_details['type']}`\nJava {version_details['javaVersion']['majorVersion']}\nReleased {release_date.split("T")[0]}' if release_date else "Release date unknown")

        view = discord.ui.View(timeout=None)
        if server_url:
            view.add_item(discord.ui.Button(label="server.jar", url=server_url, style=discord.ButtonStyle.url))
        if client_url:
            view.add_item(discord.ui.Button(label="client.jar", url=client_url, style=discord.ButtonStyle.url))

        try:
            await ctx.respond(embed=embed, view=view)
        except discord.HTTPException as e:
            await ctx.respond(f"An error occurred: {e}")

    @mcgroup.command(name="skin", description="Fetches a player's skin.", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    @commands.cooldown(1, 5, BucketType.user)
    async def minecraft_skinn(self, ctx, player: discord.Option(str, "...", required=True)): # type: ignore
        playername = urllib.parse.quote(player)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{playername}") as response:
                try:
                    thing = await response.json()
                    response.raise_for_status()
                except:
                    return await ctx.respond(embed=discord.Embed(color=discord.Color.red(), title="Error", description="Player not found."))
        embed = discord.Embed(title=f"{playername}'s skin", color=discord.Color.blue(), image=f"https://mineskin.eu/armor/body/{playername}/100.png", description=str(thing['id']))
        view = discord.ui.View(timeout=None)
        view.add_item(discord.ui.Button(label="Download", url=f"https://mineskin.eu/download/{playername}", style=discord.ButtonStyle.url))
        view.add_item(discord.ui.Button(label="Head", url=f"https://mineskin.eu/helm/{playername}", style=discord.ButtonStyle.url))
        view.add_item(discord.ui.Button(label="3D head", url=f"https://mineskin.eu/headhelm/{playername}/100.png", style=discord.ButtonStyle.url))
        await ctx.respond(embed=embed, view=view)

def setup(bot):
    bot.add_cog(MinecraftCommands(bot))