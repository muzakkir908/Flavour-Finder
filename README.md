# Flavour Finder

A recipe discovery app built with Django. Search meals by ingredient, open a recipe, save favourites, plan meals, and find restaurants nearby.

## Features

- **Ingredient search** powered by [TheMealDB](https://www.themealdb.com/) API, with built-in fallback results if the API is unreachable
- **Recipe pages** with ingredients and instructions
- **Random meal** for when you can't decide
- **Favourites**: logged-in users save meals to their profile
- **Meal planner**
- **Nearby restaurants** using the Google Maps JavaScript API and Places library
- **Accounts**: register, log in, and reset your password with a one-time code sent by an AWS API Gateway OTP service
- **Caching**: responses from the external advertisement API are cached for an hour, so the app doesn't call it on every page load

## Stack

| Layer | Tech |
|---|---|
| Backend | Python, Django 4.2 |
| External APIs | TheMealDB, Google Maps / Places, AWS API Gateway (OTP) |
| Serving | Gunicorn, WhiteNoise, Docker |

## Run locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

export GOOGLE_MAPS_API_KEY=your-key   # Windows: set GOOGLE_MAPS_API_KEY=your-key
python manage.py migrate
python manage.py runserver
```

## Run with Docker

```bash
docker build -t flavour-finder .
docker run -p 8000:8000 -e GOOGLE_MAPS_API_KEY=your-key flavour-finder
```

## Project layout

```
flavorfinder/   settings and URLs
meals/          search, recipe pages, favourites, meal planner, maps
accounts/       registration, login, OTP password reset
profiles/       user profile
templates/      HTML templates
```
