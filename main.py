"""
This script sets up a Discord bot that periodically checks the ow2 countdown
RSS feed for new events and sends updates to a specified channel.
"""

import sqlite3
from datetime import datetime, timezone
import discord
import feedparser
from discord.ext import tasks

# YOU MUST SET THE DISCORD TOKEN AND CHANNEL ID FOR THIS TO WORK
# this guid will help you find your discord bot token: https://discordgsm.com/guide/how-to-get-a-discord-bot-token
# alternatively you can use this video: https://www.youtube.com/watch?v=mcsbmv7mZus
# this video will help you find your discord channel id: https://www.youtube.com/watch?v=NLWtSHWKbAI
DISCORD_TOKEN = "<YOUR DISCORD TOKEN>"
DISCORD_CHANNEL_ID = 00000000000000000000

if DISCORD_TOKEN == "<YOUR DISCORD TOKEN>" or DISCORD_CHANNEL_ID == 00000000000000000000:
    raise ValueError(
        "You must set the DISCORD_TOKEN and DISCORD_CHANNEL_ID variables in main.py line 16, 17 for this to work!"
    )

# Set up the database used to store events so the program won't send duplicate messages
conn = sqlite3.connect('events.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS events (
        guid TEXT PRIMARY KEY,
        title TEXT,
        description TEXT,
        link TEXT,
        eventDate TEXT,
        eventEndDate TEXT
    )'''
          )
conn.commit()

# Initialize the Discord bot
client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
    """
    Event handler for when the Discord bot is ready.
    """
    print(f'Logged in as {client.user}')
    check_events_periodically.start()


@tasks.loop(minutes=1)
async def check_events_periodically():
    """
    Function to check events periodically and send messages.
    """
    print('Checking for new events...')
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    new_events = fetch_new_events('https://ow2countdown.com/feed.xml')
    for event in new_events:
        embed = await embed_creator(event)
        await channel.send(embed=embed)


async def embed_creator(event):
    """
    Creates an embed message for the given event.

    Args:
        event: The event object.

    Returns:
        discord.Embed: The embed message.
    """
    embed = discord.Embed(
        title=event.title,
        description=event.description,
        url=event.link,
        color=0x00ff00,
    )
    embed.set_author(
        name="OW2 Countdown",
        url="https://ow2countdown.com",
        icon_url="https://github.com/CactusPuppy/ow2countdown/blob/main/static/og-image.png?raw=true"
    )
    embed.add_field(name=f"Starts <t:{event.eventdate}:R>",
                    value=f"<t:{event.eventdate}:f>", inline=True)
    embed.add_field(name=f"Ends <t:{event.eventenddate}:R>",
                    value=f"<t:{event.eventenddate}:f>", inline=True)
    return embed


def fetch_new_events(url):
    """
    Fetches new OW2 events from the provided RSS feed URL.

    Args:
        url (str): The URL of the RSS feed.

    Returns:
        list: A list of new events fetched from the RSS feed.
    """
    feed = feedparser.parse(url)
    new_events = []
    for entry in feed.entries:
        # converting to timestamp and fetching the description
        entry.eventdate = datetime_to_timestamp(entry.eventdate)
        entry.eventenddate = datetime_to_timestamp(entry.eventenddate)
        entry.description = entry.description.split(' | ')[2]
        # checking if the event already exists in the database
        c.execute("SELECT * FROM events WHERE guid = ?", (entry.guid,))
        if c.fetchone() is None:
            new_events.append(entry)
            c.execute(
                "INSERT INTO events (guid, title, description, link, eventDate, eventEndDate) VALUES (?, ?, ?, ?, ?, ?)",
                (entry.guid, entry.title, entry.description,
                 entry.link, entry.eventdate, entry.eventenddate)
            )
    conn.commit()
    return new_events


def datetime_to_timestamp(dt: str):
    """
    Converts a datetime string to a timestamp.

    Args:
        dt (str): The datetime string to convert.

    Returns:
        int: The timestamp value.
    """
    return int(datetime.strptime(dt, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc).timestamp())


# Run the bot
# Replace with your Discord bot token
client.run(DISCORD_TOKEN)
