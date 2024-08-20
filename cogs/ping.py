import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from discord.ui import Button, View
import socket
import os
import platform
import sympy as sp
import cpuinfo
import subprocess
import re
import asyncio
import random

def remove_escape_sequences(text):
    pattern = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')
    cleaned_lines = []
    for line in text.split('\n'):
        cleaned_line = pattern.sub('', line).rstrip('\t ').rstrip()
        cleaned_lines.append(cleaned_line)
    return '\n'.join(cleaned_lines)

class pingcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    aboutgroup = discord.SlashCommandGroup(name="about", integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install})

    @aboutgroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="ping", description="Shows the bot latency.")
    async def ping(self, ctx):
        embed = discord.Embed(title="Pong!", description=f"{round(self.bot.latency*1000)}ms", colour=0x00b0f4)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.respond(embed=embed)

    @aboutgroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="host", description="Shows info about the bot.")
    @commands.cooldown(1, 15, BucketType.user)
    async def info(self, ctx):
        await ctx.respond("Fetching...")
        pycpuinf = cpuinfo.get_cpu_info()
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        embed = discord.Embed(colour=0x00b0f4)
        embed.add_field(inline=False, name="Debug Information", value=f"**Latency** - `{round(self.bot.latency*1000)}ms`\n**Local IP** - `{local_ip}`\n**Hostname** - `{hostname}`\n**System** - `{platform.system()} {platform.release()} - ({os.name})`\n**Python version** - `{pycpuinf['python_version']}`")
        embed.add_field(inline=False, name="Hardware", value=f"**CPU** - `{pycpuinf['brand_raw']}`")
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        async def neofetch(interaction):
            #find / -name neofetch 2> /dev/null
            if os.name == 'nt':
                return await interaction.respond("Running under Windows host :(")
            p = remove_escape_sequences(subprocess.check_output(['neofetch', '--off']).decode("utf-8"))
            embed = discord.Embed(title='neofetch', description=f"```{p}```")
            await interaction.respond(embed=embed)
        async def pinglc(interaction):
            #find / -name ping 2> /dev/null
            await interaction.respond('Pinging `localhost`...')
            if os.name == 'nt':
                pingcmd = 'ping localhost'
            else:
                pingcmd = 'ping localhost -c 4'
            proc = await asyncio.create_subprocess_shell(
                pingcmd,
                stderr=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            if stdout:
                embed = discord.Embed(title='ping localhost', description=f"```{stdout.decode('utf-8')}```")
                await interaction.respond(embed=embed)
            else:
                await interaction.respond("An error occured.")

        async def pinglcn(interaction):
            #find / -name ping 2> /dev/null
            await interaction.respond('Pinging `api.nikolan.xyz`...')
            if os.name == 'nt':
                pingcmd = 'ping api.nikolan.xyz'
            else:
                pingcmd = 'ping api.nikolan.xyz -c 4'
            proc = await asyncio.create_subprocess_shell(
                pingcmd,
                stderr=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            if stdout:
                embed = discord.Embed(title='ping api.nikolan.xyz', description=f"```{stdout.decode('utf-8')}```")
                await interaction.respond(embed=embed)
            else:
                await interaction.respond("An error occured.")
        thev = discord.ui.View()
        butb = Button(label="Neofetch", style=discord.ButtonStyle.blurple)
        butb.callback = neofetch
        thev.add_item(butb)
        butbb = Button(label="Ping localhost", style=discord.ButtonStyle.blurple)
        butbb.callback = pinglc
        thev.add_item(butbb)
        butbbb = Button(label="Ping api.nikolan.xyz", style=discord.ButtonStyle.blurple)
        butbbb.callback = pinglcn
        thev.add_item(butbbb)
        await ctx.edit(embed=embed, content="", view=thev)

    @aboutgroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="credits", description="Shows the credits.")
    async def credyts(self, ctx):
        embed = discord.Embed(title="Credits", description=f"I'm alive thanks to those people ⬇️", colour=0x00b0f4)
        embed.add_field(inline=False, name="", value="[**nikolan**](https://nikolan.net) - Main bot developer\n[**tom1212.**](https://github.com/thepotatolover) - Helped take screenshots for the help command\n[**restartb**](https://github.com/restartb) - Helped improve and organise code, made config system, improved docs\n[**mat**](https://github.com/mat-1) - Sand cat images\n[**expect**](https://whatdidyouexpect.xyz) - Added a few commands")
        embed.add_field(inline=False, name="Computers", value="""
Lenovo ThinkPad X13 Gen 3 AMD
Lenovo ThinkPad L14 Gen 4 Intel
Acer Aspire 5 (A514-54-532U)
Huawei MateBook D14
Fujitsu Stylistic Q702
Custom built (i3-12100/RX7600)
Custom built (R5-3600/6500XT)
Custom built (R9-5900X/7800XT)
Lenovo ThinkPad W530 dGPU
Gigabyte G5 KC
""")
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        view = discord.ui.View()
        gitbuton = discord.ui.Button(label='GitHub Repo (star pls)', style=discord.ButtonStyle.url, url="https://github.com/nikolan123/nikolans-robot-rewrite")
        topbuton = discord.ui.Button(label='Top.gg (upvote pls)', style=discord.ButtonStyle.url, url=f"https://top.gg/bot/{self.bot.user.id}")
        view.add_item(gitbuton)
        view.add_item(topbuton)
        await ctx.respond(embed=embed, view=view)

    @commands.slash_command(name="pipeyhit", description="Hits someone with metal pipey.")
    async def pipeyhit(self, ctx, victim: discord.Option(discord.User, "The user you want to hit"), pingusr: discord.Option(bool, name="ping", description="Ping the victim") = False): # type: ignore
        embed = discord.Embed(
            title="Metal Pipey Hit",
            description=f":wrench: <@{victim.id}> got hit with metal pipey!!",
            color=0xFF0000,
        )
        embed.set_thumbnail(
            url="https://static.wikia.nocookie.net/object-trek/images/0/0c/Pipey.png/revision/latest/scale-to-width/360?cb=20170904212026"
        )
        
        embedDone = discord.Embed(title = "Done!")
        embedDone.color = discord.Colour.green()
        await ctx.respond(embed=embedDone, ephemeral=True)
        
        if pingusr:
            await ctx.send(embed=embed, content=victim.mention)
        else:
            await ctx.send(embed=embed)

    @commands.slash_command(name="members", description="Shows the server's member count.")
    async def members(self, ctx):
        bot_count = sum(1 for member in ctx.guild.members if member.bot)
        member_count = sum(1 for member in ctx.guild.members if not member.bot)
        embed = discord.Embed(title="Server Members",
                        description=f"**Bots:** {bot_count}\n**Members:** {member_count}",
                        colour=0x00b0f4)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.respond(embed=embed)

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="avatar", description="Gets a user's avatar")
    async def avatary(self, ctx, usery: discord.Option(discord.Member, name="user", description="The user to get the avatar of")): # type: ignore
        embed = discord.Embed(title=f"{usery.name}'s Avatar", url=usery.avatar.url, image=usery.avatar.url, colour=0x00b0f4)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.respond(embed=embed)

    @commands.slash_command(name="sleep", description="Tells others you're going to sleep.")
    async def sleep(self, ctx):
        embed = discord.Embed(
            title=f"{ctx.author.name} is going to sleep",
            description="Everyone wish them good night!",
            colour=0x55C5FF,
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1247/1247769.png")
        await ctx.respond(embed=embed)

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="calc", description="Maths")
    async def calcuyy(self, ctx, thingy: discord.Option(str, "...", name="expression")): # type: ignore
        try:
            if not all(char.isdigit() or char in "+-*/.()" for char in thingy):
                raise ValueError("Invalid input! Please provide a valid mathematical expression.")

            expr = sp.sympify(thingy)
            
            if isinstance(expr, int):
                fresulty = str(expr)
            else:
                fresulty = str(expr).rstrip('0').rstrip('.')

            embed = discord.Embed(colour=0x00b0f4, title="Math Solver", description=f"{thingy} = **{fresulty}**")
            await ctx.respond(embed=embed)
        except ValueError as e:
            embed = discord.Embed(colour=0xff0000, title='Error! Invalid input', description=str(e))
            await ctx.respond(embed=embed)
        except sp.SympifyError as e:
            embed = discord.Embed(colour=0xff0000, title='Error! Invalid input', description=str(e))
            await ctx.respond(embed=embed)
        except Exception as e:
            embed = discord.Embed(colour=0xff0000, title="Unexpected error!", description=str(e))
            await ctx.respond(embed=embed)

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name='random-color', description='Generates a random color')
    async def random_color(self, ctx):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        color_hex = "#{:02x}{:02x}{:02x}".format(red, green, blue)
        embed = discord.Embed(title="Random Color", description=color_hex, color=discord.Color(int(color_hex[1:], 16)))
        await ctx.respond(embed=embed)    

def setup(bot):
    bot.add_cog(pingcmd(bot))
