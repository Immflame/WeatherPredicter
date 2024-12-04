import requests
from app import check_bad_weather

''' ТЕСТЫ '''

url = "http://127.0.0.1:5000/weather_check"
data = {"latitude": 55.7522, "longitude": 37.6156} #координаты ЦУ
print(requests.post(url, json=data).json())

print(check_bad_weather(-5, 10, 20))
print(check_bad_weather(40, 10, 20))
print(check_bad_weather(20, 60, 20))
print(check_bad_weather(20, 10, 80))
print(check_bad_weather(20, 10, 20))
# Все исправно работает

