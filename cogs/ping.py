import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from discord.ui import Button, View
import socket
import os
import platform
import cpuinfo
import subprocess
import re
import asyncio

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
        async def embedy():
            embed = discord.Embed(title="Credits", colour=0x00b0f4)
            embed.add_field(inline=False, name="People", value="[**nikolan**](https://nikolan.net) - Main bot developer\n[**restartb**](https://github.com/restartb) - Helped improve and organise code, made config system, improved docs\n[**tom1212.**](https://github.com/thepotatolover) - Helped take screenshots for the help command and more\n[**mat**](https://github.com/mat-1) - Sand cat images\n[**expect**](https://whatdidyouexpect.eu) - Added a few commands")
            embed.add_field(inline=False, name="Links", value=f"[Github Repo (star pls :3)](https://github.com/nikolan123/nikolans-robot-rewrite)\n[Top.gg (upvote pls)](https://top.gg/bot/{self.bot.user.id})")
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            return embed
        async def first_page(interaction):
            await interaction.response.defer()
            msg = await interaction.original_response()
            view = discord.ui.View()
            first_page_button = Button(label='People', style=discord.ButtonStyle.blurple)
            first_page_button.disabled = True
            view.add_item(first_page_button)
            camputers_button = Button(label="Computers", style=discord.ButtonStyle.blurple)
            camputers_button.callback = camputers_page
            view.add_item(camputers_button)
            await msg.edit(embed=await embedy(), view=view)

        async def camputers_page(interaction):
            await interaction.response.defer()
            msg = await interaction.original_response()
            embed = discord.Embed(title='Computers', description="Lenovo ThinkPad X13 Gen 3 AMD\nLenovo ThinkPad L14 Gen 4 Intel\nAcer Aspire 5 (A514-54-532U)\nHuawei MateBook D14\nFujitsu Stylistic Q702\nCustom built (i3-12100/RX7600)\nCustom built (R5-3600/6500XT)\nCustom built (R9-5900X/7800XT)\nLenovo ThinkPad W530 dGPU\nGigabyte G5 KC", color=0x54db8d)
            embed.set_footer(text=f"Requested by {interaction.user.name}")
            view = discord.ui.View()
            people_button = Button(label="People", style=discord.ButtonStyle.blurple)
            people_button.callback = first_page
            camputers_button_disabled = Button(label="Computers", style=discord.ButtonStyle.blurple)
            camputers_button_disabled.disabled = True
            view.add_item(people_button)
            view.add_item(camputers_button_disabled)
            await msg.edit(embed=embed, view=view)

        view = discord.ui.View()
        first_page_button = Button(label='People', style=discord.ButtonStyle.blurple)
        first_page_button.disabled = True
        view.add_item(first_page_button)
        camputers_button = Button(label="Computers", style=discord.ButtonStyle.blurple)
        camputers_button.callback = camputers_page
        view.add_item(camputers_button)
        await ctx.respond(embed=await embedy(), view=view)

def setup(bot):
    bot.add_cog(pingcmd(bot))
