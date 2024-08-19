import discord
from discord.ext import commands
from discord.ext.commands import BucketType

class joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(
        name="joke",
        description="Why did the chicken cross the road?",
        integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install}
    )
    @commands.cooldown(1, 3, BucketType.user)
    async def joke(self, ctx):
        await ctx.defer(ephemeral=False)
        view = discord.ui.View(timeout=None)
        async def why_callback(interaction):
            await interaction.respond("Because to stagnate is to die. Never forget that.")
        why_button = discord.ui.Button(label="Why?", style=discord.ButtonStyle.gray)
        why_button.callback = why_callback
        view.add_item(why_button)
        await ctx.respond("Why did the chicken cross the road?", view=view)
def setup(bot):
    bot.add_cog(joke(bot))
