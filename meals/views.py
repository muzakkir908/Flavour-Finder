import json
import random
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
from .models import Favorite
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


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
    
    # Debug information
    print(f"Searching for ingredient: {ingredient}")
    
    try:
        # Use different API endpoint for MealDB
        api_url = "https://www.themealdb.com/api/json/v1/1/filter.php"
        
        # Make request to the API
        response = requests.get(api_url, params={'i': ingredient}, timeout=10)
        
        # Check if request was successful
        if response.status_code == 200:
            try:
                data = response.json()
                meals = data.get('meals', [])
                
                # For debugging
                print(f"API response: Found {len(meals) if meals else 0} meals")
            except ValueError:
                # Handle invalid JSON
                print(f"Error parsing JSON response: {response.text[:200]}")
                meals = []
        else:
            # Handle unsuccessful response
            print(f"API request failed with status code: {response.status_code}")
            print(f"Response content: {response.text[:200]}")
            meals = []
            
    except requests.RequestException as e:
        # Handle request exceptions (network issues, timeouts, etc.)
        print(f"Request error: {str(e)}")
        meals = []
    
    # Fallback to sample data if no results
    if not meals and ingredient.lower() in ['chicken', 'beef', 'pasta', 'potato', 'rice', 'fish']:
        # Provide sample data for common ingredients when API fails
        sample_meals = {
            'chicken': [
                {'strMeal': 'Chicken Alfredo', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/syqypv1486981727.jpg', 'idMeal': '52772'},
                {'strMeal': 'Chicken Enchilada Casserole', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/qtuwxu1468233098.jpg', 'idMeal': '52765'},
                {'strMeal': 'Chicken Parmesan', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/ustsqw1468250014.jpg', 'idMeal': '52795'}
            ],
            'beef': [
                {'strMeal': 'Beef Stroganoff', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/svprys1511176755.jpg', 'idMeal': '52834'},
                {'strMeal': 'Beef Wellington', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/vvpprx1487325699.jpg', 'idMeal': '52803'},
                {'strMeal': 'Beef Stir-Fry', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/xwutty1511555540.jpg', 'idMeal': '52919'}
            ],
            'pasta': [
                {'strMeal': 'Spaghetti Carbonara', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/llcbn01574260722.jpg', 'idMeal': '52982'},
                {'strMeal': 'Lasagna', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/wtsvxx1511296896.jpg', 'idMeal': '52844'},
                {'strMeal': 'Pasta Primavera', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/rvxxuy1468312893.jpg', 'idMeal': '52837'}
            ],
            'potato': [
                {'strMeal': 'Potato Gratin', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/wtsvxx1511296896.jpg', 'idMeal': '52780'},
                {'strMeal': 'Mashed Potato', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/sxxpst1468569714.jpg', 'idMeal': '52783'},
                {'strMeal': 'Potato Wedges', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/bbrrmp1565175888.jpg', 'idMeal': '52785'}
            ],
            'rice': [
                {'strMeal': 'Vegetable Fried Rice', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/uxqqtu1468233310.jpg', 'idMeal': '52766'},
                {'strMeal': 'Rice Pudding', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/wxyvqq1511723401.jpg', 'idMeal': '52842'},
                {'strMeal': 'Risotto', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/rvxxuy1468312893.jpg', 'idMeal': '52823'}
            ],
            'fish': [
                {'strMeal': 'Fish and Chips', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/ysxwuq1487323065.jpg', 'idMeal': '52802'},
                {'strMeal': 'Grilled Salmon', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/xxrxux1503070723.jpg', 'idMeal': '52773'},
                {'strMeal': 'Fish Pie', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/ysxwuq1487323065.jpg', 'idMeal': '52804'}
            ]
        }
        
        meals = sample_meals.get(ingredient.lower(), [])
        print(f"Using sample data for {ingredient}: {len(meals)} recipes")
    
    # Initialize data as an empty dict if it's not defined yet
    if 'data' not in locals():
        data = {'meals': None}
    
    context = {
        'ingredient': ingredient,
        'meals': meals,
        'count': len(meals) if meals else 0,
        'using_sample_data': len(meals) > 0 and not data.get('meals') if 'data' in locals() else False
    }
    
    return render(request, 'meals/search_results.html', context)

def nearby_restaurants(request):
    """Display nearby restaurants based on the user's location and query."""
    query = request.GET.get('q', 'restaurant')
    latitude = request.GET.get('lat', '')
    longitude = request.GET.get('lng', '')
    
    context = {
        'query': query,
        'latitude': latitude,
        'longitude': longitude,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    
    return render(request, 'meals/nearby_restaurants.html', context)
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
    
    # Process instructions into steps
    instruction_steps = []
    if meal.get('strInstructions'):
        # Replace line breaks with a standard format
        instructions_text = meal['strInstructions'].replace('\r\n', '\n').replace('\r', '\n')
        # Split into paragraphs
        paragraphs = instructions_text.split('\n')
        # Add non-empty paragraphs as steps
        for paragraph in paragraphs:
            if paragraph.strip() and len(paragraph.strip()) > 5:
                instruction_steps.append(paragraph.strip())
    
    # Extract YouTube video ID if present
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
        'ingredients': ingredients,
        'instruction_steps': instruction_steps
    }
    
    return render(request, 'meals/meal_detail.html', context)

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

def test_maps_api(request):
    """Test Google Maps API connection."""
    api_key = settings.GOOGLE_MAPS_API_KEY
    test_url = f"https://maps.googleapis.com/maps/api/geocode/json?address=New+York&key={api_key}"
    
    try:
        response = requests.get(test_url)
        data = response.json()
        
        # Log the full response for debugging
        print(f"Google Maps API Test Response: {data}")
        
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
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'meals/maps_test.html', context)
    
def meal_planner(request):
    """Generate a weekly meal plan based on preferences."""
    # Get parameters from request
    diet = request.GET.get('diet', 'balanced')  # balanced, vegetarian, vegan, etc.
    meals_per_day = int(request.GET.get('meals', '3'))  # 1-5 meals per day
    days = int(request.GET.get('days', '7'))  # 1-7 days
    calories = request.GET.get('calories', '')  # Target daily calories
    
    # Generate a weekly meal plan
    meal_plan = generate_meal_plan(diet, meals_per_day, days, calories)
    
    context = {
        'meal_plan': meal_plan,
        'diet': diet,
        'meals_per_day': meals_per_day,
        'days': days,
        'calories': calories
    }
    
    return render(request, 'meals/meal_planner.html', context)

def generate_meal_plan(diet='balanced', meals_per_day=3, days=7, calories=''):
    """Generate a meal plan."""
    # For demonstration purposes, we'll use a mix of static meals
    # In a real app, you would call an API or use a database
    
    breakfast_options = [
        {'name': 'Avocado Toast with Eggs', 'calories': 350, 'protein': 18, 'carbs': 30, 'fat': 20, 'image': 'https://www.themealdb.com/images/media/meals/1550440197.jpg'},
        {'name': 'Overnight Oats with Berries', 'calories': 280, 'protein': 12, 'carbs': 45, 'fat': 8, 'image': 'https://www.themealdb.com/images/media/meals/1550441882.jpg'},
        {'name': 'Greek Yogurt with Granola', 'calories': 300, 'protein': 15, 'carbs': 40, 'fat': 10, 'image': 'https://www.themealdb.com/images/media/meals/1550441275.jpg'},
        {'name': 'Protein Smoothie Bowl', 'calories': 320, 'protein': 20, 'carbs': 35, 'fat': 12, 'image': 'https://www.themealdb.com/images/media/meals/1550442508.jpg'},
        {'name': 'Vegetable Omelette', 'calories': 290, 'protein': 22, 'carbs': 8, 'fat': 18, 'image': 'https://www.themealdb.com/images/media/meals/1550441197.jpg'}
    ]
    
    lunch_options = [
        {'name': 'Quinoa Salad with Chicken', 'calories': 420, 'protein': 25, 'carbs': 40, 'fat': 15, 'image': 'https://www.themealdb.com/images/media/meals/1550441683.jpg'},
        {'name': 'Mediterranean Wrap', 'calories': 380, 'protein': 18, 'carbs': 45, 'fat': 14, 'image': 'https://www.themealdb.com/images/media/meals/1550441896.jpg'},
        {'name': 'Lentil Soup with Whole Grain Bread', 'calories': 340, 'protein': 16, 'carbs': 48, 'fat': 10, 'image': 'https://www.themealdb.com/images/media/meals/1550441378.jpg'},
        {'name': 'Asian Noodle Bowl', 'calories': 410, 'protein': 15, 'carbs': 60, 'fat': 12, 'image': 'https://www.themealdb.com/images/media/meals/1550441997.jpg'},
        {'name': 'Tuna Salad Sandwich', 'calories': 360, 'protein': 22, 'carbs': 35, 'fat': 16, 'image': 'https://www.themealdb.com/images/media/meals/1550440195.jpg'}
    ]
    
    dinner_options = [
        {'name': 'Grilled Salmon with Roasted Vegetables', 'calories': 480, 'protein': 30, 'carbs': 25, 'fat': 22, 'image': 'https://www.themealdb.com/images/media/meals/1548772327.jpg'},
        {'name': 'Chicken Stir-Fry with Brown Rice', 'calories': 450, 'protein': 28, 'carbs': 50, 'fat': 14, 'image': 'https://www.themealdb.com/images/media/meals/1548772327.jpg'},
        {'name': 'Vegetable Lasagna', 'calories': 420, 'protein': 18, 'carbs': 48, 'fat': 20, 'image': 'https://www.themealdb.com/images/media/meals/1549542877.jpg'},
        {'name': 'Beef and Broccoli', 'calories': 460, 'protein': 32, 'carbs': 30, 'fat': 18, 'image': 'https://www.themealdb.com/images/media/meals/1546869496.jpg'},
        {'name': 'Tofu and Vegetable Curry with Rice', 'calories': 410, 'protein': 15, 'carbs': 55, 'fat': 16, 'image': 'https://www.themealdb.com/images/media/meals/1550441266.jpg'}
    ]
    
    snack_options = [
        {'name': 'Apple with Almond Butter', 'calories': 180, 'protein': 5, 'carbs': 20, 'fat': 10, 'image': 'https://www.themealdb.com/images/media/meals/1550442107.jpg'},
        {'name': 'Protein Bar', 'calories': 200, 'protein': 15, 'carbs': 25, 'fat': 8, 'image': 'https://www.themealdb.com/images/media/meals/1550442408.jpg'},
        {'name': 'Hummus with Vegetable Sticks', 'calories': 150, 'protein': 6, 'carbs': 15, 'fat': 8, 'image': 'https://www.themealdb.com/images/media/meals/1550442365.jpg'},
        {'name': 'Greek Yogurt with Honey', 'calories': 170, 'protein': 12, 'carbs': 20, 'fat': 5, 'image': 'https://www.themealdb.com/images/media/meals/1550441275.jpg'},
        {'name': 'Trail Mix', 'calories': 210, 'protein': 7, 'carbs': 18, 'fat': 14, 'image': 'https://www.themealdb.com/images/media/meals/1550442431.jpg'}
    ]
    
    # Adjust options based on diet preference
    if diet == 'vegetarian':
        dinner_options = [m for m in dinner_options if 'Chicken' not in m['name'] and 'Beef' not in m['name'] and 'Salmon' not in m['name']]
        lunch_options = [m for m in lunch_options if 'Chicken' not in m['name'] and 'Tuna' not in m['name']]
    elif diet == 'vegan':
        breakfast_options = [m for m in breakfast_options if 'Eggs' not in m['name'] and 'Yogurt' not in m['name']]
        lunch_options = [m for m in lunch_options if 'Chicken' not in m['name'] and 'Tuna' not in m['name']]
        dinner_options = [m for m in dinner_options if 'Chicken' not in m['name'] and 'Beef' not in m['name'] and 'Salmon' not in m['name']]
        snack_options = [m for m in snack_options if 'Yogurt' not in m['name']]
    
    # Generate the meal plan
    import random
    import datetime
    
    meal_plan = []
    start_date = datetime.datetime.now()
    
    for day in range(days):
        current_date = (start_date + datetime.timedelta(days=day)).strftime('%A, %B %d')
        day_plan = {
            'date': current_date,
            'meals': []
        }
        
        # Daily total nutrition
        day_calories = 0
        day_protein = 0
        day_carbs = 0
        day_fat = 0
        
        # Distribute meals based on meals_per_day
        if meals_per_day == 1:
            # Just dinner
            meal = random.choice(dinner_options)
            day_plan['meals'].append({'type': 'Dinner', 'meal': meal})
            day_calories += meal['calories']
            day_protein += meal['protein']
            day_carbs += meal['carbs']
            day_fat += meal['fat']
        elif meals_per_day == 2:
            # Breakfast and dinner
            breakfast = random.choice(breakfast_options)
            dinner = random.choice(dinner_options)
            day_plan['meals'].append({'type': 'Breakfast', 'meal': breakfast})
            day_plan['meals'].append({'type': 'Dinner', 'meal': dinner})
            day_calories += breakfast['calories'] + dinner['calories']
            day_protein += breakfast['protein'] + dinner['protein']
            day_carbs += breakfast['carbs'] + dinner['carbs']
            day_fat += breakfast['fat'] + dinner['fat']
        elif meals_per_day == 3:
            # Three meals
            breakfast = random.choice(breakfast_options)
            lunch = random.choice(lunch_options)
            dinner = random.choice(dinner_options)
            day_plan['meals'].append({'type': 'Breakfast', 'meal': breakfast})
            day_plan['meals'].append({'type': 'Lunch', 'meal': lunch})
            day_plan['meals'].append({'type': 'Dinner', 'meal': dinner})
            day_calories += breakfast['calories'] + lunch['calories'] + dinner['calories']
            day_protein += breakfast['protein'] + lunch['protein'] + dinner['protein']
            day_carbs += breakfast['carbs'] + lunch['carbs'] + dinner['carbs']
            day_fat += breakfast['fat'] + lunch['fat'] + dinner['fat']
        elif meals_per_day >= 4:
            # Three meals plus snacks
            breakfast = random.choice(breakfast_options)
            lunch = random.choice(lunch_options)
            dinner = random.choice(dinner_options)
            snack1 = random.choice(snack_options)
            day_plan['meals'].append({'type': 'Breakfast', 'meal': breakfast})
            day_plan['meals'].append({'type': 'Lunch', 'meal': lunch})
            day_plan['meals'].append({'type': 'Dinner', 'meal': dinner})
            day_plan['meals'].append({'type': 'Snack', 'meal': snack1})
            day_calories += breakfast['calories'] + lunch['calories'] + dinner['calories'] + snack1['calories']
            day_protein += breakfast['protein'] + lunch['protein'] + dinner['protein'] + snack1['protein']
            day_carbs += breakfast['carbs'] + lunch['carbs'] + dinner['carbs'] + snack1['carbs']
            day_fat += breakfast['fat'] + lunch['fat'] + dinner['fat'] + snack1['fat']
            
            # Add a second snack if meals_per_day is 5
            if meals_per_day >= 5:
                snack2 = random.choice([s for s in snack_options if s != snack1])
                day_plan['meals'].append({'type': 'Snack', 'meal': snack2})
                day_calories += snack2['calories']
                day_protein += snack2['protein']
                day_carbs += snack2['carbs']
                day_fat += snack2['fat']
        
        # Add nutrition totals
        day_plan['nutrition'] = {
            'calories': day_calories,
            'protein': day_protein,
            'carbs': day_carbs,
            'fat': day_fat
        }
        
        meal_plan.append(day_plan)
    
    return meal_plan

# Login-required versions of the favorite functions
@login_required
@csrf_exempt
def add_favorite(request, meal_id):
    """Add a meal to favorites."""
    if request.method == 'POST':
        meal_name = request.POST.get('meal_name')
        meal_thumb = request.POST.get('meal_thumb')
        
        # Check if already in favorites for this user
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
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

@login_required
@csrf_exempt
def remove_favorite(request, meal_id):
    """Remove a meal from favorites."""
    if request.method == 'POST':
        try:
            favorite = Favorite.objects.get(user=request.user, meal_id=meal_id)
            favorite.delete()
            return JsonResponse({'status': 'removed'})
        except Favorite.DoesNotExist:
            return JsonResponse({'status': 'not_found'})
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def favorites(request):
    """Display user's favorite meals."""
    favorites = Favorite.objects.filter(user=request.user).order_by('-date_added')
    
    context = {
        'favorites': favorites
    }
    
    return render(request, 'meals/favorites.html', context)

@login_required
def check_favorite(request, meal_id):
    """Check if a meal is in favorites."""
    is_favorite = Favorite.objects.filter(user=request.user, meal_id=meal_id).exists()
    return JsonResponse({'is_favorite': is_favorite})