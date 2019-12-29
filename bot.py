import os
import discord
from dotenv import load_dotenv
import praw
import asyncio

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client_id = os.getenv('REDDIT_ID')
client_secret = os.getenv('REDDIT_SECRET')
user_agent = os.getenv('REDDIT_USER_AGENT')

client = discord.Client()
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    activity = discord.Activity(name='for free games!', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    client.loop.create_task(my_background_task())


@client.event
async def on_message(message):
    channel = client.get_channel(431676381659791371)
    if message.author == client.user:
        return
    
    if message.content == '>>latest':
        title, url = retrieve_subreddit()
        previous_messages = []
        author_id = message.author.id
        await message.delete()

        async for message in channel.history(limit=100):
            previous_messages.append(message.content)

        if title in ''.join([str(messages) for messages in previous_messages ]):
            await channel.send(f"<@{str(author_id)}> There is no free games today :(")
        else:
            inital_message = await channel.send('Retrieving latest post from r/Freegamestuff')
            await inital_message.delete(delay=2)
            await channel.send('<@&431674916455055361> ' + str(title) + "\n" + str(url))
        

def retrieve_subreddit(): 
    for submission in reddit.subreddit('Freegamestuff').hot(limit=5):
        if 'free' in submission.title.lower():
            return submission.title, submission.shortlink

async def my_background_task():
        channel = client.get_channel(431676381659791371)
        while True:
            title, url = retrieve_subreddit()
            previous_messages = []
            async for message in channel.history(limit=100):
                previous_messages.append(message.content)

            if title in ''.join([str(messages) for messages in previous_messages ]):
                pass
            else:
                await channel.send('<@&431674916455055361> ' + str(title) + "\n" + str(url))

            await asyncio.sleep(43200) # task runs every 43200 seconds / 12 hours

if __name__ == "__main__":
    client.run(token)