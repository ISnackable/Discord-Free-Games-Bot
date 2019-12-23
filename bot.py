import os

import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    activity = discord.Activity(name='DEVELOPING BOT', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    # channel = client.get_channel(431676381659791371)    
    # role.mention()
    # await channel.send(f'{channel.} test ping')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == '>>exit':
        print('stopping bot')
        exit()

client.run(token)