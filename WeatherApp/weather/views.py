from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    appid = '5d290aeb1680295df037391e88d12b68'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    try:
        city = City.objects.last()
        res = requests.get(url.format(city.name)).json()
        current_info = {
            'city': city.name,
            'temp': int(round(res['main']['temp'], 0)),
            'temp_h': res['main']['temp_max'],
            'temp_l': res['main']['temp_min'],
            'icon': res['weather'][0]['icon'],
            'main': res['weather'][0]['main'],
            'wind': res['wind']['speed'],
            'feels_like': res['main']['feels_like']
        }
    except Exception as ex:
        res = requests.get(url.format('Saint Petersburg')).json()
        current_info = {
            'temp': int(round(res['main']['temp'], 0)),
            'temp_h': res['main']['temp_max'],
            'temp_l': res['main']['temp_min'],
            'icon': res['weather'][0]['icon'],
            'main': res['weather'][0]['main'],
            'wind': res['wind']['speed'],
            'feels_like': res['main']['feels_like']
        }

    context = {'info': current_info, 'form': form}

    return render(request, 'weather/index.html', context)
