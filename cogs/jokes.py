import discord
from discord.ext import commands
from discord.ext.commands import BucketType

class Joke(commands.Cog):
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

        # Button callback function
        async def why_callback(interaction):
            await interaction.respond("Because to stagnate is to die. Never forget that.")

        # Create the button
        why_button = discord.ui.Button(label="Why?", style=discord.ButtonStyle.gray)
        why_button.callback = why_callback

        # Add the button to the view
        view.add_item(why_button)

        # Respond with the initial joke and the button
        await ctx.respond("Why did the chicken cross the road?", view=view)

# Setup function to add the cog to the bot
def setup(bot):
    bot.add_cog(Joke(bot))
