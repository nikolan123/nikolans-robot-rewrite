import discord
from discord.ext import commands
import random

class misccmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.slash_command(name="pipeyhit", description="Hits someone with metal pipey.")
    async def pipeyhit(self, ctx, victim: discord.Option(discord.User, "The user you want to hit"), pingusr: discord.Option(bool, name="ping", description="Ping the victim") = False): # type: ignore
        embed = discord.Embed(
            title="Metal Pipey Hit",
            description=f":wrench: <@{victim.id}> got hit with metal pipey!!",
            color=0xFF0000,
        )
        embed.set_thumbnail(
            url="https://static.wikia.nocookie.net/object-trek/images/0/0c/Pipey.png/revision/latest/scale-to-width/360?cb=20170904212026"
        )
        
        embedDone = discord.Embed(title = "Done!")
        embedDone.color = discord.Colour.green()
        await ctx.respond(embed=embedDone, ephemeral=True)
        
        if pingusr:
            await ctx.send(embed=embed, content=victim.mention)
        else:
            await ctx.send(embed=embed)

    @commands.slash_command(name="members", description="Shows the server's member count.")
    async def members(self, ctx):
        bot_count = sum(1 for member in ctx.guild.members if member.bot)
        member_count = sum(1 for member in ctx.guild.members if not member.bot)
        embed = discord.Embed(title="Server Members",
                        description=f"**Bots:** {bot_count}\n**Members:** {member_count}",
                        colour=0x00b0f4)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.respond(embed=embed)

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="avatar", description="Gets a user's avatar")
    async def avatar_command(self, ctx, usery: discord.Option(discord.Member, name="user", description="The user to get the avatar of")): # type: ignore
        embed = discord.Embed(title=f"{usery.name}'s Avatar", url=usery.avatar.url, image=usery.avatar.url, colour=0x00b0f4)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.respond(embed=embed)

    @commands.slash_command(name="sleep", description="Tells others you're going to sleep.")
    async def sleep(self, ctx):
        embed = discord.Embed(
            title=f"{ctx.author.name} is going to sleep",
            description="Everyone wish them good night!",
            colour=0x55C5FF,
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1247/1247769.png")
        await ctx.respond(embed=embed)

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name='random-color', description='Generates a random color')
    async def random_color(self, ctx):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        color_hex = "#{:02x}{:02x}{:02x}".format(red, green, blue)
        embed = discord.Embed(title="Random Color", description=color_hex, color=discord.Color(int(color_hex[1:], 16)))
        await ctx.respond(embed=embed)  
    
def setup(bot):
    bot.add_cog(misccmds(bot))
