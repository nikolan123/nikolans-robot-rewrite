import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import socket
import os
import platform
import cpuinfo

class pingcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name="ping", description="Shows the bot latency")
    async def ping(self, ctx):
        embed = discord.Embed(title="Pong!", description=f"{round(self.bot.latency*1000)}ms", colour=0x00b0f4)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.respond(embed=embed)

    @commands.slash_command(name="debug_info", description="Shows info about the bot")
    @commands.cooldown(1, 15, BucketType.user)
    async def info(self, ctx):
        await ctx.respond("Busy")
        pycpuinf = cpuinfo.get_cpu_info()
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        embed = discord.Embed(colour=0x00b0f4)
        embed.add_field(inline=False, name="Debug Information", value=f"**Latency** - `{round(self.bot.latency*1000)}ms`\n**Local IP** - `{local_ip}`\n**Hostname** - `{hostname}`\n**System** - `{platform.system()} {platform.release()} - ({os.name})`\n**Python version** - `{pycpuinf['python_version']}`")
        embed.add_field(inline=False, name="Hardware", value=f"**CPU** - `{pycpuinf['brand_raw']}`")
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.edit(embed=embed, content="")

    @commands.slash_command(name="top-gg", description="Sends a link to the bot's page in top.gg")
    async def topgg(self, ctx):
        embed = discord.Embed(color=0xff0000, url=f"https://top.gg/bot/{self.bot.user.id}", title="Top.gg", description="Please, upvote the bot in Top.gg!")
        await ctx.respond(embed=embed)

    @commands.slash_command(name="credits", description="Shows the credits")
    async def credyts(self, ctx):
        embed = discord.Embed(title="Credits", description=f"I'm alive thanks to those peoples ⬇️", colour=0x00b0f4)
        embed.add_field(inline=False, name="Current version", value="**nikolan** - Main bot developer")
        embed.add_field(inline=False, name="Old version", value="**nikolan** - Main bot developer\n**tom1212.** - Contributor, helped with a lot of stuff\n**giga** - Former contributor, helped clean the code up\n**nexus** - Helped find bugs and vulnerabilities in the bot")
        embed.add_field(inline=False, name="Camputers", value="""
Lenovo ThinkPad X13 Gen 3 AMD
Lenovo ThinkPad L14 Gen 4 Intel
Acer Aspire 5 (A514-54-532U)
Huawei MateBook D14
Custom built (i3-12100/RX7600)
Custom built (R5-3600/6500XT)
""")
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.respond(embed=embed)

    @commands.slash_command(name="pipeyhit", description="Hits someone with metal pipey")
    async def pipeyhit(self, ctx, victim: discord.Option(discord.User, "The user you want to hit"), pingusr: discord.Option(bool, name="ping", description="Ping the victim") = False): # type: ignore
        embed = discord.Embed(
            title="Metal Pipey Hit",
            description=f":wrench: <@{victim.id}> got hit with metal pipey!!",
            color=0xFF0000,
        )
        embed.set_thumbnail(
            url="https://static.wikia.nocookie.net/object-trek/images/0/0c/Pipey.png/revision/latest/scale-to-width/360?cb=20170904212026"
        )
        await ctx.respond("Done!", ephemeral=True)
        if pingusr:
            await ctx.send(embed=embed, content=victim.mention)
        else:
            await ctx.send(embed=embed)

    @commands.slash_command(name="members", description="Shows the server's member count")
    async def members(self, ctx):
        bot_count = sum(1 for member in ctx.guild.members if member.bot)
        member_count = sum(1 for member in ctx.guild.members if not member.bot)
        embed = discord.Embed(title="Server Members",
                        description=f"**Bots:** {bot_count}\n**Members:** {member_count}",
                        colour=0x00b0f4)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.respond(embed=embed)

    @commands.slash_command(name="avatar", description="Gets a user's avatar")
    async def avatary(self, ctx, usery: discord.Option(discord.Member, name="user", description="The user to get the avatar of")): # type: ignore
        embed = discord.Embed(title=f"{usery.name}'s Avatar", url=usery.avatar.url, image=usery.avatar.url, colour=0x00b0f4)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.respond(embed=embed)

    @commands.slash_command(name="sleep", description="Tells others you're going to sleep")
    async def sleep(self, ctx):
        embed = discord.Embed(
            title=f"{ctx.author.name} is going to sleep",
            description="Everyone wish them good night!",
            colour=0x55C5FF,
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1247/1247769.png")
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(pingcmd(bot))
