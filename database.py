import os
import json
import requests

from models.campaign import Campaign
from models.character import Character

from firebase import firebase
from firebase.jsonutil import JSONEncoder

FIREBASE_DB_URL = os.environ.get('FIREBASE_DB_URL')
FIREBASE_API_SECRET = os.environ.get('FIREBASE_API_SECRET')

RACE_URLS = {
    "Dwarf": "http://www.dnd5eapi.co/api/races/1",
    "Elf": "http://www.dnd5eapi.co/api/races/2",
    "Halfling": "http://www.dnd5eapi.co/api/races/3",
    "Human": "http://www.dnd5eapi.co/api/races/4",
    "Dragonborn": "http://www.dnd5eapi.co/api/races/5",
    "Gnome": "http://www.dnd5eapi.co/api/races/6",
    "Half-Elf": "http://www.dnd5eapi.co/api/races/7",
    "Half-Orc": "http://www.dnd5eapi.co/api/races/8",
    "Tiefling": "http://www.dnd5eapi.co/api/races/9"
}

class Database:
    def __init__(self):
        """Initialize Firebase database connection."""
        self.firebase_db = firebase.FirebaseApplication(FIREBASE_DB_URL, None)
        self._ensure_campaigns_directory()

    def _ensure_campaigns_directory(self):
        """Ensure campaigns directory exists in Firebase."""
        if not self.firebase_db.get('/campaigns', None):
            self.firebase_db.put('/', 'campaigns', {}, params={'auth': FIREBASE_API_SECRET})

    def create_campaign(self, chat_id, campaign_name, dm_username):
        """
        Create a new campaign.
        
        Args:
            chat_id (int): Chat ID where campaign is created
            campaign_name (str): Name of the campaign
            dm_username (str): Username of the Dungeon Master
        
        Returns:
            tuple: (campaign_id, campaign_data)
        """
        campaign_data = {
            'name': campaign_name,
            'dm': dm_username,
            'chat_id': chat_id,
            'active': True,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            }
            
            self.ref.child('campaigns').push(campaign_data)
        except Exception as e:
            logger.error(f"Error adding campaign: {str(e)}")
            raise

    def get_campaign(self, campaign_id: str) -> Campaign:
        """Get a campaign by ID."""
        campaign_data = self.ref.child(f'campaigns/{campaign_id}').get()
        if not campaign_data:
            raise exceptions.CampaignNotFound(f"Campaign {campaign_id} not found")
            
        return Campaign(
            id=campaign_id,
            name=campaign_data['name'],
            description=campaign_data['description'],
            dm=campaign_data['dm'],
            players=campaign_data['players'],
            current_turn=campaign_data['current_turn']
        )

    def update_campaign(self, campaign_id: str, campaign: Campaign) -> None:
        """Update an existing campaign."""
        try:
            campaign_data = {
                'name': campaign.name,
                'description': campaign.description,
                'updated_at': datetime.now().isoformat(),
                'dm': campaign.dm,
                'players': campaign.players,
                'current_turn': campaign.current_turn
            }
            
            self.ref.child(f'campaigns/{campaign_id}').update(campaign_data)
        except Exception as e:
            logger.error(f"Error updating campaign: {str(e)}")
            raise

    def delete_campaign(self, campaign_id: str) -> None:
        """Delete a campaign."""
        try:
            self.ref.child(f'campaigns/{campaign_id}').set(None)
        except Exception as e:
            logger.error(f"Error deleting campaign: {str(e)}")
            raise

    def add_character(self, campaign_id: str, character: Character) -> None:
        """Add a character to a campaign."""
        try:
            character_data = {
                'name': character.name,
                'race': character.race,
                'character_class': character.character_class,
                'level': character.level,
                'experience': character.experience,
                'hit_points': character.hit_points,
                'current_hit_points': character.current_hit_points,
                'currency': character.currency,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            self.ref.child(f'campaigns/{campaign_id}/characters').push(character_data)
        except Exception as e:
            logger.error(f"Error adding character: {str(e)}")
            raise

    def get_characters(self, campaign_id: str) -> list:
        """Get all characters in a campaign."""
        characters = self.ref.child(f'campaigns/{campaign_id}/characters').get()
        if not characters:
            return []
            
        return list(characters.values())

    def update_character(self, campaign_id: str, character: Character) -> None:
        """Update a character."""
        try:
            character_data = {
                'name': character.name,
                'race': character.race,
                'character_class': character.character_class,
                'level': character.level,
                'experience': character.experience,
                'hit_points': character.hit_points,
                'current_hit_points': character.current_hit_points,
                'currency': character.currency,
                'updated_at': datetime.now().isoformat()
            }
            
            self.ref.child(f'campaigns/{campaign_id}/characters/{character.id}').update(character_data)
        except Exception as e:
            logger.error(f"Error updating character: {str(e)}")
            raise

    def delete_character(self, campaign_id: str, character_id: str) -> None:
        """Delete a character from a campaign."""
        try:
            self.ref.child(f'campaigns/{campaign_id}/characters/{character_id}').set(None)
        except Exception as e:
            logger.error(f"Error deleting character: {str(e)}")
            raise

    def add_npc(self, campaign_id: str, npc: NPC) -> None:
        """Add an NPC to a campaign."""
        try:
            npc_data = {
                'name': npc.name,
                'race': npc.race,
                'npc_class': npc.npc_class,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            self.ref.child(f'campaigns/{campaign_id}/npcs').push(npc_data)
        except Exception as e:
            logger.error(f"Error adding NPC: {str(e)}")
            raise

    def get_npcs(self, campaign_id: str) -> list:
        """Get all NPCs in a campaign."""
        npcs = self.ref.child(f'campaigns/{campaign_id}/npcs').get()
        if not npcs:
            return []
            
        return list(npcs.values())
        return [Adventure(adventure) for adventure in adventures.values()]

    def get_adventure_by_name(self, chat_id, name):
        """Get an adventure by name."""
        campaign_id, campaign = self.get_campaign(chat_id)
        if campaign_id is None:
            raise CampaignNotFoundException("No active campaign found")

        adventures = self.firebase_db.get(f'/campaigns/{campaign_id}/adventures',
                                  None,
                                  params={'auth': FIREBASE_API_SECRET})
        
        if adventures is None:
            return None
            
        for adventure in adventures.values():
            if adventure['name'].lower() == name.lower():
                return Adventure(adventure)
        
        return None

    def update_adventure(self, chat_id, adventure):
        """Update an existing adventure."""
        campaign_id, campaign = self.get_campaign(chat_id)
        if campaign_id is None:
            raise CampaignNotFoundException("No active campaign found")

        adventure_data = adventure.to_json()
        adventure_data['chat_id'] = chat_id
        
        adventures = self.firebase_db.get(f'/campaigns/{campaign_id}/adventures',
                                  None,
                                  params={'auth': FIREBASE_API_SECRET})
        
        if adventures is None:
            return
            
        for adventure_id, adventure_data in adventures.items():
            if adventure_data['name'].lower() == adventure.name.lower():
                self.firebase_db.patch(f'/campaigns/{campaign_id}/adventures/{adventure_id}',
                                     data=adventure_data,
                                     params={'auth': FIREBASE_API_SECRET})
                break

    def delete_adventure(self, chat_id, adventure):
        """Delete an adventure from the campaign."""
        campaign_id, campaign = self.get_campaign(chat_id)
        if campaign_id is None:
            raise CampaignNotFoundException("No active campaign found")

        adventures = self.firebase_db.get(f'/campaigns/{campaign_id}/adventures',
                                  None,
                                  params={'auth': FIREBASE_API_SECRET})
        
        if adventures is None:
            return
            
        for adventure_id, adventure_data in adventures.items():
            if adventure_data['name'].lower() == adventure.name.lower():
                self.firebase_db.delete(f'/campaigns/{campaign_id}/adventures/{adventure_id}',
                                      None,
                                      params={'auth': FIREBASE_API_SECRET})
                break


class CampaignActiveException(Exception):
    def __init__(self, message):
        super().__init__(message)


class CampaignNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
