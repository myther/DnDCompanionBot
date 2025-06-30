import requests
from typing import Dict, List, Optional
from models.adventure import Adventure
import os
import hashlib
import json
from datetime import datetime

class ExternalSources:
    """Service for working with external sources of D&D content."""
    
    DND5E_API_URL = "https://www.dnd5eapi.co"
    
    def __init__(self, cache_dir: str = "./cache"):
        """
        Initialize the service with cache directory.
        
        Args:
            cache_dir (str): Directory for storing cached data
        """
        self.cache_dir = cache_dir
        self._ensure_cache_directory()
        
    def _ensure_cache_directory(self):
        """Create cache directory if it doesn't exist."""
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def _get_cached_data(self, url: str) -> Optional[Dict]:
        """
        Get cached data for a URL if available.
        
        Args:
            url (str): URL to check cache for
            
        Returns:
            Optional[Dict]: Cached data if available, None otherwise
        """
        cache_file = os.path.join(self.cache_dir, f"{hashlib.md5(url.encode()).hexdigest()}.json")
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        
    def _cache_data(self, url: str, data: Dict):
        """
        Cache data for a URL.
        
        Args:
            url (str): URL to cache data for
            data (Dict): Data to cache
        """
        cache_file = os.path.join(self.cache_dir, f"{hashlib.md5(url.encode()).hexdigest()}.json")
        with open(cache_file, 'w') as f:
            json.dump(data, f)
            
    def get_adventure_from_url(self, url: str) -> Optional[Adventure]:
        """
        Import an adventure from an external URL.
        
        Args:
            url (str): URL of the adventure
            
        Returns:
            Optional[Adventure]: Imported adventure or None if failed
        """
        cached_data = self._get_cached_data(url)
        if cached_data:
            return Adventure(cached_data)
            
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Convert data to Adventure format
            adventure_data = {
                'name': data.get('title', 'Unknown Adventure'),
                'description': data.get('description', ''),
                'level_range': data.get('level_range', [1, 20]),
                'players': [],
                'npcs': data.get('npcs', []),
                'monsters': data.get('monsters', []),
                'locations': data.get('locations', []),
                'encounters': data.get('encounters', []),
                'items': data.get('items', []),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'status': 'imported'
            }
            
            adventure = Adventure(adventure_data)
            self._cache_data(url, adventure_data)
            return adventure
            
        except requests.RequestException as e:
            print(f"Error importing adventure: {e}")
            return None
            
    def get_adventure_from_dnd5e_api(self, adventure_id: str) -> Optional[Adventure]:
        """
        Import an adventure from the D&D 5e API.
        
        Args:
            adventure_id (str): ID of the adventure
            
        Returns:
            Optional[Adventure]: Imported adventure or None if failed
        """
        url = f"{self.DND5E_API_URL}/api/adventures/{adventure_id}"
        return self.get_adventure_from_url(url)
        
    def search_adventures(self, query: str) -> List[Dict]:
        """
        Search for adventures using the D&D 5e API.
        
        Args:
            query (str): Search query
            
        Returns:
            List[Dict]: List of adventure results
        """
        url = f"{self.DND5E_API_URL}/api/adventures"
        try:
            response = requests.get(url)
            response.raise_for_status()
            adventures = response.json()
            
            return [
                {
                    'id': adv['index'],
                    'name': adv['name'],
                    'description': adv.get('desc', ''),
                    'level_range': adv.get('level_range', [1, 20])
                }
                for adv in adventures
                if query.lower() in adv['name'].lower()
            ]
            
        except requests.RequestException as e:
            print(f"Error searching adventures: {e}")
            return []
