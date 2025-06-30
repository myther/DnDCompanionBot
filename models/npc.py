import math

from models.character import Character
from models.armor import Armor
from models.weapon import Weapon
from models.spell import Spell

class NPC(Character):
    """Class representing a Non-Player Character."""
    
    def __init__(self, json_data):
        """
        Initialize an NPC from JSON data.
        
        Args:
            json_data (dict): JSON data containing NPC information
        """
        # Initialize base character attributes
        super().__init__(json_data, {}, True)
        
        # NPC-specific attributes
        self.alignment = json_data.get('alignment', 'Neutral')
        self.personality_traits = json_data.get('personality_traits', [])
        self.ideal = json_data.get('ideal', '')
        self.bond = json_data.get('bond', '')
        self.flaw = json_data.get('flaw', '')
        self.background = json_data.get('background', '')
        self.occupation = json_data.get('occupation', '')
        
        # NPC-specific modifiers
        self.charisma_mod = math.floor((self.cha - 10) / 2)
        self.intelligence_mod = math.floor((self.int - 10) / 2)
        
    def get_description(self):
        """Get a formatted description of the NPC."""
        return f"""{self.name}
Level: {self.level}
Race: {self.race}
Class: {self._class}
Alignment: {self.alignment}
Background: {self.background}
Occupation: {self.occupation}

Personality Traits:
{self.personality_traits}

Ideal: {self.ideal}
Bond: {self.bond}
Flaw: {self.flaw}

Abilities:
STR: {self.str} ({self.str_mod:+})
DEX: {self.dex} ({self.dex_mod:+})
CON: {self.con} ({self.con_mod:+})
INT: {self.int} ({self.int_mod:+})
WIS: {self.wis} ({self.wis_mod:+})
CHA: {self.cha} ({self.cha_mod:+})"""

    def __str__(self):
        return self.get_description()
