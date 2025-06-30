import math

from models.character import Character
from models.armor import Armor
from models.weapon import Weapon
from models.spell import Spell

class Monster(Character):
    """Class representing a monster in the game."""
    
    def __init__(self, json_data):
        """
        Initialize a monster from JSON data.
        
        Args:
            json_data (dict): JSON data containing monster information
        """
        # Initialize base character attributes
        super().__init__(json_data, {}, True)
        
        # Monster-specific attributes
        self.challenge_rating = json_data.get('challenge_rating', 0)
        self.size = json_data.get('size', 'Medium')
        self.type = json_data.get('type', 'Humanoid')
        self.alignment = json_data.get('alignment', 'Neutral')
        self.languages = json_data.get('languages', [])
        self.senses = json_data.get('senses', {})
        self.special_abilities = json_data.get('special_abilities', [])
        self.legendary_actions = json_data.get('legendary_actions', [])
        self.legendary_resistance = json_data.get('legendary_resistance', 0)
        self.damage_resistances = json_data.get('damage_resistances', [])
        self.damage_immunities = json_data.get('damage_immunities', [])
        self.condition_immunities = json_data.get('condition_immunities', [])
        
        # Monster-specific modifiers
        self.armor_class = json_data.get('armor_class', 10 + self.dex_mod)
        
    def get_description(self):
        """Get a formatted description of the monster."""
        return f"""{self.name}
Size: {self.size}
Type: {self.type}
Challenge Rating: {self.challenge_rating}
Alignment: {self.alignment}

Abilities:
STR: {self.str} ({self.str_mod:+})
DEX: {self.dex} ({self.dex_mod:+})
CON: {self.con} ({self.con_mod:+})
INT: {self.int} ({self.int_mod:+})
WIS: {self.wis} ({self.wis_mod:+})
CHA: {self.cha} ({self.cha_mod:+})

Armor Class: {self.armor_class}
Hit Points: {self.max_hit_points}

Special Abilities:
{self._format_list(self.special_abilities)}

Legendary Actions:
{self._format_list(self.legendary_actions)}

Damage Resistances:
{self._format_list(self.damage_resistances)}

Damage Immunities:
{self._format_list(self.damage_immunities)}

Condition Immunities:
{self._format_list(self.condition_immunities)}"""

    def _format_list(self, items):
        """Format a list of items into a readable string."""
        if not items:
            return "None"
        return "\n".join(f"- {item}" for item in items)

    def __str__(self):
        return self.get_description()
