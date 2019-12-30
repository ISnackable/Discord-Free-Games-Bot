import os
import re
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

def process_link(link):
    url = re.search(r'(http|ftp|https)://([\w-]+(?:(?:.[\w-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', link)
    return url.group(0)


def process_title(title):
    p = re.compile(process_link(title))
    return p.sub('', title)
    

def retrieve_subreddit(): 
    for submission in reddit.subreddit('Freegamestuff').new(limit=1):
        game_title = process_title(submission.title)
        if submission.selftext != "":
            game_link = process_link(submission.selftext)
        else:
            game_link = process_link(submission.url)
    return game_title, game_link


async def check_history(title, link):
    channel = client.get_channel(431676381659791371) # Change 431676381659791371 to whatever channel's id you want
    previous_messages = []
    async for message in channel.history(limit=5, oldest_first=False):
            previous_messages.append(message.content)
    for messages in previous_messages:
        if title in messages or link in messages:
            print("Already posted")
            return True
        else:
            # embed=discord.Embed(title=title, url=link, description='Price:FREE (100% OFF) <:Steam:661129090191065120>')
            # embed.set_footer(text='Retrieved with FreeGamesBot by Ruii')
            # await channel.send(embed=embed)
            inital_message = await channel.send('Retrieving latest post from r/Freegamestuff')
            await inital_message.delete(delay=2)
            await channel.send('<@98797564966506496> ' + str(title) + "\n" + str(link)) # Change <@&431674916455055361> to whatever role's id you want
            return False


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    activity = discord.Activity(name='for free games!', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    client.loop.create_task(my_background_task())


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('uwuEasterEgg'):
        await message.delete()
        embed=discord.Embed(title=message.author.name, description='This person is so cool, :O')
        embed.set_footer(text='uwu')
        await message.channel.send(embed=embed)

    elif message.content.startswith('$screenshare'):
        if message.author.voice is not None:
            voice_channel = message.author.voice.channel.id
            await message.channel.send(f"https://www.discordapp.com/channels/{message.guild.id}/{voice_channel}")
        else:
            await message.channel.send(f"Please join a voice channel first")
            
    # if message.content.startswith('>>latest'): # command to retrieve latest free game
    #     await message.delete()
    #     game_title, game_link = retrieve_subreddit()
    #     author_id = message.author.id

    #     if await check_history(game_title, game_link):
    #         already_posted_message = await channel.send(f"<@{str(author_id)}> The game posted above is already the latest free game.")
    #         await already_posted_message.delete(delay=10)
    #     else:
    #         pass


async def my_background_task():
        while True:
            game_title, game_link = retrieve_subreddit()
            await check_history(game_title, game_link)

            await asyncio.sleep(1800) # task runs every 1800 seconds / 30 minutes

if __name__ == "__main__":
    client.run(token)