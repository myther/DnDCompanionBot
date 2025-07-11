[![Build Status](https://travis-ci.com/satanas/DnDCompanionBot.svg?branch=master)](https://travis-ci.com/satanas/DnDCompanionBot)

# Dungeons and Dragons Companion Bot
`DnDCompanionBot` is a telegram bot to play Dungeons and Dragons. In the future, this bot should be able to track
campaigns, character sheets and help the DM with management tasks.

## Features

- Character management
  - Import characters from external sources
  - Track character stats, equipment, and spells
  - Manage character inventory
  - Track character experience and level progression
- Campaign control
  - Create and manage campaigns
  - Track campaign progress
  - Manage campaign NPCs and monsters
- Adventure management
  - Create and manage adventures
  - Import adventures from external sources
  - Track adventure progress
  - Manage adventure NPCs, monsters, and encounters
- Dice rolling
  - Roll dice for attacks, saving throws, and skill checks
- Battle tracking
  - Track initiative order
  - Manage combat encounters
  - Track damage and healing
- Character linking
  - Link characters to campaigns
  - Track character progress across campaigns
- Import functionality
  - Import characters from external sources
  - Import NPCs and monsters from external sources
  - Import adventures from external sources

## Commands
General commands | Action
--------|-------
/start | starts the DnDCompanionBot
/roll \<expression\> | rolls the dice using the [dice notation](https://en.wikipedia.org/wiki/Dice_notation)
/charsheet \<username\> | returns the character sheet associated with username
/help | shows this help message

Campaign commands | Action
--------|-------
/start_campaign | starts a new campaign in the invoked group
/close_campaign | closes an active campaign
/set_turns \<username1\>, ..., \<usernameN\> | creates a list with the order of players for a given round
/turn | shows the current player in the turns list
/next_turn | moves to the next player in the turns list
/set_dm \<username\> | sets the username of the DM for the current campaign
/dm | shows the DM for the current campaign
/start_battle \<width\>, \<height\> | generates a new battle field
/set_positions \<expression\> | set characters positions at the battle field
/map | set characters positions at the battle field

Character commands | Action
--------|-------
/import_char \<url\> | imports the JSON data of a character from a URL
/link_char \<char\_id\>, (username) | links character to target username or self username
/status \<username\|character\> | shows the list of weapons of a character
/weapons \<username\|character\> | shows the list of weapons of a character
/spells \<username\|character\> | shows the list of damage spells of a character
/currency \<username\|character\> | shows the currency pouch of a character
/damage \<username\|character\>, \<hp\> | apply damage to a character
/heal \<username\|character\>, \<hp\> | apply heal to a character
/attack_roll \<weapon\|spell\>, \<melee\|range\>, (distance), (adv\|disadv) | performs an attack roll on a character
/initiative_roll \<character\> | performs an initiative roll for a character
/short_rest_roll \<username\|character\> | performs an short rest roll for a character
/ability_check \<ability\>, (skill) | performs an ability check or a skill check if skill is specified
/say \<character\>, \<message\> | prints a message using in-game conversation format
/whisper \<character\>, \<message\> | prints a whisper message using in-game conversation format
/yell \<character\>, \<message\> | prints a yell message using in-game conversation format
/move \<character for dm\> | moves your character on the battle field
/set_currency \<username\|character\>, \<expression\> | set the currency pouch of a character
/add_xp \<username\|character\>, \<xp\> | adds points of experience to a character


## What do I need?
- A AWS key configured locally, see [here](https://serverless.com/framework/docs/providers/aws/guide/credentials/).
- NodeJS >= v8.9.0.
- A Telegram account.

## Installing
```
# Install the Serverless Framework
$ npm install serverless -g

# Install the necessary plugins
$ npm install

# Get a bot from Telegram, sending this message to @BotFather
$ /newbot

# Put the token received into a file called serverless.env.yml, along with your Firebase configuration details. Like this:
# file: serverless.env.yml
TELEGRAM_TOKEN: <your_token>
FIREBASE_DB_URL: <your_firebase_realtime_database_url>
FIREBASE_API_SECRET: <your_firebase_realtime_database_secret>

# Deploy it!
$ serverless deploy

# With the URL returned in the output, configure the Webhook
$ curl -X POST https://<your_url>.amazonaws.com/dev/set_webhook
```

## Installing locally

Define the following ENV variables for your OS:
```
TELEGRAM_TOKEN: <your_telegram_bot_token>
FIREBASE_DB_URL: <your_firebase_realtime_database_url>
FIREBASE_API_SECRET: <your_firebase_realtime_database_secret>
```

Then, make sure you use pip and all tools for Python 3 and install all dependencies:
```
$ pip3 install virtualenv
$ virtualenv venv
$ source venv/bin/activate

$ pip3 install -r requirements.txt
```

## Running the bot locally

Follow the instructions from the section [Installing locally](#installing-locally), and then run the bot:

```
$ python local.py
```

## Running tests locally

Follow the instructions from the section [Installing locally](#installing-locally), and then run the tests:

```
$ nose2 -v
```

## How to use the bot

### Import character from DndBeyond

1. Make sure your character is up-to-date in DnDBeyond.
2. Go to `https://www.dndbeyond.com/profile/{username}/characters/{character_id}/json` (replacing `{username}` with
your username and `character_id` with the ID of your character)
3. Copy the output JSON and paste it on a public location (Github Gist, Drive, Dropbox, etc)
4. Go to the Telegram chat where you're playing and execute `/link_char {json_url}` (where `{json_url} is the URL to
the public JSON you created in step 3).
5. Profit!

## Other notes
AWS credentials saved on your machine at ~/.aws/credentials.

## References
* https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/README.md
* https://github.com/treetrnk/rollem-telegram-bot/blob/master/bot.py
* https://rpg.stackexchange.com/questions/83930/how-do-i-calculate-my-skill-modifier
