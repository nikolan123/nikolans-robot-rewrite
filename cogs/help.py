import discord
from discord.ext import commands
from discord.ui import Button
import csv

async def autocompletehelp(ctx):
    with open('data/help.csv', 'r') as thefile:
        reader = csv.DictReader(thefile)
        misterarray = []
        for row in reader:
            if ctx.options['command'].lower() in row['command'].lower():
                misterarray.append(row['command'])
        return misterarray
    
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install}, name="help", description="Shows the bot's commands.")
    async def help_command(self, ctx, commandsys: discord.Option(str, name="command", autocomplete=autocompletehelp, description="(optional) The command to get help for") = None): # type: ignore
        if commandsys == None:
            try:
                await ctx.defer(ephemeral=False)
                commandslist = []
                commandspages = []
                counter = 0
                with open('data/help.csv', newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        command = {
                            "command": row["command"],
                            "description": row["description"],
                            "args": row["args"],
                            "screenshot": row["screenshot"]
                        }
                        commandslist.append(command)
                        counter += 1
                        if counter == 9:
                            commandspages.append(commandslist)
                            commandslist = []
                            counter = 0

                if commandslist:
                    commandspages.append(commandslist)
                pagesnum = 0
                for _ in commandspages:pagesnum += 1
                embed = discord.Embed(title=f"[1/{pagesnum}] Help")
                indexy = 0
                async def callbacktesty(interaction):
                    nonlocal indexy
                    indexy += 1
                    if indexy == pagesnum:
                        indexy = 0
                    embed = discord.Embed(title=f"[{indexy+1}/{pagesnum}] Help")
                    for f in commandspages[indexy]:
                        embed.add_field(name=f['command'], value=f['description'], inline=False)
                    await interaction.response.edit_message(embed=embed)
                async def callbacktestyb(interaction):
                    nonlocal indexy
                    indexy -= 1
                    if indexy == -1:
                        indexy = pagesnum-1
                    embed = discord.Embed(title=f"[{indexy+1}/{pagesnum}] Help")
                    for f in commandspages[indexy]:
                        embed.add_field(name=f['command'], value=f['description'], inline=False)
                    await interaction.response.edit_message(embed=embed)
                for f in commandspages[indexy]:
                    embed.add_field(name=f['command'], value=f['description'], inline=False)
                thev = discord.ui.View(timeout=None)
                but = Button(label="Next", style=discord.ButtonStyle.green)
                but.callback = callbacktesty
                butb = Button(label="Back", style=discord.ButtonStyle.green)
                butb.callback = callbacktestyb
                thev.add_item(butb)
                thev.add_item(but)
                await ctx.respond(embed=embed,view=thev)
            except Exception as e:
                embed = discord.Embed(title = "Error", description = f"Command broke!\n\n{e}")
                embed.color = discord.Colour.red()
                await ctx.respond(embed=embed, ephemeral=True)
        else:
            try:
                with open('data/help.csv', 'r') as thefile:
                    reader = csv.DictReader(thefile)
                    for row in reader:
                        if commandsys.lower() == row['command'].lower():
                            embed = discord.Embed(color=0x00b0f4, title=f"Help - {row['command']}", description=row['description'], image=row['screenshot'])
                            embed.add_field(name='Arguments', value=row['args'])
                            await ctx.respond(embed=embed)
                            return
                await ctx.respond('Command not found.')
            except Exception as e:
                embed = discord.Embed(title = "Error", description = f"Command broke!\n\n{e}")
                embed.color = discord.Colour.red()
                await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Help(bot))
