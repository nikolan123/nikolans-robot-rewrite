import discord
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed


class suhestyons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name="suggest", description="Suggest a feature to the bot's developers.")
    async def sugesttt(self, ctx, the: discord.Option(str, name="suggestion", description="Your suggestion")): # type: ignore
        rlhook = DiscordWebhook(url=self.bot.suggestionshook, username=f"{self.bot.logginghookname} - suggestions")
        rlembed = DiscordEmbed(title="New suggestion!", description=f"User {ctx.author.name} ({ctx.author.id}):\n\n>>> {the}", color="7adedb")
        rlembed.set_timestamp()
        rlhook.add_embed(rlembed)
        rlhook.execute()    
        await ctx.respond("Thank you!", ephemeral=True)
    @commands.slash_command(name="bugreport", description="Report a bug to the bot's developers.")
    async def reeeeeefwrgfszfdg(self, ctx, the: discord.Option(str, name="bug", description="Describe the bug you found")): # type: ignore
        rlhook = DiscordWebhook(url=self.bot.suggestionshook, username=f"{self.bot.logginghookname} - bug report")
        rlembed = DiscordEmbed(title="New bug report!", description=f"User {ctx.author.name} ({ctx.author.id}):\n\n>>> {the}", color="7adedb")
        rlembed.set_timestamp()
        rlhook.add_embed(rlembed)
        rlhook.execute()    
        await ctx.respond("Thank you!", ephemeral=True)


def setup(bot):
    bot.add_cog(suhestyons(bot))
