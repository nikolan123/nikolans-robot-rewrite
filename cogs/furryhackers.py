import discord
from discord.ext import commands

class SiegedSecCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="siegedsec_attacks",
        description="Summarizes notable attacks carried out by SiegedSec.",
        integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install}
    )
    async def siegedsec_attacks(self, ctx):
        attack_summaries = [
            {
                "title": "Atlassian",
                "description": (
                    "In February 2023, SiegedSec leaked data from Australian software provider Atlassian. "
                    "The hack exposed 13,000 employee records and office floorplans, achieved through stolen employee credentials."
                )
            },
            {
                "title": "#OpTransRights Movements",
                "description": (
                    "SiegedSec initiated #OpTransRights in June 2023, targeting US government entities to protest anti–gender-affirming-care bills. "
                    "In 2024, during #OpTransRights2, they leaked data from Real America's Voice and River Valley Church."
                )
            },
            {
                "title": "University of Connecticut",
                "description": (
                    "In July 2023, SiegedSec used email spoofing to send false death announcements to University of Connecticut students. "
                    "They exploited a vulnerability and later claimed responsibility, stating they did it 'for the lulz'."
                )
            },
            {
                "title": "NATO",
                "description": (
                    "In 2023, SiegedSec compromised NATO portals twice, leaking over 3000 internal documents. "
                    "Portals such as the Joint Advanced Distributed Learning and NATO Lessons Learned Portal were affected."
                )
            },
            {
                "title": "Bezeq",
                "description": (
                    "In October 2023, SiegedSec attacked Bezeq, one of Israel's largest telecommunication providers, leaking data on nearly 50,000 customers."
                )
            },
            {
                "title": "Idaho National Laboratory",
                "description": (
                    "In November 2023, SiegedSec breached Idaho National Laboratory's Oracle HR system, leaking employee data. "
                    "They demanded research into creating 'real-life catgirls' in exchange for removing the leaked data."
                )
            },
            {
                "title": "The Heritage Foundation",
                "description": (
                    "In July 2024, SiegedSec breached conservative think tank The Heritage Foundation. "
                    "The attack was in response to their Project 2025 proposals, which the group deemed authoritarian."
                )
            }
        ]
        embed = discord.Embed(title="Notable SiegedSec Attacks", colour=0x00b0f4)
        
        for attack in attack_summaries:
            embed.add_field(name=attack["title"], value=attack["description"], inline=False)
        try:
            await ctx.respond(embed=embed)
        except discord.HTTPException as e:
            await ctx.respond(f"An error occurred: {e}")
def setup(bot):
    bot.add_cog(SiegedSecCommands(bot))
