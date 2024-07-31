import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import SearchHistory

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def get_weather(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        api_key = 'b1345553c03cabd7c9dd2b93bda34317'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

        response = requests.get(url)
        weather_data = response.json()

        if weather_data['cod'] == 200:
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']

            # Save the search history
            SearchHistory.objects.create(
                user=request.user,
                city=city,
                temperature=temperature,
                description=description,
                humidity=humidity,
                wind_speed=wind_speed,
            )

            context = {
                'city': city,
                'temperature': temperature,
                'description': description,
                'humidity': humidity,
                'wind_speed': wind_speed,
            }
            return render(request, 'weather_result.html', context)
        else:
            error_message = weather_data.get('message', 'City not found')
            return render(request, 'home.html', {'error': error_message})
    return redirect('home')

@login_required
def search_history(request):
    search_history = SearchHistory.objects.filter(user=request.user).order_by('-date_searched')
    context = {
        'search_history': search_history,
    }
    return render(request, 'history.html', context)

