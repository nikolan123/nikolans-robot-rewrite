import discord
from discord.ext import commands
import aiohttp
import asyncio
from discord.ext.commands import BucketType
import random

class apicmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    async def fetch_data(self, ctx, endpoint):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, timeout=3) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        embed = discord.Embed(title = "Error", description = f"Failed to fetch data from the API. Please contact @{self.bot.ownername}.")
                        embed.add_field(name = "Status Code", value = response.status)
                        embed.color = discord.Colour.red()
                        await ctx.respond(embed=embed)
        except aiohttp.ClientError:
            embed = discord.Embed(title = "Error", description = f"An error occurred while fetching data from the API. Please contact @{self.bot.ownername}.")
            embed.color = discord.Colour.red()
            await ctx.respond(embed=embed)
        except asyncio.TimeoutError:
            embed = discord.Embed(title = "Error", description = f"The request to the API timed out. Please contact @{self.bot.ownername}.")
            embed.color = discord.Colour.red()
            await ctx.respond(embed=embed)

    async def intelcpu(self, ctxauthor):
        # Get data from API
        endpoint = "https://api.nikolan.xyz/intel-cpu"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, timeout=3) as response:
                    response.raise_for_status()
                    if response.status == 200:
                        data = await response.json()
        except aiohttp.ClientError:
            embed = discord.Embed(title = "Error", description = f"An error occurred while fetching data from the API. Please contact @{self.bot.ownername}.")
            embed.color = discord.Colour.red()
            return embed
        except asyncio.TimeoutError:
            embed = discord.Embed(title = "Error", description = f"The request to the API timed out. Please contact @{self.bot.ownername}.")
            embed.color = discord.Colour.red()
            return embed
        except Exception:
                embed = discord.Embed(title = "Error", description = f"An unknown error occured. Please contact @{self.bot.ownername}.")
                embed.color = discord.Colour.red()
                return embed
        
        # Process data
        if data:
            cpu_info = data.get("cpu")
            if cpu_info:
                ghzs = f"**Base Frequency** {cpu_info['Base Freq.(GHz)']}GHz" if cpu_info['Max. Turbo Freq.(GHz)'] == "N/A" else f"**Base/Max Frequency** {cpu_info['Base Freq.(GHz)']}/{cpu_info['Max. Turbo Freq.(GHz)']}GHz"
                embed = discord.Embed(title=f"Intel {cpu_info['Product']}", color=0x2494A1, description=f"**Cores/Threads** {cpu_info['Cores']}c{cpu_info['Threads']}t\n**Release Date** {cpu_info['Release Date']}\n**TDP** {cpu_info['TDP(W)']}W\n**Lithography** {cpu_info['Lithography(nm)']}nm\n{ghzs}")
                embed.set_footer(text=f"Requested by {ctxauthor} | api.nikolan.xyz/intel-cpu")
                return embed
            else:
                embed = discord.Embed(title = "Error", description = f"An error occurred while fetching CPU data from the API. Try again later.")
                embed.color = discord.Colour.red()
                return embed
        
    async def amdcpu(self, ctxauthor):
        # Get data from API
        endpoint = "https://api.nikolan.xyz/amd-cpu"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(endpoint, timeout=3) as response:
                    response.raise_for_status()
                    if response.status == 200:
                        cpu_info = await response.json()
            except aiohttp.ClientError:
                embed = discord.Embed(title = "Error", description = f"An error occurred while fetching data from the API. Please contact @{self.bot.ownername}.")
                embed.color = discord.Colour.red()
                return embed
            except asyncio.TimeoutError:
                embed = discord.Embed(title = "Error", description = f"The request to the API timed out. Please contact @{self.bot.ownername}.")
                embed.color = discord.Colour.red()
                return embed
            except Exception:
                embed = discord.Embed(title = "Error", description = f"An unknown error occured. Please contact @{self.bot.ownername}.")
                embed.color = discord.Colour.red()
                return embed
        
        # Process data
        if cpu_info:
            stupid = "\u00c2\u00b9 \u00c2\u00b2"
            cpumodel = cpu_info['Model']
            clockbase = cpu_info['Base Clock'].replace('GHz', '')
            clockmax = cpu_info[f'Max. Boost Clock {stupid}'].replace("GHz", "").replace("Up to ", "")
            rdate = cpu_info['Launch Date']
            if rdate == "":
                rdate = "Unknown"
            if not "AMD" in str(cpumodel):
                cpumodel = f"AMD {cpumodel}"
            tdp = cpu_info['Default TDP']
            if tdp == "":
                tdp = "Unknown"
            cpumodel = cpumodel.replace("â„¢", "")
            embed = discord.Embed(
                title=f"{cpumodel}",
                color=0xff0000,
                description=f"""**Cores/Threads** {cpu_info['# of CPU Cores']}c{cpu_info['# of Threads']}t
            **Release Date** {rdate}
            **TDP** {tdp}
            **Lithography** {cpu_info['Processor Technology for CPU Cores']}
            **Base/Max Frequency** {clockbase}/{clockmax}GHz""")

            embed.set_footer(text=f"Requested by {ctxauthor} | api.nikolan.xyz/amd-cpu")
            return embed
        else:
            embed = discord.Embed(title = "Error", description = f"An error occurred while fetching CPU data from the API. Try again later.")
            embed.color = discord.Colour.red()
            return embed

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="cpu", description="Sends a random Intel or AMD CPU.")
    @commands.cooldown(1, 3, BucketType.user)
    async def random_cpu(self, ctx):
        await ctx.defer(ephemeral=False)
        view = discord.ui.View(timeout=None)
        async def randintel(interaction):
            the = await self.intelcpu(ctx.author.name)
            await interaction.respond(embed=the, view=view)
        async def randamd(interaction):
            the = await self.amdcpu(ctx.author.name)
            await interaction.respond(embed=the, view=view)
        intelb = discord.ui.Button(label="Intel", style=discord.ButtonStyle.blurple)
        amdb = discord.ui.Button(label="AMD", style=discord.ButtonStyle.red)
        intelb.callback = randintel
        amdb.callback = randamd
        view.add_item(intelb)
        view.add_item(amdb)
        if random.choice(["intel", "amd"]) == "intel":
            the = await self.intelcpu(ctx.author.name)
            return await ctx.respond(embed=the, view=view)
        else:
            the = await self.amdcpu(ctx.author.name)
            return await ctx.respond(embed=the, view=view)

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="random-gpu", description="Sends a random Nvidia or AMD GPU.")
    @commands.cooldown(1, 3, BucketType.user)
    async def random_gpu(self, ctx):
        await ctx.defer(ephemeral=False)

        if random.choice(["nvidia", "amd"]) == "nvidia":
            # Get data from API
            endpoint = "https://api.nikolan.xyz/nvidia-gpu"
            data = await self.fetch_data(ctx, endpoint)
            
            # Process data
            if data:
                gpuname = data["gpu"]
                if not "nvidia" in gpuname.lower():
                    gpuname = f"Nvidia {gpuname}"
                embed = discord.Embed(title=gpuname, color=0x00ff00)
                embed.set_footer(text=f"Requested by {ctx.author.name} | api.nikolan.xyz/nvidia-gpu")
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title = "Error", description = f"An error occurred while fetching GPU data from the API. Try again later.")
                embed.color = discord.Colour.red()
                await ctx.respond(embed=embed)
        else:
            # Get data from API
            endpoint = "https://api.nikolan.xyz/amd-gpu"
            cpu_info = await self.fetch_data(ctx, endpoint)
            
            # Process data
            if cpu_info:
                cpumodel = cpu_info['Model']
                rdate = cpu_info['Launch Date']
                tdp = cpu_info['Typical Board Power (Desktop)']
                maxvram = cpu_info['Max Memory Size']
                ramtype = cpu_info['Memory Type']
                embed = discord.Embed(
                    title=f"{cpumodel}",
                    color=0xff0000,
                    description=f"""
                **Release Date** {rdate}
                **VRAM**: Up to {maxvram} {ramtype}
                **TBP** {tdp}
                """)
                embed.set_footer(text=f"Requested by {ctx.author.name} | api.nikolan.xyz/amd-gpu")
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title = "Error", description = f"An error occurred while fetching GPU data from the API. Try again later.")
                embed.color = discord.Colour.red()
                await ctx.respond(embed=embed)
    
    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="amd-gpu", description="Sends a random AMD GPU.")
    @commands.cooldown(1, 3, BucketType.user)
    async def gpumyy(self, ctx):
        # Get data from API
        endpoint = "https://api.nikolan.xyz/amd-gpu"
        cpu_info = await self.fetch_data(ctx, endpoint)
        
        # Process data
        if cpu_info:
            cpumodel = cpu_info['Model']
            rdate = cpu_info['Launch Date']
            tdp = cpu_info['Typical Board Power (Desktop)']
            maxvram = cpu_info['Max Memory Size']
            ramtype = cpu_info['Memory Type']
            embed = discord.Embed(
                title=f"{cpumodel}",
                color=0xff0000,
                description=f"""
            **Release Date** {rdate}
            **VRAM**: Up to {maxvram} {ramtype}
            **TBP** {tdp}
            """)
            embed.set_footer(text=f"Requested by {ctx.author.name} | api.nikolan.xyz/amd-gpu")
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title = "Error", description = f"An error occurred while fetching GPU data from the API. Try again later.")
            embed.color = discord.Colour.red()
            await ctx.respond(embed=embed)

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="nvidia-gpu", description="Sends a random Nvidia GPU.")
    @commands.cooldown(1, 3, BucketType.user)
    async def nvgpu(self, ctx):
        # Get data from API
        endpoint = "https://api.nikolan.xyz/nvidia-gpu"
        data = await self.fetch_data(ctx, endpoint)
        
        # Process data
        if data:
            gpuname = data["gpu"]
            if not "nvidia" in gpuname.lower():
                gpuname = f"Nvidia {gpuname}"
            embed = discord.Embed(title=gpuname, color=0x00ff00)
            embed.set_footer(text=f"Requested by {ctx.author.name} | api.nikolan.xyz/nvidia-gpu")
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title = "Error", description = f"An error occurred while fetching GPU data from the API. Try again later.")
            embed.color = discord.Colour.red()
            await ctx.respond(embed=embed)

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="95cdkey", description="Generates a Windows 95 CD Key.")
    @commands.cooldown(1, 3, BucketType.user)
    async def nfcdkey(self, ctx):
        # Get data from API
        endpoint = "https://api.nikolan.xyz/95cdkey"
        data = await self.fetch_data(ctx, endpoint)
        
        # Process data
        if data:
            embed = discord.Embed(title="Windows 95 CD Key", color=0x2494A1, description=f"{data['cdkey']}")
            embed.set_footer(text=f"Requested by {ctx.author.name} | api.nikolan.xyz/95cdkey")
            embed.set_thumbnail(url="https://64.media.tumblr.com/f0b0786998dc2e44bfe179e9da3fa116/39dad773e2bb50bc-4c/s540x810/3534cc436c2b90f526bd483f632d0ff804a80e7b.gif")
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title = "Error", description = f"An error occurred while fetching key data from the API. Try again later.")
            embed.color = discord.Colour.red()
            await ctx.respond(embed=embed)

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="8ball", description="yes")
    @commands.cooldown(1, 3, BucketType.user)
    async def ebll(self, ctx, texty: discord.Option(str, name="question", description="The question for 8ball")): # type: ignore
        # Get data from API
        endpoint = f"https://api.nikolan.xyz/8ball?question={texty}"
        data = await self.fetch_data(ctx, endpoint)
        
        # Process data
        if data:
            embed = discord.Embed(title="🎱 8ball", color=0x2494A1, description=f"❓ Question: {texty}\n**🎱 8ball: {data['answer']}**")
            embed.set_footer(text=f"Requested by {ctx.author.name} | api.nikolan.xyz/8ball")
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title = "Error", description = f"An error occurred while fetching 8 ball data from the API. Try again later.")
            embed.color = discord.Colour.red()
            await ctx.respond(embed=embed)

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="scramble", description="Scrambles text.")
    @commands.cooldown(1, 3, BucketType.user)
    async def scrmbol(self, ctx, texty: discord.Option(str, name="text", description="The text to scramble.")): # type: ignore
        # Get data from API
        endpoint = f"https://api.nikolan.xyz/scramble?text={texty}"
        data = await self.fetch_data(ctx, endpoint)
        
        # Process data
        if data:
            embed = discord.Embed(title="Scramble", color=0x2494A1, description=f"**Oops, I scrambled it:** {data['scrambled_text']}")
            embed.set_footer(text=f"Requested by {ctx.author.name} | api.nikolan.xyz/scramble")
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title = "Error", description = f"An error occurred while fetching scrambled data from the API. Try again later.")
            embed.color = discord.Colour.red()
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(apicmds(bot))
