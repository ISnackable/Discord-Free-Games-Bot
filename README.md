# Discord Free Games Bot
A bot that will retrieve the latest post from reddit r/Freegamestuff and post on discord

By [ISnackable](https://github.com/ISnackable)

## Dependencies
The following tools should be installed before starting:
* Python
* Discord
* Praw

## How to setup this project

1. Make sure you have all of the dependencies installed
2. Clone this repo using `https://github.com/ISnackable/Discord-Free-Games-Bot.git`
3. Navigate into the directory `cd Discord-Free-Games-Bot`
4. Create file `.env` and insert your tokens like shown below
```
DISCORD_TOKEN=<REPLACE WITH DISCORD DEVELOPER TOKEN>
REDDIT_ID=<REPLACE WITH REDDIT API ID>
REDDIT_SECRET=<REPLACE WITH REDDIT API SECRET TOKEN>
REDDIT_USER_AGENT=<REPLACE WITH REDDIT API NAME>
```
5. Edit bot.py and replace line 29, 47, 56 & 66 to an appropriate discord channel/role ID 
6. That's all, thanks for checking out my bot