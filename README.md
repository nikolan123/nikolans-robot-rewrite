# nikolan's robot rewrite
Steam API, Spotify API, FBI wanted list, sand cats, Windows product keys, animals, random CPUs and GPUs, Bing image search, AI, 8ball, Minecraft skin and version lookup and more!

## Setup
If you would like to self host the bot, you can do so with the following steps:
> [!CAUTION]
> When generating Bot Tokens and API Secrets, do not share them with anybody!

### Config File Setup
1. Copy the `example-config.cfg` file, and rename the copied version to `config.cfg`. This is your config file.
2. Enter the `config.cfg` file with a text editor, and change the values to fit you. We will generate a bot token in the next stage.

### Discord Bot Token
All Discord bots require a Discord Bot Token to function. The steps to get one are as follows:
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and log in with your Discord Account.
2. Create a new application and fill in the information required.
3. Go to the `Bot` section, and generate a new bot.
4. Give your bot a username, and optionally, a PFP and banner.
5. Copy the Bot Token. Go to the `config.cfg` file, and replace the value in `bot-token` with your bot token. Due to security reasons, you will only be able to view the bot token once from Discord Developer Portal before having to generate a new one.

### Dependencies
The following dependencies are required to run the bot:\
`py-cord, g4f, aiohttp, bing_image_urls, discord_webhook, py-cpuinfo, curl_cffi, sympy, aiofiles`.\
\
You can install these dependencies using **PIP** with the following command:\
`pip install py-cord g4f aiohttp bing_image_urls discord_webhook py-cpuinfo curl_cffi sympy aiofiles`

### Starting the Bot
Once you have have installed the required Python modules, generated your token, and filled in your config file, you can run the bot as follows:
1. Navigate to the bot directory through the terminal.
2. Once you are in the bot directory, run `python main.py`, and monitor for any errors in the terminal.

## Credits
- [**nikolan**](https://nikolan.net) - Main bot developer
- [**restartb**](https://github.com/restartb) - Helped improve and organise code, made config system, improved docs
- [**tom1212.**](https://github.com/thepotatolover) - Helped take screenshots for the help command and more
- [**mat**](https://github.com/mat-1) - Sand cat images


# This project is licensed under [AGPLv3](/LICENSE)
