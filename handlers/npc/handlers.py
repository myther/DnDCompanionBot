from database import Database
from models.npc import NPC
from decorators import only_dm, get_campaign
from exceptions import CampaignNotFound

def handler(bot, update, command, txt_args, username, chat_id, db):
    """Handle NPC-related commands."""
    if command == '/create_npc':
        response = create_npc(txt_args, db, chat_id)
    elif command == '/list_npcs':
        response = list_npcs(db, chat_id)
    elif command == '/view_npc':
        response = view_npc(txt_args, db, chat_id)
    elif command == '/update_npc':
        response = update_npc(txt_args, db, chat_id)
    elif command == '/delete_npc':
        response = delete_npc(txt_args, db, chat_id)
    
    return response

def create_npc(txt_args, db, chat_id):
    """Create a new NPC."""
    if not txt_args:
        return "Usage: /create_npc <name> <race> <class>"
    
    name, race, npc_class = txt_args[:3]
    
    npc_data = {
        'name': name,
        'race': race,
        'class': npc_class,
        'level': 1,
        'str': 10,
        'dex': 10,
        'con': 10,
        'int': 10,
        'wis': 10,
        'cha': 10,
        'alignment': 'Neutral',
        'background': '',
        'occupation': '',
        'personality_traits': [],
        'ideal': '',
        'bond': '',
        'flaw': ''
    }
    
    npc = NPC(npc_data)
    db.add_npc(chat_id, npc)
    
    return f"NPC '{npc.name}' created successfully!"

def list_npcs(db, chat_id):
    """List all NPCs in the current campaign."""
    npcs = db.get_npcs(chat_id)
    if not npcs:
        return "No NPCs found in this campaign."
    
    response = "NPCs in this campaign:\n"
    for npc in npcs:
        response += f"\n• {npc.name} (Level {npc.level}, {npc.race} {npc._class})"
    
    return response

def view_npc(txt_args, db, chat_id):
    """View detailed information about an NPC."""
    if not txt_args:
        return "Usage: /view_npc <name>"
    
    name = txt_args[0]
    npc = db.get_npc_by_name(chat_id, name)
    
    if not npc:
        return f"NPC '{name}' not found in this campaign."
    
    return str(npc)

def update_npc(txt_args, db, chat_id):
    """Update NPC attributes."""
    if len(txt_args) < 3:
        return "Usage: /update_npc <name> <attribute> <value>"
    
    name, attribute, value = txt_args[:3]
    npc = db.get_npc_by_name(chat_id, name)
    
    if not npc:
        return f"NPC '{name}' not found in this campaign."
    
    try:
        setattr(npc, attribute, value)
        db.update_npc(chat_id, npc)
        return f"NPC '{name}' updated successfully!"
    except AttributeError:
        return f"Invalid attribute '{attribute}' for NPC."

def delete_npc(txt_args, db, chat_id):
    """Delete an NPC from the campaign."""
    if not txt_args:
        return "Usage: /delete_npc <name>"
    
    name = txt_args[0]
    npc = db.get_npc_by_name(chat_id, name)
    
    if not npc:
        return f"NPC '{name}' not found in this campaign."
    
    db.delete_npc(chat_id, npc)
    return f"NPC '{name}' deleted successfully!"
