# nikolan's robot rewrite
My Discord bot :3 it sucks

## Credits
### Current Version
- [**nikolan**](https://git.nikolan.xyz/nikolan) - Main bot developer
- [**tom1212.**](https://github.com/thepotatolover) - Helped take screenshots for the help command\n
- [**restartb**](https://github.com/restartb) - Helped improve and organise code, made config system, improved docs
  
### Old Version
- [**nikolan**](https://git.nikolan.xyz/nikolan) - Main bot developer
- [**tom1212.**](https://github.com/thepotatolover) - Contributor, helped with a lot of stuff
- [**giga**](https://github.com/fikinoob) - Former contributor, helped clean the code up
- [**nexus**](https://github.com/lhwe) - Helped find bugs and vulnerabilities in the bot

## Dependencies
The following dependencies are required to run the bot:\
`py-cord g4f requests aiohttp bing_image_urls discord_webhook py-cpuinfo curl_cffi sympy aiofiles`\
\
You can install these dependencies using **PIP** with the following command:\
`pip install py-cord g4f requests aiohttp bing_image_urls discord_webhook py-cpuinfo curl_cffi sympy aiofiles`

## Setup
If you would like to self host the bot, you can do so with the following steps:
> [!CAUTION]
> When generating Bot Tokens and API Secrets, do not share them with anybody!

### Config File Setup
1. Copy the `example-config.cfg`, and rename the copied version to `config.cfg`. This is your config file.
2. Enter the `config.cfg` file with a text editor, and change the values to fit you. We will generate a bot token in the next stage.

### Discord Bot Token
All Discord bots require a Discord Bot Token to function. The steps to get one are as follows:
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and log in with your Discord Account.
2. Create a new application and fill in the information required.
3. Go to the `Bot` section, and generate a new bot.
4. Give your bot a username, and optionally, a PFP and banner.
5. Copy the Bot Token. Go to the `config.cfg` file, and replace the value in `bot-token` with your bot token. Due to security reasons, you will only be able to view the bot token once from Discord Developer Portal before having to generate a new one.

### Starting the Bot
Once you have have installed the required Python modules, generated your token, and filled in your config file, you can run the bot as follows:
1. Navigate to the bot directory through the terminal.
2. Once you are in the bot directory, run `python main.py`, and monitor for any errors in the terminal.