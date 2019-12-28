import os

import discord
from dotenv import load_dotenv
# import praw

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
# client_id = os.getenv('REDDIT_ID')
# client_secret = os.getenv('REDDIT_SECRET')
# user_agent = os.getenv('REDDIT_USER_AGENT')

client = discord.Client()
# reddit = praw.Reddit(client_id='my client id',
#                      client_secret='my client secret',
#                      user_agent='my user agent')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    activity = discord.Activity(name='DEVELOPING BOT', type=discord.ActivityType.playing)
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
        await message.channel.send('Stopping bot')
        exit()

# for submission in reddit.subreddit('Freegamestuff').stream.submissions():
#     if "free" in submission.title.lower:
#         print(submission)

client.run(token)