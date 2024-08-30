import discord
from discord.ext import commands
import aiohttp
import html
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
                product = cpu_info.get('Product', 'Unknown') or 'Unknown'
                base_freq = cpu_info.get('Base Freq.(GHz)', '').replace('GHz', '')
                max_turbo_freq = cpu_info.get('Max. Turbo Freq.(GHz)', '').replace('GHz', '')
                cores = cpu_info.get('Cores', 'Unknown') or 'Unknown'
                threads = cpu_info.get('Threads', 'Unknown') or 'Unknown'
                release_date = cpu_info.get('Release Date', 'Unknown') or 'Unknown'
                tdp = cpu_info.get('TDP(W)', 'Unknown') or 'Unknown'
                lithography = cpu_info.get('Lithography(nm)', 'Unknown') or 'Unknown'
                
                base_freq = base_freq if base_freq and base_freq != "N/A" else "Unknown"
                max_turbo_freq = max_turbo_freq if max_turbo_freq and max_turbo_freq != "N/A" else "Unknown"
                cores = cores if cores and cores != "N/A" else "Unknown"
                threads = threads if threads and threads != "N/A" else "Unknown"
                release_date = release_date if release_date and release_date != "N/A" else "Unknown"
                tdp = tdp if tdp and tdp != "N/A" else "Unknown"
                lithography = lithography if lithography and lithography != "N/A" else "Unknown"

                if max_turbo_freq == "Unknown":
                    ghzs = f"**Base Frequency** {base_freq}GHz"
                else:
                    ghzs = f"**Base/Max Frequency** {base_freq}/{max_turbo_freq}GHz"

                embed = discord.Embed(
                    title=f"Intel {product}",
                    color=0x2494A1,
                    description=f"""**Cores/Threads** {cores}c{threads}t
            **Release Date** {release_date}
            **TDP** {tdp}W
            **Lithography** {lithography}nm
            {ghzs}"""
                )
                embed.set_footer(text=f"Requested by {ctxauthor} | api.nikolan.xyz/intel-cpu")

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
            cpumodel = cpu_info.get('Model', 'Unknown') or 'Unknown'
            clockbase = cpu_info.get('Base Clock', '').replace('GHz', '') or 'Unknown'
            clockmax = cpu_info.get(f'Max. Boost Clock', '').replace("GHz", "").replace("Up to ", "") or 'Unknown'
            rdate = cpu_info.get('Launch Date', 'Unknown') or 'Unknown'
            tdp = cpu_info.get('Default TDP', 'Unknown') or 'Unknown'
            lithography = cpu_info.get('Processor Technology for CPU Cores', 'Unknown') or 'Unknown'
            cores = cpu_info.get('# of CPU Cores', '0') or '0'
            threads = cpu_info.get('# of Threads', '0') or '0'

            # Format CPU model if it doesn't already contain "AMD"
            if "AMD" not in str(cpumodel):
                cpumodel = f"AMD {cpumodel}"

            cpumodel = cpumodel.replace("â„¢", "")

            embed = discord.Embed(
                title=cpumodel,
                color=0xff0000,
                description=f"""**Cores/Threads** {cores}c/{threads}t
**Release Date** {rdate}
**TDP** {tdp}
**Lithography** {lithography}
**Base/Max Frequency** {clockbase}/{clockmax}GHz"""
            )
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

        async def randany(interaction):
            nonlocal view
            if random.choice(["intel", "amd"]) == "intel":
                the = await self.intelcpu(interaction.user.name)
            else:
                the = await self.amdcpu(interaction.user.name)
            await interaction.respond(embed=the, view=view)

        async def randintel(interaction):
            nonlocal view
            the = await self.intelcpu(interaction.user.name)
            await interaction.respond(embed=the, view=view)

        async def randamd(interaction):
            nonlocal view
            the = await self.amdcpu(interaction.user.name)
            await interaction.respond(embed=the, view=view)

        anyb = discord.ui.Button(label="Any", style=discord.ButtonStyle.gray)
        intelb = discord.ui.Button(label="Intel", style=discord.ButtonStyle.blurple)
        amdb = discord.ui.Button(label="AMD", style=discord.ButtonStyle.red)
        anyb.callback = randany
        intelb.callback = randintel
        amdb.callback = randamd
        view.add_item(anyb)
        view.add_item(intelb)
        view.add_item(amdb)

        if random.choice(["intel", "amd"]) == "intel":
            the = await self.intelcpu(ctx.author.name)
            return await ctx.respond(embed=the, view=view)
        else:
            the = await self.amdcpu(ctx.author.name)
            return await ctx.respond(embed=the, view=view)

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="gpu", description="Sends a random Nvidia or AMD GPU.")
    @commands.cooldown(1, 3, BucketType.user)
    async def random_gpu(self, ctx):
        await ctx.defer(ephemeral=False)
        view = discord.ui.View(timeout=None)

        async def amdgpu(interaction):
            nonlocal view
            try:
                await interaction.response.defer()
            except discord.errors.InteractionResponded:
                pass
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
                try:
                    authorname = interaction.author.name
                except:
                    authorname = interaction.user.name
                embed.set_footer(text=f"Requested by {authorname} | api.nikolan.xyz/amd-gpu")
                await interaction.respond(embed=embed, view=view)

        async def nvidiagpu(interaction):
            nonlocal view
            try:
                await interaction.response.defer()
            except discord.errors.InteractionResponded:
                pass
            endpoint = "https://api.nikolan.xyz/nvidia-gpu"
            data = await self.fetch_data(ctx, endpoint)
            
            # Process data
            if data:
                gpuname = data["gpu"]
                if not "nvidia" in gpuname.lower():
                    gpuname = f"Nvidia {gpuname}"
                embed = discord.Embed(title=gpuname, color=0x00ff00)
                try:
                    authorname = interaction.author.name
                except:
                    authorname = interaction.user.name
                embed.set_footer(text=f"Requested by {authorname} | api.nikolan.xyz/nvidia-gpu")
                await ctx.respond(embed=embed, view=view)
            else:
                embed = discord.Embed(title = "Error", description = f"An error occurred while fetching GPU data from the API. Try again later.")
                embed.color = discord.Colour.red()
                await interaction.respond(embed=embed, view=view)
        
        async def anygpu(interaction):
            if random.choice(["amd", "nvidia"]) == "amd":
                await amdgpu(interaction)
            else:
                await nvidiagpu(interaction)

        anyb = discord.ui.Button(label="Any", style=discord.ButtonStyle.gray)
        amdb = discord.ui.Button(label="AMD", style=discord.ButtonStyle.red)
        nvidiab = discord.ui.Button(label="Nvidia", style=discord.ButtonStyle.green)
        anyb.callback = anygpu
        amdb.callback = amdgpu
        nvidiab.callback = nvidiagpu

        view.add_item(anyb)
        view.add_item(amdb)
        view.add_item(nvidiab)

        await anygpu(ctx)
            
    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="8ball", description="yes")
    @commands.cooldown(1, 3, BucketType.user)
    async def eightball(self, ctx, texty: discord.Option(str, name="question", description="The question for 8ball")): # type: ignore
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
    async def scramble_command(self, ctx, texty: discord.Option(str, name="text", description="The text to scramble.")): # type: ignore
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

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="fbiwanted", description="Shows the FBI wanted list.")
    @commands.cooldown(1, 15, BucketType.user)
    async def fbiwanted(self, ctx):  # type: ignore
        async def genpage(infoy):
            imgurl = f"https://external-content.duckduckgo.com/iu/?u={infoy['images'][0]['thumb']}"
            embed = discord.Embed(title="FBI Wanted List", thumbnail=imgurl, description=f"**{infoy['title']}**\n{html.unescape(infoy['description'])}")
            if infoy['age_range']:
                embed.add_field(name="Age Range", value=infoy['age_range'])
            if infoy['eyes_raw']:
                embed.add_field(name="Eye Color", value=infoy['eyes_raw'])
            if infoy['place_of_birth']:
                embed.add_field(name="Place of Birth", value=infoy['place_of_birth'])
            if infoy['reward_text']:
                embed.add_field(name="Reward", value=infoy['reward_text'])
            if infoy['languages']:
                langs = ", ".join(infoy['languages'])
                embed.add_field(name="Languages", value=langs)
            return embed
        async def fetchpage(page_num):
            endpoint = f"https://api.fbi.gov/wanted/v1/list?page={page_num}"
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0"
                }
                async with aiohttp.ClientSession(headers=headers) as session:
                    async with session.get(endpoint) as response:
                        response.raise_for_status()  
                        data = await response.json()
                        return data
            except Exception as e:
                print(e)
                return None
        
        counter = 0
        page_num = 1
        data = await fetchpage(page_num)
        
        if not data:
            embed = discord.Embed(title="Error", description="An error occurred while fetching data from the API. Try again later.")
            embed.color = discord.Colour.red()
            await ctx.respond(embed=embed)
            return

        total_entries = data['total']
        items_per_page = len(data['items'])

        # discord view
        view = discord.ui.View(timeout=None)

        async def backcb(interaction):
            await interaction.response.defer()
            nonlocal counter
            nonlocal page_num
            nonlocal data
            if counter == 0:
                if page_num == 1:
                    # go to last page
                    page_num = (total_entries // items_per_page) + (1 if total_entries % items_per_page > 0 else 0)
                    data = await fetchpage(page_num)
                    counter = len(data['items']) - 1
                else:
                    # go back
                    page_num -= 1
                    data = await fetchpage(page_num)
                    counter = len(data['items']) - 1

            else:
                counter -= 1

            embed = await genpage(data['items'][counter])
            embed.set_footer(text=f"{(page_num-1)*items_per_page + counter + 1}/{total_entries}")
            msg = await interaction.original_response()
            await msg.edit(embed=embed, view=view)

        async def nextcb(interaction):
            await interaction.response.defer()
            nonlocal counter
            nonlocal page_num
            nonlocal data
            
            counter += 1

            if counter >= len(data['items']):
                page_num += 1
                counter = 0
                data = await fetchpage(page_num)

                if not data or not data['items']:
                    if page_num == 1:
                        return await interaction.respond("No more entries.", ephemeral=True)
                    page_num = 1
                    counter = 0
                    data = await fetchpage(page_num)
                    if not data or not data['items']:
                        return await interaction.respond("No more entries.", ephemeral=True)

            embed = await genpage(data['items'][counter])
            embed.set_footer(text=f"{(page_num-1)*len(data['items']) + counter + 1}/{total_entries}")
            
            msg = await interaction.original_response()
            await msg.edit(embed=embed, view=view)
            embed = await genpage(data['items'][counter])
            embed.set_footer(text=f"{(page_num-1)*items_per_page + counter + 1}/{total_entries}")
            
            msg = await interaction.original_response()
            await msg.edit(embed=embed, view=view)

        backbutton = discord.ui.Button(label="Back", style=discord.ButtonStyle.blurple)
        nextbutton = discord.ui.Button(label="Next", style=discord.ButtonStyle.blurple)
        backbutton.callback = backcb
        nextbutton.callback = nextcb
        view.add_item(backbutton)
        view.add_item(nextbutton)

        try:
            embed = await genpage(data['items'][counter])
            embed.set_footer(text=f"{counter+1}/{total_entries}")
            await ctx.respond(embed=embed, view=view)
        except Exception as e:
            embed = discord.Embed(title="Error", description="An error occurred while processing the data.")
            embed.color = discord.Colour.red()
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(apicmds(bot))
