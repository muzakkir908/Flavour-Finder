# meals/utils.py
import requests
from django.conf import settings
from django.core.cache import cache

def fetch_advertisements():
    """Utility function to fetch ads with caching."""
    cache_key = 'advertisements_data'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    try:
        response = requests.get(settings.ADVERTISEMENT_API_URL, timeout=5)
        response.raise_for_status()
        ads = response.json()
        cache.set(cache_key, ads, settings.ADVERTISEMENT_CACHE_TIMEOUT)
        return ads
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching advertisements: {e}")
        return []