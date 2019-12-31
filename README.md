# Discord Free Games Bot
A bot that will retrieve the latest post from subreddit r/Freegamestuff and post on the assigned discord text channel

By [ISnackable](https://github.com/ISnackable)

## Dependencies
The following tools should be installed before starting:
* [Python](https://www.python.org/)
* [Discord](https://discordapp.com/developers/docs/intro)
* [Dotenv](https://pypi.org/project/python-dotenv/#installation)
* [Praw](https://praw.readthedocs.io/en/latest/getting_started/installation.html)

## How to setup this project

1. Make sure you have all of the dependencies installed
2. Clone this repo using `git clone https://github.com/ISnackable/Discord-Free-Games-Bot.git`
3. Navigate into the directory `cd Discord-Free-Games-Bot`
4. Install the dependencies
```
pip install -U discord.py
pip install -U python-dotenv
pip install praw
```
5. Create file `.env` and insert your tokens like the text shown below
```
DISCORD_TOKEN=<REPLACE WITH DISCORD DEVELOPER TOKEN> 
REDDIT_ID=<REPLACE WITH REDDIT API ID>
REDDIT_SECRET=<REPLACE WITH REDDIT API SECRET TOKEN>
REDDIT_USER_AGENT=<REPLACE WITH REDDIT API NAME>

// Eg. DISCORD_TOKEN=ASIDUHIAUWBDUI1I3123AD
```
7. That's all, thanks for checking out my bot