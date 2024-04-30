import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import requests
import g4f
from time import sleep

class ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name="ai", description="Generates text using AI")
    @commands.cooldown(1, 6, BucketType.user)
    async def aicmdy(self, ctx, prompt: discord.Option(str, name="prompt", description="The prompt for the ai")): # type: ignore
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
                provider=g4f.Provider.You,
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
            payload = f'-----011000010111000001101001\r\nContent-Disposition: form-data; name="text"\r\n\r\{aresponse}\r\n-----011000010111000001101001--\r\n'
            headers = {
                "content-type": "multipart/form-data; boundary=---011000010111000001101001"
            }
            response = requests.post(url, data=payload, headers=headers)
            ufembed = discord.Embed(url=response.url, title="Click to view response", description="The AI's response was over 2000 characters, so it was uploaded to a [third-party website](https://upaste.de).", colour=0x00B0F4)
            ufembed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.edit(embed=ufembed)
            return
        dembed = discord.Embed(description=aresponse, color=0x00B0F4)
        dembed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.edit(embed=dembed)#content=f"> Generated using model gpt-3.5-turbo\n> Requested by {ctx.author.name} \n{aresponse}", embed=None)
def setup(bot):
    bot.add_cog(ai(bot))
