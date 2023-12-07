# Overwatch 2 Countdown Bot

This script sets up a Discord bot that periodically checks the ow2 countdown RSS feed for new events and sends updates to a specified channel.

## Credits

- CactusPuppy for creating the ow2countdown website. This project wouldn't be possible without his project. You can find the project on [GitHub](https://github.com/CactusPuppy/ow2countdown) and the website at [ow2countdown.com](https://ow2countdown.com).

## Prerequisites

- Python 3.6 or higher
- Discord bot token
- Discord channel ID

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/overjump1/OW2-Countdown-discord-bot.git
   ```

2. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

3. Set up the Discord bot:

   - Obtain a Discord bot token by following this guide: [How to Get a Discord Bot Token](https://discordgsm.com/guide/how-to-get-a-discord-bot-token)
   - Find your Discord channel ID by following this video: [How to Find Your Discord Channel ID](https://www.youtube.com/watch?v=NLWtSHWKbAI)

4. Update the `DISCORD_TOKEN` and `DISCORD_CHANNEL_ID` variables in `main.py` with your Discord bot token and channel ID.

## Usage

Run the bot using the following command:

python main.py

its recommanded to run it in docker for best results
