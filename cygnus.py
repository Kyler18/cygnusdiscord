import os
import discord
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

load_dotenv()  # take environment variables from .env.
API_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()  # or use discord.Intents.all() to receive all events
client = discord.Client(intents=intents)
guild = discord.Guild

# Specify the authors you want to log messages from
specified_authors = ['re1yk', '238605015474765825']

@client.event
async def on_message(message):
    message_content = message.content
    message_author = str(message.author)
    timestamp = str(datetime.utcnow())  # get the current time

    # Log messages from the specified authors or messages that mention the specified authors
    if any(author in message_content for author in specified_authors) or message_author in specified_authors:
        print(f'New message -> {message_author} said: {message_content} at {timestamp}')

        # Insert the new message into the Supabase database
        data = {
            'author': message_author,
            'content': message_content,
        }
        try:
            response = supabase.table('messages').insert(data).execute()
        except Exception as e:
            print(f'Error inserting message into database: {response.error}')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

if __name__ == "__main__":
    client.run(API_TOKEN)