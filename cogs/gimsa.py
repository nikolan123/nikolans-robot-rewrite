import discord
from discord.ext import commands
from bing_image_urls import bing_image_urls
from time import sleep

class gimsathing(discord.ui.View):
    def __init__(self, ctx, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        self.imgurl = ctx.imgurl
        self.counter = 0  # Initialize the counter
        self.lengthy = ctx.lengthy
    
    @discord.ui.button(label="Back", style=discord.ButtonStyle.primary, emoji="⬅️")
    async def back_button_callback(self, button, interaction):
        if self.ctx.author.id == interaction.user.id:
            self.counter = (self.counter - 1) % len(self.imgurl)  # Decrement the counter and loop back to the end if it goes below 0
            embed = discord.Embed(title=f"Image {self.counter+1}/{self.lengthy}", image=self.imgurl[self.counter].replace(' ', '%20'), colour=0x00b0f4)
            embed.set_footer(text=f"Requested by {self.ctx.author.name}")
            await interaction.response.edit_message(embed=embed)#content=f"Image [{self.counter+1}/{self.lengthy}]({self.imgurl[self.counter].replace(' ', '%20')})")
        else:
            await interaction.response.send_message(f"Only {self.ctx.author.mention} is allowed to do that.", ephemeral=True)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary, emoji="➡️")
    async def next_button_callback(self, button, interaction):
        if self.ctx.author.id == interaction.user.id:
            self.counter = (self.counter + 1) % len(self.imgurl)  # Increment the counter and loop back to 0 if it exceeds the list length
            embed = discord.Embed(title=f"Image {self.counter+1}/{self.lengthy}", image=self.imgurl[self.counter].replace(' ', '%20'), colour=0x00b0f4)
            embed.set_footer(text=f"Requested by {self.ctx.author.name}")
            await interaction.response.edit_message(embed=embed)#content=f"Image [{self.counter+1}/{self.lengthy}]({self.imgurl[self.counter].replace(' ', '%20')})")
        else:
            await interaction.response.send_message(f"Only {self.ctx.author.mention} is allowed to do that.", ephemeral=True)

class gimsacmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name="gimsa", description="Searches Bing for images")
    async def sgimsa(self, ctx, query: discord.Option(str, description="The thing to search for", name="prompt")): # type: ignore
        imgurldirty = bing_image_urls(query, limit=20)
        ctx.imgurl = [url for url in imgurldirty if "reddit.com" not in url and "preview" not in url and (url.endswith('.png') or url.endswith('.jpg') or url.endswith('.jpeg'))]
        ctx.lengthy = len(ctx.imgurl)
        #await ctx.respond(f"Left {ctx.lengthy} out of 20 images")
        #sleep(3)
        embed = discord.Embed(title=f"Image 1/{ctx.lengthy}", image=ctx.imgurl[0].replace(' ', '%20'), colour=0x00b0f4)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.respond(embed=embed, view=gimsathing(ctx))

def setup(bot):
    bot.add_cog(gimsacmd(bot))
