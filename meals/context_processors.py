# meals/context_processors.py
from django.conf import settings
from django.core.cache import cache  # Add this import
import requests
import logging

def google_maps_api_key(request):
    """Add Google Maps API key to all templates."""
    return {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
    
    

def advertisements(request):
    """Fetch and cache advertisements for all templates."""
    cache_key = 'advertisements_data'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return {'advertisements': cached_data}
    
    try:
        response = requests.get(settings.ADVERTISEMENT_API_URL, timeout=5)
        response.raise_for_status()
        ads = response.json()
        cache.set(cache_key, ads, settings.ADVERTISEMENT_CACHE_TIMEOUT)
        return {'advertisements': ads}
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching advertisements: {e}")
        return {'advertisements': []}