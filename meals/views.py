import json
import random
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
from .models import Favorite
from django.views.decorators.csrf import csrf_exempt


# API endpoints
MEALDB_BASE_URL = "https://www.themealdb.com/api/json/v1/1"
SEARCH_BY_INGREDIENT_URL = f"{MEALDB_BASE_URL}/filter.php"
MEAL_DETAILS_URL = f"{MEALDB_BASE_URL}/lookup.php"
RANDOM_MEAL_URL = f"{MEALDB_BASE_URL}/random.php"

def home(request):
    """Home page view with search form and random meal button."""
    return render(request, 'meals/home.html')

def search_results(request):
    """Display search results based on the ingredient provided."""
    ingredient = request.GET.get('ingredient', '')
    
    if not ingredient:
        return redirect('home')
    
    # Call the MealDB API to search by ingredient
    response = requests.get(SEARCH_BY_INGREDIENT_URL, params={'i': ingredient})
    data = response.json()
    
    meals = data.get('meals', [])
    
    context = {
        'ingredient': ingredient,
        'meals': meals,
        'count': len(meals) if meals else 0
    }
    
    return render(request, 'meals/search_results.html', context)

def nearby_restaurants(request):
    """Display nearby restaurants based on the user's location and query."""
    query = request.GET.get('q', '')
    latitude = request.GET.get('lat', '')
    longitude = request.GET.get('lng', '')
    
    # Create some sample data since we can't use Google Places API
    sample_restaurants = []
    
    if query and (latitude and longitude):
        # Generate sample restaurants based on the query
        restaurant_names = [
            f"{query.title()} Palace",
            f"The {query.title()} House",
            f"Authentic {query.title()}",
            f"{query.title()} Express",
            f"Royal {query.title()}"
        ]
        
        distances = [0.5, 0.8, 1.2, 1.5, 2.0]
        ratings = [4.7, 4.2, 3.9, 4.5, 4.1]
        
        for i in range(5):
            sample_restaurants.append({
                'name': restaurant_names[i],
                'vicinity': f"{i+1} Main Street",
                'distance': distances[i],
                'rating': ratings[i],
                'reviews': (i+1) * 25
            })
    
    context = {
        'query': query,
        'latitude': latitude,
        'longitude': longitude,
        'restaurants': sample_restaurants,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'using_sample_data': True
    }
    
    return render(request, 'meals/nearby_restaurants.html', context)

def add_favorite(request, meal_id):
    """Add a meal to favorites."""
    if request.method == 'POST':
        meal_name = request.POST.get('meal_name')
        meal_thumb = request.POST.get('meal_thumb')
        
        # Check if already in favorites
        favorite, created = Favorite.objects.get_or_create(
            meal_id=meal_id,
            defaults={
                'meal_name': meal_name,
                'meal_thumb': meal_thumb
            }
        )
        
        if created:
            return JsonResponse({'status': 'added'})
        else:
            return JsonResponse({'status': 'exists'})
    
    return JsonResponse({'status': 'error'}, status=400)

def remove_favorite(request, meal_id):
    """Remove a meal from favorites."""
    if request.method == 'POST':
        try:
            favorite = Favorite.objects.get(meal_id=meal_id)
            favorite.delete()
            return JsonResponse({'status': 'removed'})
        except Favorite.DoesNotExist:
            return JsonResponse({'status': 'not_found'})
    
    return JsonResponse({'status': 'error'}, status=400)

def favorites(request):
    """Display user's favorite meals."""
    favorites = Favorite.objects.all().order_by('-date_added')
    
    context = {
        'favorites': favorites
    }
    
    return render(request, 'meals/favorites.html', context)

import requests
from django.http import HttpResponse
from django.shortcuts import render

MEAL_DETAILS_URL = "https://www.themealdb.com/api/json/v1/1/lookup.php"

def meal_detail(request, meal_id):
    """Display detailed information about a specific meal."""
    # Call the MealDB API to get meal details
    response = requests.get(MEAL_DETAILS_URL, params={'i': meal_id})
    data = response.json()
    
    meal = data.get('meals', [None])[0]
    
    if not meal:
        return HttpResponse("Meal not found", status=404)
    
    # Process ingredients and measurements
    ingredients = []
    for i in range(1, 21):  # MealDB provides up to 20 ingredients
        ingredient = meal.get(f'strIngredient{i}')
        measure = meal.get(f'strMeasure{i}')
        
        if ingredient and ingredient.strip():
            ingredients.append({
                'name': ingredient,
                'measure': measure
            })
    
    # ✅ Extract YouTube video ID if present
    if meal.get('strYoutube'):
        youtube_url = meal['strYoutube']
        if "v=" in youtube_url:
            video_id = youtube_url.split('v=')[-1]
        elif "youtu.be/" in youtube_url:
            video_id = youtube_url.split("youtu.be/")[-1]
        else:
            video_id = None

        if video_id:
            meal['youtube_embed_url'] = f"https://www.youtube.com/embed/{video_id}"
    
    context = {
        'meal': meal,
        'ingredients': ingredients
    }
    
    return render(request, 'meals/meal_detail.html', context)


def check_favorite(request, meal_id):
    """Check if a meal is in favorites."""
    is_favorite = Favorite.objects.filter(meal_id=meal_id).exists()
    return JsonResponse({'is_favorite': is_favorite})

def random_meal(request):
    """Redirect to a random meal detail page."""
    # Call the MealDB API to get a random meal
    response = requests.get(RANDOM_MEAL_URL)
    data = response.json()
    
    meal = data.get('meals', [None])[0]
    
    if not meal:
        return HttpResponse("Failed to get random meal", status=500)
    
    meal_id = meal.get('idMeal')
    return redirect('meal_detail', meal_id=meal_id)
def nearby_restaurants(request):
    """Display nearby restaurants based on the user's location and query."""
    query = request.GET.get('q', '')
    latitude = request.GET.get('lat', '')
    longitude = request.GET.get('lng', '')
    
    context = {
        'query': query,
        'latitude': latitude,
        'longitude': longitude,
        'google_maps_api_key': 'AIzaSyAtX02OJOKyVBmE3QV45Pm8qQKkHGlZ0xQ'
    }
    
    return render(request, 'meals/nearby_restaurants.html', context)

def nearby_restaurants(request):
    """Display nearby restaurants based on the user's location and query."""
    query = request.GET.get('q', '')
    
    # This is a placeholder for the actual implementation
    # In a real application, you would use Foursquare API or similar
    
    context = {
        'query': query,
        'message': 'This feature is coming soon!',
        'restaurants': []
    }
    
    return render(request, 'meals/nearby_restaurants.html', context)
    

@csrf_exempt
def add_favorite(request, meal_id):
    """Add a meal to favorites."""
    if request.method == 'POST':
        meal_name = request.POST.get('meal_name')
        meal_thumb = request.POST.get('meal_thumb')
        
        # Check if already in favorites
        favorite, created = Favorite.objects.get_or_create(
            meal_id=meal_id,
            defaults={
                'meal_name': meal_name,
                'meal_thumb': meal_thumb
            }
        )
        
        if created:
            return JsonResponse({'status': 'added'})
        else:
            return JsonResponse({'status': 'exists'})
    
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def remove_favorite(request, meal_id):
    """Remove a meal from favorites."""
    if request.method == 'POST':
        try:
            favorite = Favorite.objects.get(meal_id=meal_id)
            favorite.delete()
            return JsonResponse({'status': 'removed'})
        except Favorite.DoesNotExist:
            return JsonResponse({'status': 'not_found'})
    
    return JsonResponse({'status': 'error'}, status=400)
    
def test_maps_api(request):
    """Test Google Maps API connection."""
    api_key = settings.GOOGLE_MAPS_API_KEY
    test_url = f"https://maps.googleapis.com/maps/api/geocode/json?address=New+York&key={api_key}"
    
    try:
        response = requests.get(test_url)
        data = response.json()
        
        if data.get('status') == 'OK':
            return JsonResponse({'status': 'success', 'message': 'Google Maps API is working correctly'})
        else:
            return JsonResponse({
                'status': 'error', 
                'message': f"API Error: {data.get('status', 'Unknown error')}",
                'details': data.get('error_message', 'No details available')
            })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f"Connection error: {str(e)}"})
def maps_test(request):
    """Test page for Google Maps API."""
    context = {
        'api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'meals/maps_test.html', context)