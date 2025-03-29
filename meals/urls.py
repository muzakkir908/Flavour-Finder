from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),
    path('meal/<int:meal_id>/', views.meal_detail, name='meal_detail'),
    path('meal/<int:meal_id>/favorite/add/', views.add_favorite, name='add_favorite'),
    path('meal/<int:meal_id>/favorite/remove/', views.remove_favorite, name='remove_favorite'),
    path('favorites/check/<int:meal_id>/', views.check_favorite, name='check_favorite'),
    path('favorites/', views.favorites, name='favorites'),
    path('random/', views.random_meal, name='random_meal'),
    path('meal-planner/', views.meal_planner, name='meal_planner'),  # New URL for meal planner
    path('api/test-maps/', views.test_maps_api, name='test_maps_api'),
    path('maps-test/', views.maps_test, name='maps_test'),
]