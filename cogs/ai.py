import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from discord.ui import View
import aiohttp
import g4f
from time import sleep

class ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="ai", description="Generates text using AI.")
    @commands.cooldown(1, 6, BucketType.user)
    async def aicmdy(self, ctx, prompt: discord.Option(str, name="prompt", description="Your prompt for the AI.")): # type: ignore
        #send loading embed
        embed = discord.Embed(title="Generating, please wait...", colour=0x00B0F4)
        embed.set_thumbnail(
            url="https://media.tenor.com/czYMSjtm8goAAAAC/windows10-windows10loading.gif"
        )
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.respond(embed=embed)
        #generate and replace @ to prevent pings
        aresponse = "not yet"
        try:
            aresponse = await g4f.ChatCompletion.create_async(
                model=g4f.models.default,
                messages=[{"role": "user", "content": prompt}],
                provider=g4f.Provider.Blackbox
            )
        except Exception as e:
            print(e)
        while aresponse == "not yet":
            sleep(1)
        aresponse = (
            aresponse
            .replace("@", "_")
            .replace("##", "#")
        )
        #check if discord can send, otherwise upload to upaste.de
        if len(aresponse) > 1957:
            url = "https://upaste.de/"
            form_data = aiohttp.FormData()
            form_data.add_field('text', aresponse)
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=form_data) as response:
                    ufembed = discord.Embed(title="Response Uploaded", description="The AI's response was over 2000 characters, so it was uploaded to a [third-party website](https://upaste.de).", colour=0x00B0F4)
                    ufembed.set_footer(text=f"Requested by {ctx.author.name}")
                
                    view = View(timeout=None)
                    view.add_item(discord.ui.Button(label = "View Response", url = str(response.url), style = discord.ButtonStyle.url))

            await ctx.edit(embed=ufembed, view = view)
            return
        dembed = discord.Embed(description=aresponse, color=0x00B0F4)
        dembed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.edit(embed=dembed)#content=f"> Generated using model gpt-3.5-turbo\n> Requested by {ctx.author.name} \n{aresponse}", embed=None)


    # @commands.slash_command(name="local_ai", description="Generates text using AI")
    # @commands.cooldown(1, 6, BucketType.user)
    # async def localaicmdy(self, ctx, prompt: discord.Option(str, name="prompt", description="The prompt for the ai")): # type: ignore
    #     #send loading embed
    #     embed = discord.Embed(title="Generating, please wait...", colour=0x00B0F4)
    #     embed.set_thumbnail(
    #         url="https://media.tenor.com/czYMSjtm8goAAAAC/windows10-windows10loading.gif"
    #     )
    #     embed.set_footer(text=f"Requested by {ctx.author.name}")

    #     await ctx.respond(embed=embed)
    #     #generate and replace @ to prevent pings
    #     aresponse = "not yet"
    #     try:
    #         #generation
    #         url = 'http://localhost:11434/api/generate'
    #         data = {
    #             "system": "You are an AI assistant for an AI command in a Discord bot called 'nikolan's robot' by the developer nikolan (the capitalisation and spelling is correct, don't modify that). The bot is written in Python and you (the ai) runs on his main PC with an Intel Core i3-12100 (12th gen), 32GB of DDR4 3200MT/s and an AMD RX 7600, don't mention any of this sentence unless asked. You are respectful to all users, try to provide useful information and you are allowed to use markdown. Do not say things that may be unethical or break the Discord ToS. Don't use too many emojis and don't roleplay.",
    #             "model": "llama2",
    #             "prompt": prompt,
    #             "stream": False
    #         }
            
    #         async with aiohttp.ClientSession() as session:
    #             async with session.post(url, json=data) as response:
    #                 aresponse = await response.json()
    #                 aresponse = aresponse['response']
    #                 """ json_lines = thanswe.strip().split('\n')
    #                 responses = [json.loads(line)['response'] for line in json_lines]
    #                 aresponse = ''.join(responses) """
    #     except Exception as e:
    #         print(e)
    #     while aresponse == "not yet":
    #         sleep(1)
    #     aresponse = (
    #         aresponse
    #         .replace("@", "_")
    #         .replace("##", "#")
    #     )
    #     #check if discord can send, otherwise upload to upaste.de
    #     if len(aresponse) > 1957:
    #         url = "https://upaste.de/"
    #         payload = f'-----011000010111000001101001\r\nContent-Disposition: form-data; name="text"\r\n\r\{aresponse}\r\n-----011000010111000001101001--\r\n'
    #         headers = {
    #             "content-type": "multipart/form-data; boundary=---011000010111000001101001"
    #         }
    #         response = requests.post(url, data=payload, headers=headers)
    #         ufembed = discord.Embed(url=response.url, title="Click to view response", description="The AI's response was over 2000 characters, so it was uploaded to a [third-party website](https://upaste.de).", colour=0x00B0F4)
    #         ufembed.set_footer(text=f"Requested by {ctx.author.name}")
    #         await ctx.edit(embed=ufembed)
    #         return
    #     dembed = discord.Embed(description=aresponse, color=0x00B0F4)
    #     dembed.set_footer(text=f"Requested by {ctx.author.name}")
    #     await ctx.edit(embed=dembed)#content=f"> Generated using model gpt-3.5-turbo\n> Requested by {ctx.author.name} \n{aresponse}", embed=None)

    
def setup(bot):
    bot.add_cog(ai(bot))
