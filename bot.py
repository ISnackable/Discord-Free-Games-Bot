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
channels_to_update = {}
processed_submission = []

def check_owner(message):
    if message.author.guild_permissions >= message.guild.owner.guild_permissions:
        return True
    else:
        return False


def process_link(link):
    url = re.search(r'(http|ftp|https)://([\w-]+(?:(?:.[\w-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', link)
    
    if url is not None:
        return url.group(0)
    else:
        return ""


def process_title(title):
    p = re.compile(process_link(title)) # Remove link from title if there is any
    return p.sub('', title)
    

def retrieve_subreddit(): 
    for submission in reddit.subreddit('Freegamestuff').new(limit=1):
        submission_id = submission.id
        game_title = process_title(submission.title)
        if submission.selftext != "":
            game_link = process_link(submission.selftext)
        else:
            game_link = process_link(submission.url)
    return game_title, game_link, submission_id


async def check_history(title, link, submission_id):
    for channel in channels_to_update:
        if submission_id in processed_submission:
            # print("Already posted")
            break
        else:
            await post_freegame(channel, title, link)
    processed_submission.append(submission_id)


async def post_freegame(channel, title, link):
    if channels_to_update[channel] != None:
        await channel.send('<@&'+str(channels_to_update[channel])+'> ' + str(title) + "\n" + str(link))
    else:
        await channel.send(str(title) + "\n" + str(link))

    if len(processed_submission) >= 20:
        processed_submission.clear()


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
        embed=discord.Embed(title=message.author.name, description='Thiws pewson iws so coow, uwu.')
        embed.set_footer(text='uwu')
        await message.channel.send(embed=embed)

    elif message.content.startswith('$help'):
        embed=discord.Embed(title="Commands", description="List of commands", color=0x00ffff)
        embed.add_field(name="$screenshare", value="Share screen in a discord server", inline=False)
        embed.add_field(name="$activate", value="Activate channel to be notified about free games", inline=False)
        embed.add_field(name="$activate @role", value="Activate channel & role to be notified about free games", inline=False)
        embed.add_field(name="$deactivate", value="Deactivate channel from being notified about free games", inline=False)
        embed.set_footer(text="Bot made by Ruii")
        await message.channel.send(embed=embed)

    elif message.content.startswith('$screenshare'):
        if message.author.voice is not None:
            voice_channel = message.author.voice.channel.id
            await message.channel.send(f"https://www.discordapp.com/channels/{message.guild.id}/{voice_channel}")
        else:
            await message.channel.send(f"Please join a voice channel first")

    elif message.content.startswith('$activate'):
        if check_owner(message):
            if not message.channel in channels_to_update:
                if len(message.role_mentions) == 0:
                    channels_to_update[message.channel] = None
                    await message.channel.send('This channel will now be notified of new free games!')
                elif len(message.role_mentions) == 1: 
                    role_to_update = message.role_mentions[0].id
                    channels_to_update[message.channel] = role_to_update
                    await message.channel.send(f'This channel and @{message.role_mentions[0].name} will now be notified of new free games!')
                else:
                    await message.channel.send("You may only add 1 role to be mentioned, refer to the commands with '$help'.")
            else:
                await message.channel.send('This channel is already in the list to receive notifications.')
        else:
            await message.channel.send(f'Sorry <@{str(message.author.id)}>, you do not have permission to use $activate.')

    elif message.content.startswith('$deactivate'):
        if check_owner(message):
            if not message.channel in channels_to_update:
                await message.channel.send('This channel has not been activated for free games yet!')
            else:
                del channels_to_update[message.channel]
                await message.channel.send('This channel will now stop receiving notifications.')
        else:
            await message.channel.send(f'Sorry <@{str(message.author.id)}>, you do not have permission to use $deactivate.')

    elif message.content.startswith('$latest'): # Testing command
        await message.delete()
        if check_owner(message):
            game_title, game_link, submission_id = retrieve_subreddit()
            await check_history(game_title, game_link, submission_id)
        else:
            await message.channel.send(f'Sorry <@{str(message.author.id)}>, you do not have permission to use $deactivate.')


async def my_background_task():
        while True:
            if len(channels_to_update) != 0:
                game_title, game_link, submission_id = retrieve_subreddit()
                await check_history(game_title, game_link, submission_id)

            await asyncio.sleep(60) # task runs every 60 seconds

if __name__ == "__main__":
    client.run(token)