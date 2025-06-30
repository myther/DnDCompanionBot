from database import Database
from models.adventure import Adventure
from decorators import only_dm, get_campaign
from exceptions import CampaignNotFound
from services.external_sources import ExternalSources

external_sources = ExternalSources()

def handler(bot, update, command, txt_args, username, chat_id, db):
    """Handle adventure-related commands."""
    if command == '/create_adventure':
        response = create_adventure(txt_args, db, chat_id)
    elif command == '/list_adventures':
        response = list_adventures(db, chat_id)
    elif command == '/view_adventure':
        response = view_adventure(txt_args, db, chat_id)
    elif command == '/update_adventure':
        response = update_adventure(txt_args, db, chat_id)
    elif command == '/delete_adventure':
        response = delete_adventure(txt_args, db, chat_id)
    elif command == '/import_adventure':
        response = import_adventure(txt_args, db, chat_id)
    elif command == '/start_adventure':
        response = start_adventure(txt_args, db, chat_id)
    elif command == '/end_adventure':
        response = end_adventure(txt_args, db, chat_id)
    
    return response

def create_adventure(txt_args, db, chat_id):
    """Create a new adventure."""
    if not txt_args:
        return "Usage: /create_adventure <name> <description> <level_range>"
    
    name = txt_args[0]
    description = txt_args[1]
    level_range = list(map(int, txt_args[2].split('-'))) if '-' in txt_args[2] else [int(txt_args[2]), int(txt_args[2])]
    
    adventure_data = {
        'name': name,
        'description': description,
        'level_range': level_range,
        'status': 'draft'
    }
    
    adventure = Adventure(adventure_data)
    db.add_adventure(chat_id, adventure)
    
    return f"Adventure '{adventure.name}' created successfully!"

def list_adventures(db, chat_id):
    """List all adventures in the campaign."""
    adventures = db.get_adventures(chat_id)
    if not adventures:
        return "No adventures found in this campaign."
    
    response = "Adventures in this campaign:\n"
    for adventure in adventures:
        response += f"\n• {adventure.name} (Level {adventure.level_range[0]}-{adventure.level_range[1]})"
    
    return response

def view_adventure(txt_args, db, chat_id):
    """View detailed information about an adventure."""
    if not txt_args:
        return "Usage: /view_adventure <name>"
    
    name = txt_args[0]
    adventure = db.get_adventure_by_name(chat_id, name)
    
    if not adventure:
        return f"Adventure '{name}' not found in this campaign."
    
    return str(adventure)

def update_adventure(txt_args, db, chat_id):
    """Update adventure attributes."""
    if len(txt_args) < 3:
        return "Usage: /update_adventure <name> <attribute> <value>"
    
    name, attribute, value = txt_args[:3]
    adventure = db.get_adventure_by_name(chat_id, name)
    
    if not adventure:
        return f"Adventure '{name}' not found in this campaign."
    
    try:
        setattr(adventure, attribute, value)
        db.update_adventure(chat_id, adventure)
        return f"Adventure '{name}' updated successfully!"
    except AttributeError:
        return f"Invalid attribute '{attribute}' for adventure."

def delete_adventure(txt_args, db, chat_id):
    """Delete an adventure from the campaign."""
    if not txt_args:
        return "Usage: /delete_adventure <name>"
    
    name = txt_args[0]
    adventure = db.get_adventure_by_name(chat_id, name)
    
    if not adventure:
        return f"Adventure '{name}' not found in this campaign."
    
    db.delete_adventure(chat_id, adventure)
    return f"Adventure '{name}' deleted successfully!"

def import_adventure(txt_args, db, chat_id):
    """Import an adventure from external source."""
    if not txt_args:
        return "Usage: /import_adventure <url>"
    
    url = txt_args[0]
    # TODO: Implement actual import logic
    return "Adventure import functionality will be implemented soon."

def start_adventure(txt_args, db, chat_id):
    """Start an adventure."""
    if not txt_args:
        return "Usage: /start_adventure <name>"
    
    name = txt_args[0]
    adventure = db.get_adventure_by_name(chat_id, name)
    
    if not adventure:
        return f"Adventure '{name}' not found in this campaign."
    
    adventure.status = 'active'
    db.update_adventure(chat_id, adventure)
    return f"Adventure '{name}' started successfully!"

def end_adventure(txt_args, db, chat_id):
    """End an adventure."""
    if not txt_args:
        return "Usage: /end_adventure <name>"
    
    name = txt_args[0]
    adventure = db.get_adventure_by_name(chat_id, name)
    
    if not adventure:
        return f"Adventure '{name}' not found in this campaign."
    
    adventure.status = 'completed'
    db.update_adventure(chat_id, adventure)
    return f"Adventure '{name}' ended successfully!"
