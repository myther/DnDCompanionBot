from database import Database
from models.monster import Monster
from decorators import only_dm, get_campaign
from exceptions import CampaignNotFound

def handler(bot, update, command, txt_args, username, chat_id, db):
    """Handle monster-related commands."""
    if command == '/create_monster':
        response = create_monster(txt_args, db, chat_id)
    elif command == '/list_monsters':
        response = list_monsters(db, chat_id)
    elif command == '/view_monster':
        response = view_monster(txt_args, db, chat_id)
    elif command == '/update_monster':
        response = update_monster(txt_args, db, chat_id)
    elif command == '/delete_monster':
        response = delete_monster(txt_args, db, chat_id)
    elif command == '/import_monster':
        response = import_monster(txt_args, db, chat_id)
    
    return response

def create_monster(txt_args, db, chat_id):
    """Create a new monster."""
    if len(txt_args) < 3:
        return "Usage: /create_monster <name> <type> <challenge_rating>"
    
    name, monster_type, cr = txt_args[:3]
    cr = float(cr)
    
    monster_data = {
        'name': name,
        'type': monster_type,
        'challenge_rating': cr,
        'size': 'Medium',
        'alignment': 'Neutral',
        'str': 10,
        'dex': 10,
        'con': 10,
        'int': 10,
        'wis': 10,
        'cha': 10,
        'armor_class': 10,
        'max_hit_points': 10,
        'speed': 30,
        'languages': [],
        'senses': {},
        'damage_resistances': [],
        'damage_immunities': [],

@decorators.only_dm
@decorators.get_campaign
async def list_monsters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all monsters in the campaign."""
    monsters = database.get_monsters(context.campaign_id)
    if not monsters:
        await update.message.reply_text("No monsters found in this campaign.")
        return
    
    monster_list = "\n".join([f"{monster['name']} - {monster['type']} CR {monster['challenge_rating']} HP {monster['hp']}" 
                             for monster in monsters])
    await update.message.reply_text(f"Monsters in campaign:\n{monster_list}")

@decorators.only_dm
@decorators.get_campaign
async def update_monster(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Update an existing monster."""
    args = context.args
    if not args or len(args) < 4:
        await update.message.reply_text("Usage: /update_monster <name> <type> <challenge_rating> <hp>")
        return
    
    try:
        name = args[0]
        monster_type = args[1]
        challenge_rating = float(args[2])
        hp = int(args[3])
        
        monster = Monster(name, monster_type, challenge_rating, hp)
        database.update_monster(context.campaign_id, monster)
        await update.message.reply_text(f"Monster {name} updated successfully!")
    except (IndexError, ValueError):
        await update.message.reply_text("Invalid arguments. Usage: /update_monster <name> <type> <challenge_rating> <hp>")

@decorators.only_dm
@decorators.get_campaign
async def delete_monster(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a monster."""
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /delete_monster <name>")
        return
    
    name = args[0]
    monster = database.get_monster_by_name(context.campaign_id, name)
    if not monster:
        await update.message.reply_text(f"Monster {name} not found.")
        return
    
    database.delete_monster(context.campaign_id, monster)
    await update.message.reply_text(f"Monster {name} deleted successfully!")

@decorators.only_dm
async def import_monster(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Import a monster from an external source."""
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /import_monster <url>")
        return
    
    try:
        # TODO: Implement monster import logic
        await update.message.reply_text("Monster import feature coming soon!")
    except Exception as e:
        await update.message.reply_text(f"Error importing monster: {str(e)}")
