import discord
from discord.ext import commands
import aiohttp
from discord.ext.commands import BucketType

class apicmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name="intel-cpu", description="Sends a random Intel CPU")
    @commands.cooldown(1, 3, BucketType.user)
    async def cpur(self, ctx):
        await ctx.defer(ephemeral=False)
        #endpoint = "https://api.nikolan.xyz/intel-cpu"
        endpoint = "http://192.168.88.25:3032/intel-cpu"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    cpu_info = data.get("cpu")
                    if cpu_info:
                        ghzs = f"**Base Frequency** {cpu_info['Base Freq.(GHz)']}GHz" if cpu_info['Max. Turbo Freq.(GHz)'] == "N/A" else f"**Base/Max Frequency** {cpu_info['Base Freq.(GHz)']}/{cpu_info['Max. Turbo Freq.(GHz)']}GHz"                        
                        embed = discord.Embed(title=f"Intel {cpu_info['Product']}", color=0x2494A1, description=f"**Cores/Threads** {cpu_info['Cores']}c{cpu_info['Threads']}t\n**Release Date** {cpu_info['Release Date']}\n**TDP** {cpu_info['TDP(W)']}W\n**Lithography** {cpu_info['Lithography(nm)']}nm\n{ghzs}")
                        embed.set_footer(text=f"Requested by {ctx.author.name} | api.nikolan.xyz/intel-cpu")
                        await ctx.respond(embed=embed)
                    else:
                        await ctx.respond("Failed to fetch CPU information from the API.")
                else:
                    await ctx.respond(f"Failed to fetch data from the API. Status code: {response.status}")

    @commands.slash_command(name="amd-cpu", description="Sends a random AMD CPU")
    @commands.cooldown(1, 3, BucketType.user)
    async def cpum(self, ctx):
        endpoint = "https://api.nikolan.xyz/amd-cpu"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                if response.status == 200:
                    cpu_info = await response.json()
                    if cpu_info:
                        stupid = "\u00c2\u00b9 \u00c2\u00b2"
                        cpumodel = cpu_info['Model']
                        clockbase = cpu_info['Base Clock'].replace('GHz', '')
                        clockmax = cpu_info[f'Max. Boost Clock {stupid}'].replace("GHz", "").replace("Up to ", "")
                        rdate = cpu_info['Launch Date']
                        if rdate == "":
                            rdate = "Unknown"
                        if not "AMD" in cpumodel:
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

                        embed.set_footer(text=f"Requested by {ctx.author.name} | api.nikolan.xyz/amd-cpu")
                        await ctx.respond(embed=embed)
                    else:
                        await ctx.respond("Failed to fetch CPU information from the API.")
                else:
                    await ctx.respond(f"Failed to fetch data from the API. Status code: {response.status}")

    @commands.slash_command(name="amd-gpu", description="Sends a random AMD GPU")
    @commands.cooldown(1, 3, BucketType.user)
    async def gpumyy(self, ctx):
        endpoint = "https://api.nikolan.xyz/amd-gpu"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                if response.status == 200:
                    cpu_info = await response.json()
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
                        await ctx.respond("Failed to fetch CPU information from the API.")
                else:
                    await ctx.respond(f"Failed to fetch data from the API. Status code: {response.status}")

    @commands.slash_command(name="nvidia-gpu", description="Sends a random Nvidia GPU")
    @commands.cooldown(1, 3, BucketType.user)
    async def nvgpu(self, ctx):
        endpoint = "https://api.nikolan.xyz/nvidia-gpu"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    gpuname = data["gpu"]
                    if not "nvidia" in gpuname.lower():
                        gpuname = f"Nvidia {gpuname}"
                    embed = discord.Embed(title=gpuname, color=0x00ff00)
                    embed.set_footer(text=f"Requested by {ctx.author.name} | api.nikolan.xyz/nvidia-gpu")
                    await ctx.respond(embed=embed)
                else:
                    await ctx.respond(f"Failed to fetch data from the API. Status code: {response.status}")


    @commands.slash_command(name="95cdkey", description="Generates a Windows 95 CD Key")
    @commands.cooldown(1, 3, BucketType.user)
    async def nfcdkey(self, ctx):
        endpoint = "https://api.nikolan.xyz/95cdkey"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = discord.Embed(title="Windows 95 CD Key", color=0x2494A1, description=f"{data['cdkey']}")
                    embed.set_footer(text=f"Requested by {ctx.author.name} | api.nikolan.xyz/95cdkey")
                    embed.set_thumbnail(url="https://64.media.tumblr.com/f0b0786998dc2e44bfe179e9da3fa116/39dad773e2bb50bc-4c/s540x810/3534cc436c2b90f526bd483f632d0ff804a80e7b.gif")
                    await ctx.respond(embed=embed)
                else:
                    await ctx.respond(f"Failed to fetch data from the API. Status code: {response.status}")

    @commands.slash_command(name="8ball", description="yes")
    @commands.cooldown(1, 3, BucketType.user)
    async def ebll(self, ctx, texty: discord.Option(str, name="question", description="The question for 8ball")): # type: ignore
        endpoint = f"https://api.nikolan.xyz/8ball?question={texty}"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = discord.Embed(title="🎱 8ball", color=0x2494A1, description=f"❓ Question: {texty}\n**🎱 8ball: {data['answer']}**")
                    embed.set_footer(text=f"Requested by {ctx.author.name} | api.nikolan.xyz/8ball")
                    await ctx.respond(embed=embed)
                else:
                    await ctx.respond(f"Failed to fetch data from the API. Status code: {response.status}")

    @commands.slash_command(name="scramble", description="Scrambles text")
    @commands.cooldown(1, 3, BucketType.user)
    async def scrmbol(self, ctx, texty: discord.Option(str, name="text", description="The text to scramble")): # type: ignore
        endpoint = f"https://api.nikolan.xyz/scramble?text={texty}"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = discord.Embed(title="Scramble", color=0x2494A1, description=f"Oops I scrambled it: {data['scrambled_text']}")
                    embed.set_footer(text=f"Requested by {ctx.author.name} | api.nikolan.xyz/scramble")
                    await ctx.respond(embed=embed)
                else:
                    await ctx.respond(f"Failed to fetch data from the API. Status code: {response.status}")


def setup(bot):
    bot.add_cog(apicmds(bot))
