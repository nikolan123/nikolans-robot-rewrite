import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from discord.ui import Button
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

class AboutCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    aboutgroup = discord.SlashCommandGroup(name="about", integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install})

    @aboutgroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="host", description="Shows info about the bot's host.")
    @commands.cooldown(1, 15, BucketType.user)
    async def host_info(self, ctx):
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
                powershell_command = r'''
                if (!(Test-Path "$env:TEMP\neofetch.exe")) { 
                    Invoke-WebRequest -Uri "https://github.com/nepnep39/neofetch-win/releases/download/v1.2.1/neofetch.exe" -OutFile "$env:TEMP\neofetch.exe" 
                } 
                & "$env:TEMP\neofetch.exe"
                '''    
                try:
                    output = subprocess.check_output(['powershell.exe', '-Command', powershell_command], text=True)
                except Exception:
                    output = None
                if output:
                    output = output.replace('``', '`​`​') # zwsp backticks
                    return await interaction.respond(f"```{output}```")
                else:
                    return await interaction.respond("An error occurred :(")
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
        thev = discord.ui.View(timeout=None)
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
    async def bot_credits(self, ctx):
        # first page
        embed1 = discord.Embed(title="Credits", colour=0x00b0f4)
        embed1.add_field(inline=False, name="People", value="[**nikolan**](https://nikolan.net) - Main bot developer\n[**restartb**](https://github.com/restartb) - Helped improve and organise code, made config system, improved docs\n[**tom1212.**](https://github.com/thepotatolover) - Helped take screenshots for the help command and more\n[**mat**](https://github.com/mat-1) - Sand cat images")
        embed1.add_field(inline=False, name="Links", value=f"[Github Repo (star pls :3)](https://github.com/nikolan123/nikolans-robot-rewrite)\n[Top.gg (upvote pls)](https://top.gg/bot/{self.bot.user.id})")
        # second page
        embed2 = discord.Embed(title='Computers', description="Lenovo ThinkPad X13 Gen 3 AMD\nLenovo ThinkPad L14 Gen 4 Intel\nAcer Aspire 5 (A514-54-532U)\nHuawei MateBook D14\nFujitsu Stylistic Q702\nCustom built (i3-12100/RX7600)\nCustom built (R5-3600/6500XT)\nCustom built (R9-5900X/7800XT)", color=0x54db8d)
        
        async def first_page(interaction):
            nonlocal view
            nonlocal embed1
            nonlocal camputers_button
            nonlocal first_page_button
            camputers_button.disabled = False
            first_page_button.disabled = True
            await interaction.response.defer()
            msg = await interaction.original_response()
            embed = embed1
            embed.set_footer(text=f"Requested by {interaction.user.name}")
            await msg.edit(embed=embed, view=view)

        async def second_page(interaction):
            nonlocal view
            nonlocal embed2
            nonlocal camputers_button
            nonlocal first_page_button
            camputers_button.disabled = True
            first_page_button.disabled = False
            await interaction.response.defer()
            msg = await interaction.original_response()
            embed = embed2
            embed.set_footer(text=f"Requested by {interaction.user.name}")
            await msg.edit(embed=embed, view=view)

        view = discord.ui.View(timeout=None)
        first_page_button = Button(label='People', style=discord.ButtonStyle.blurple)
        first_page_button.callback = first_page
        view.add_item(first_page_button)
        camputers_button = Button(label="Computers", style=discord.ButtonStyle.blurple)
        camputers_button.callback = second_page
        view.add_item(camputers_button)
        first_page_button.disabled = True
        camputers_button.disabled = False

        embed = embed1
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.respond(embed=embed, view=view)

    @aboutgroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="bot", description="Shows info about the bot.")
    async def bot_info(self, ctx):
        async def credits_callback(interaction):
            nonlocal ctx
            await interaction.response.defer()
            ctx2 = ctx
            ctx2.author = interaction.user
            await self.bot_credits(ctx2)

        async def contributing_callback(interaction):
            await interaction.response.defer()
            view = discord.ui.View(timeout=None)
            gitbuton = discord.ui.Button(label='GitHub Repo', style=discord.ButtonStyle.url, url="https://github.com/nikolan123/nikolans-robot-rewrite")
            view.add_item(gitbuton)
            embed = discord.Embed(color=discord.Color.dark_teal(), title="Contributing", description="Anyone is able to contribute to the bot, as it is fully open-source.")
            embed.add_field(name="How to Start",value="1. Fork the repository on GitHub.\n""2. Clone your fork to your local machine.\n""3. Create a new branch for your feature or bug fix.",inline=False)
            embed.add_field(name="Reporting Issues",value=f"If you find a bug or have a suggestion, please open an issue on our GitHub repository. For security issues, do not file a public issue, instead send {self.bot.ownername} a direct message.",inline=False)
            embed.add_field(name="Pull Requests", value="Please ensure your code is well-documented and includes tests where appropriate. Submit a pull request when ready.", inline=False)
            embed.set_footer(text="Thank you for your contributions!")
            await interaction.respond(embed=embed, view=view)
            
        embed = discord.Embed(title="nikolan's robot", description="A multifunctional Discord bot.\nLicensed under AGPLv3\n[⭐ Star the GitHub repository!](https://github.com/nikolan123/nikolans-robot-rewrite)", thumbnail=str(self.bot.user.avatar.url), color=discord.Color.dark_gold())
        embed.set_footer(text="mreeow :3")
        view = discord.ui.View(timeout=None)
        button_credits = Button(label="Credits", style=discord.ButtonStyle.blurple)
        button_credits.callback = credits_callback
        view.add_item(button_credits)
        button_contributing = Button(label="Contributing", style=discord.ButtonStyle.blurple)
        button_contributing.callback = contributing_callback
        view.add_item(button_contributing)
        await ctx.respond(embed=embed, view=view)

def setup(bot):
    bot.add_cog(AboutCommands(bot))
