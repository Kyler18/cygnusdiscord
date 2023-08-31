import os
import discord
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
API_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()  # or use discord.Intents.all() to receive all events
client = discord.Client(intents=intents)
guild = discord.Guild

# Specify the authors you want to log messages from
specified_authors = ['238605015474765825']

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('messages.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (timestamp text, author text, content text)''')

@client.event
async def on_message(message):
    message_content = message.content
    message_author = str(message.author)
    timestamp = str(datetime.utcnow())  # get the current time

    # Log messages from the specified authors or messages that mention the specified authors
    if any(author in message_content for author in specified_authors) or message_author in specified_authors:
        print(f'New message -> {message_author} said: {message_content} at {timestamp}')
        
        # Insert the message into the SQLite database
        c.execute("INSERT INTO messages VALUES (?,?,?)", (timestamp, message_author, message_content))
        conn.commit()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

if __name__ == "__main__":
    client.run(API_TOKEN)