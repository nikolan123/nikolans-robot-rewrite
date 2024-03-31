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
        embed = discord.Embed(title="Pong!", description=f"{round(self.bot.latency*1000)}ms")
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.respond(embed=embed)

    @commands.slash_command(name="debug_info", description="Shows info about the bot")
    @commands.cooldown(1, 15, BucketType.user)
    async def info(self, ctx):
        await ctx.respond("Busy")
        pycpuinf = cpuinfo.get_cpu_info()
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        embed = discord.Embed()
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
        embed = discord.Embed(title="Credits", description=f"I'm alive thanks to those peoples ⬇️")
        embed.add_field(inline=False, name="nikolan", value="Bot owner and main developer")
        embed.add_field(inline=False, name="tom1212.", value="Contributor, helped with a lot of stuff")
        embed.add_field(inline=False, name="giga", value="Former contributor, helped clean the code up")
        embed.add_field(inline=False, name="nexus", value="Helping find bugs and vulnerabilities in the bot")
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


def setup(bot):
    bot.add_cog(pingcmd(bot))
