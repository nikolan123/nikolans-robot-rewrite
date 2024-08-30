import discord
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed

class suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    contactgroup = discord.SlashCommandGroup(name="contact", integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install})

    @contactgroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="suggest", description="Suggest a feature to the bot's developers.")
    async def suggestion(self, ctx, the: discord.Option(str, name="suggestion", description="Your suggestion")): # type: ignore
        rlhook = DiscordWebhook(url=self.bot.suggestionshook, username=f"{self.bot.logginghookname} - suggestions")
        rlembed = DiscordEmbed(title="New suggestion!", description=f"User {ctx.author.name} ({ctx.author.id}):\n\n>>> {the}", color="7adedb")
        rlembed.set_timestamp()
        rlhook.add_embed(rlembed)
        rlhook.execute()    
        
        embed = discord.Embed(title = "Thank you!", description = f"We have recieved your suggestion.")
        embed.color = discord.Colour.green()
        await ctx.respond(embed=embed, ephemeral=True)
        
    @contactgroup.command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="bugreport", description="Report a bug to the bot's developers.")
    async def bugreport(self, ctx, the: discord.Option(str, name="bug", description="Describe the bug you found")): # type: ignore
        rlhook = DiscordWebhook(url=self.bot.suggestionshook, username=f"{self.bot.logginghookname} - bug report")
        rlembed = DiscordEmbed(title="New bug report!", description=f"User {ctx.author.name} ({ctx.author.id}):\n\n>>> {the}", color="7adedb")
        rlembed.set_timestamp()
        rlhook.add_embed(rlembed)
        rlhook.execute()    

        embed = discord.Embed(title = "Thank you!", description = f"We have recieved your bug report.")
        embed.color = discord.Colour.green()
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(suggestions(bot))
