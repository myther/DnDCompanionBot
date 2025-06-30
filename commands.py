from exceptions import CommandNotFound, NotACommand
from handlers.roll import handler as roll_handler
from handlers.charsheet import handler as charsheet_handler
from handlers.character import handler as character_handler
from handlers.turns import handler as turn_handler
from handlers.dm import handler as dm_handler
from handlers.campaign import handler as campaign_handler
from handlers.npc.handlers import handler as npc_handler
from handlers.monster.handlers import handler as monster_handler
from handlers.adventure.handlers import handler as adventure_handler

# Each command should be defined using the expression below:
#
# "/cmd": (handler, args, description)
#
# where:
#   cmd: the command string
#   handler: is the method that will handle the action requested with the command
#   args: is an array of arguments the command need. Args wrapped between `<>` are mandatory and wrapped
#         between `()` are optional. Can be None if no arguments are required.
#   description: the text that will describe the command

GENERAL_COMMANDS = {
    "/start": (None, None, "starts the DnDCompanionBot"),
    "/roll": (roll_handler, ["<expression>"], "rolls the dice using the [dice notation](https://en.wikipedia.org/wiki/Dice_notation)"),
    "/charsheet": (charsheet_handler, ["<username>"], "returns the character sheet associated with username"),
    "/help": (None, None, "shows this help message"),
    "/create_npc": (npc_handler, ["<name>", "<race>", "<class>"], "creates a new NPC character"),
    "/list_npcs": (npc_handler, None, "lists all NPCs in the current campaign"),
    "/view_npc": (npc_handler, ["<name>"], "view detailed information about an NPC"),
    "/update_npc": (npc_handler, ["<name>", "<attribute>", "<value>"], "update NPC attributes"),
    "/delete_npc": (npc_handler, ["<name>"], "delete an NPC from the campaign"),
    "/create_monster": (monster_handler, ["<name>", "<type>", "<challenge_rating>"], "creates a new monster"),
    "/list_monsters": (monster_handler, None, "lists all monsters in the current campaign"),
    "/view_monster": (monster_handler, ["<name>"], "view detailed information about a monster"),
    "/update_monster": (monster_handler, ["<name>", "<attribute>", "<value>"], "update monster attributes"),
    "/delete_monster": (monster_handler, ["<name>"], "delete a monster from the campaign"),
    "/import_monster": (monster_handler, ["<url>"], "import a monster from external source"),
    "/create_adventure": (adventure_handler, ["<name>", "<description>", "<level_range>"], "creates a new adventure with the specified name, description, and level range"),
    "/list_adventures": (adventure_handler, None, "lists all adventures in the current campaign with their names and level ranges"),
    "/view_adventure": (adventure_handler, ["<name>"], "view detailed information about an adventure including NPCs, monsters, and encounters"),
    "/update_adventure": (adventure_handler, ["<name>", "<attribute>", "<value>"], "update adventure attributes such as description, level range, or status"),
    "/delete_adventure": (adventure_handler, ["<name>"], "delete an adventure from the campaign"),
    "/import_adventure": (adventure_handler, ["<url>"], "import an adventure from an external source, supports D&D 5e API"),
    "/start_adventure": (adventure_handler, ["<name>"], "mark an adventure as started, allowing tracking of progress"),
    "/end_adventure": (adventure_handler, ["<name>"], "mark an adventure as completed and finalize its status")
}

CAMPAIGN_COMMANDS = {
    "/start_campaign": (campaign_handler, None, "starts a new campaign in the invoked group"),
    "/close_campaign": (campaign_handler, None, "closes an active campaign"),
    "/set_turns": (turn_handler, ["<username1>", "...", "<usernameN>"], "creates a list with the order of players for a given round"),
    "/turn": (turn_handler, None, "shows the current player in the turns list"),
    "/next_turn": (turn_handler,  None, "moves to the next player in the turns list"),
    "/set_dm": (dm_handler, ["<username>"], "sets the username of the DM for the current campaign"),
    "/dm": (dm_handler, None, "shows the DM for the current campaign"),
    "/start_battle": (campaign_handler, ["<width>", "<height>"], "generates a new battle field"),
    "/set_positions": (campaign_handler, ["<expression>"], "set characters positions at the battle field"),
    "/map": (campaign_handler, None, "set characters positions at the battle field"),
}

CHARACTER_COMMANDS = {
    "/import_char": (character_handler, ["<url>"], "imports the JSON data of a character from a URL"),
    "/link_char": (character_handler, ["<char_id>", "(username)"], "links character to target username or self username"),
    "/status": (character_handler, ["<username|character>"], "shows the status of a character"),
    "/weapons": (character_handler, ["<username|character>"], "shows the list of weapons of a character"),
    "/spells": (character_handler, ["<username|character>"], "shows the list of damage spells of a character"),
    "/currency": (character_handler, ["<username|character>"], "shows the currency pouch of a character"),
    "/damage": (character_handler, ["<username|character>", "<hp>"], "apply damage to a character"),
    "/heal": (character_handler, ["<username|character>", "<hp>"], "apply heal to a character"),
    "/attack_roll": (character_handler, ["<weapon|spell>", "<melee|range>", "(distance)", "(adv|disadv)"], "performs an attack roll on a character"),
    "/initiative_roll": (character_handler, ["<character>"], "performs an initiative roll for a character"),
    "/short_rest_roll": (character_handler, ["<username|character>"], "performs an short rest roll for a character"),
    "/ability_check": (character_handler, ["<ability>", "(skill)"], "performs an ability check or a skill check if skill is specified"),
    "/say": (character_handler, ["<character>", "<message>"], "prints a message using in-game conversation format"),
    "/whisper": (character_handler, ["<character>", "<message>"], "prints a whisper message using in-game conversation format"),
    "/yell": (character_handler, ["<character>", "<message>"], "prints a yell message using in-game conversation format"),
    "/move": (character_handler, ["<character for dm>"], "moves your character on the battle field"),
    "/set_currency": (character_handler, ["<username|character>", "<expression>"], "set the currency pouch of a character"),
    "/add_xp": (dm_handler, ["<username|character>", "<xp>"], "adds points of experience to a character"),
}

ALL_COMMANDS = {}
ALL_COMMANDS.update(GENERAL_COMMANDS)
ALL_COMMANDS.update(CAMPAIGN_COMMANDS)
ALL_COMMANDS.update(CHARACTER_COMMANDS)

def command_handler(command):
    if command == "/help" or command == '/start':
        raise CommandNotFound
    #    return default_handler
    #elif command == "/start":
    elif command in ALL_COMMANDS:
        return ALL_COMMANDS[command][0]
    else:
        raise CommandNotFound

def default_handler(bot, update, message):
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode="Markdown", disable_web_page_preview=True)

def is_command(update):
    if update.message is None:
        return False

    return update.message.text is not None and update.message.text != '' \
            and update.message.text.startswith('/')

def parse_command(txt_message):
    cmd = txt_message.split(' ')[0]
    if cmd.find('@') >= 0:
        cmd = cmd.split('@')[0]
    return cmd
