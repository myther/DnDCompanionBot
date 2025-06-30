import json
from datetime import datetime

class Adventure:
    """Class representing a D&D adventure."""
    
    def __init__(self, data):
        """
        Initialize an adventure from data.
        
        Args:
            data (dict): JSON data containing adventure information
        """
        self.id = data.get('id', None)
        self.name = data.get('name', '')
        self.description = data.get('description', '')
        self.level_range = data.get('level_range', [])
        self.players = data.get('players', [])
        self.npcs = data.get('npcs', [])
        self.monsters = data.get('monsters', [])
        self.locations = data.get('locations', [])
        self.encounters = data.get('encounters', [])
        self.items = data.get('items', [])
        self.created_at = data.get('created_at', datetime.now().isoformat())
        self.updated_at = data.get('updated_at', datetime.now().isoformat())
        self.status = data.get('status', 'draft')  # draft, active, completed
        
    def add_player(self, player_id):
        """Add a player to the adventure."""
        if player_id not in self.players:
            self.players.append(player_id)
            self.updated_at = datetime.now().isoformat()
            
    def remove_player(self, player_id):
        """Remove a player from the adventure."""
        if player_id in self.players:
            self.players.remove(player_id)
            self.updated_at = datetime.now().isoformat()
            
    def add_npc(self, npc_data):
        """Add an NPC to the adventure."""
        self.npcs.append(npc_data)
        self.updated_at = datetime.now().isoformat()
        
    def add_monster(self, monster_data):
        """Add a monster to the adventure."""
        self.monsters.append(monster_data)
        self.updated_at = datetime.now().isoformat()
        
    def add_location(self, location_data):
        """Add a location to the adventure."""
        self.locations.append(location_data)
        self.updated_at = datetime.now().isoformat()
        
    def add_encounter(self, encounter_data):
        """Add an encounter to the adventure."""
        self.encounters.append(encounter_data)
        self.updated_at = datetime.now().isoformat()
        
    def add_item(self, item_data):
        """Add an item to the adventure."""
        self.items.append(item_data)
        self.updated_at = datetime.now().isoformat()
        
    def to_json(self):
        """Convert adventure to JSON format."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'level_range': self.level_range,
            'players': self.players,
            'npcs': self.npcs,
            'monsters': self.monsters,
            'locations': self.locations,
            'encounters': self.encounters,
            'items': self.items,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'status': self.status
        }
        
    def __str__(self):
        """Get a formatted string representation of the adventure."""
        return f"""Adventure: {self.name}
Status: {self.status}
Level Range: {self.level_range}
Players: {len(self.players)}
NPCs: {len(self.npcs)}
Monsters: {len(self.monsters)}
Locations: {len(self.locations)}
Encounters: {len(self.encounters)}
Items: {len(self.items)}
Created: {self.created_at}
Updated: {self.updated_at}"""
