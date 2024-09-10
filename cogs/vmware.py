import discord
from discord.ext import commands
import aiohttp
import re
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


class VMWareDL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    vmwaregroup = discord.SlashCommandGroup(name="vmware", integration_types={discord.IntegrationType.guild_install,discord.IntegrationType.user_install})

    class DownloadView(discord.ui.View):
        def __init__(self, seledition, dllinks):
            super().__init__()
            self.seledition = seledition
            self.dllinks = dllinks
            options = [
                discord.SelectOption(label=name)
                for name in self.dllinks.keys()
            ]

            select = discord.ui.Select(
                placeholder="Choose a version to download",
                min_values=1,
                max_values=1,
                options=options
            )
            
            select.callback = self.select_callback
            self.add_item(select)

        async def select_callback(self, interaction: discord.Interaction):
            await interaction.response.defer()
            selected_version = interaction.data['values'][0]
            
            dl_link = self.dllinks[selected_version]
            async with aiohttp.ClientSession() as session:
                async with session.get(dl_link) as response:
                    if response.status == 200:
                        the_content = await response.text() 
                        soup = BeautifulSoup(the_content, 'html.parser')
                        a_tag = soup.find('a', href=re.compile(r'vmware', re.IGNORECASE))
                        if a_tag:
                            dl_link = dl_link + a_tag.get('href')
            
            embed = discord.Embed(title="VMWare Download Assistant", color=discord.Color.blue(), description=f"The download link for {self.seledition} {selected_version} can be found below.")
            view = discord.ui.View()
            view.add_item(discord.ui.Button(label="Download", style=discord.ButtonStyle.url, url=dl_link))
            msg = await interaction.original_response()
            await msg.edit(embed=embed, view=view)
 
    class ListView(discord.ui.View):
        def __init__(self, editions):
            super().__init__()
            self.editions = editions
            options = [
                discord.SelectOption(label=name)
                for name in self.editions.keys()
            ]

            select = discord.ui.Select(
                placeholder="Choose an edition to download",
                min_values=1,
                max_values=1,
                options=options
            )
            
            select.callback = self.select_callback
            self.add_item(select)
            
        async def fetch_versions(self, url):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        xml_content = await response.text() 

                        version_url_dict = {}
                        root = ET.fromstring(xml_content)
                        
                        for metadata in root.findall('.//metadata'):
                            version_tag = metadata.find('version') 
                            url_tag = metadata.find('url')
                            
                            if version_tag is not None and url_tag is not None:
                                url_tag.text = 'https://softwareupdate.vmware.com/cds/vmw-desktop/' + url_tag.text.strip("metadata.xml.gz").replace('packages', 'core')
                                version_url_dict[url_tag.text.split('/')[6]] = url_tag.text
                        
                        return version_url_dict
        
        async def select_callback(self, interaction: discord.Interaction):
            await interaction.response.defer()
            def is_numeric_version(version):
                return all(part.isdigit() for part in version.split('.'))
            def version_key(version):
                return [int(part) for part in version.split('.')]
            selected_edition = interaction.data['values'][0]
            xml_link = self.editions[selected_edition]
            try:
                versions_available = await self.fetch_versions(xml_link)
                filtered_versions = {k: v for k, v in versions_available.items() if is_numeric_version(k)}
                sorted_versions = dict(sorted(filtered_versions.items(), key=lambda item: version_key(item[0]), reverse=True))
                if len(sorted_versions) > 25:
                    sorted_versions = dict(list(sorted_versions.items())[:25])
            except:
                return await interaction.response.send_message("An error occured :(")
            url_parts = next(iter(sorted_versions.items()))[1].split('/')
            embed = discord.Embed(title="VMWare Download Assistant", color=discord.Color.blue(), description=f"These are the latest 25 releases of {selected_edition}. For more versions, please visit [this page]({'/'.join(url_parts[:-5])}).")
            msg = await interaction.original_response()
            await msg.edit(embed=embed, view=VMWareDL.DownloadView(selected_edition, sorted_versions))

    @vmwaregroup.command(name="download", description="Gets download links for VMWare")
    async def vmwdl(self, ctx):
        editions = {
            "VMWare Fusion ARM64": "https://softwareupdate.vmware.com/cds/vmw-desktop/fusion-arm64.xml",
            "VMWare Fusion Universal": "https://softwareupdate.vmware.com/cds/vmw-desktop/fusion-universal.xml",
            "VMWare Fusion": "https://softwareupdate.vmware.com/cds/vmw-desktop/fusion.xml",
            "VMWare Workstation Player Linux": "https://softwareupdate.vmware.com/cds/vmw-desktop/player-linux.xml",
            "VMWare Workstation Player Windows": "https://softwareupdate.vmware.com/cds/vmw-desktop/player-windows.xml",
            "VMWare Workstation Pro Linux": "https://softwareupdate.vmware.com/cds/vmw-desktop/ws-linux.xml",
            "VMWare Workstation Pro Windows": "https://softwareupdate.vmware.com/cds/vmw-desktop/ws-windows.xml",
            "VMWare Remote Console Linux": "https://softwareupdate.vmware.com/cds/vmw-desktop/vmrc-linux.xml",
            "VMWare Remote Console macOS": "https://softwareupdate.vmware.com/cds/vmw-desktop/vmrc-macos.xml",
            "VMWare Remote Console Windows": "https://softwareupdate.vmware.com/cds/vmw-desktop/vmrc-windows.xml"
        }

        embed = discord.Embed(title="VMWare Download Assistant", color=discord.Color.blue(), description="Since Broadcom acquired VMWare, it has been really hard to get a download link for new VMWare versions. This commands pulls a download link for them directly from the Software Update Servers.")

        view = self.ListView(editions)
        await ctx.respond(embed=embed, view=view)
    
def setup(bot):
    bot.add_cog(VMWareDL(bot))
