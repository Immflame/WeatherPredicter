import requests
from flask import Flask, jsonify, request


app = Flask(__name__)
API_KEY = '9Etl6nguqorKbY1pVtI8aDybzGzT5BAC'


def get_weather_data(latitude, longitude, api_key):
    """Получает данные о погоде"""
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{get_location(latitude, longitude, api_key)}?apikey={api_key}&language=ru-ru&details=true"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        return data[0] # Возвращаем данные о погоде
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None


def get_location(lat, lon, api_key):
    """Получает locationKey"""
    url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={api_key}&q={lat},{lon}&language=ru-ru"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['Key']
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None


def check_bad_weather(temperature, wind_speed, rain_probability):
    """Проверяет является ли погода плохой"""
    if (temperature < 0 or temperature > 35) or \
            wind_speed > 50 or \
            rain_probability > 70:
        return "Плохие погодные условия"
    else:
        return "Хорошие погодные условия"


@app.route('/weather_check', methods=['POST'])
def weather_check():
    """Обрабатывает запрос на проверку погодных условий."""
    try:
        data = request.get_json()
        latitude = data['latitude']
        longitude = data['longitude']

        weather_data = get_weather_data(latitude, longitude, API_KEY)
        if weather_data:
            temperature = weather_data['Temperature']['Metric']['Value']
            wind_speed = weather_data['Wind']['Speed']['Metric']['Value']
            rain_probability = weather_data['PrecipitationSummary']['PrecipitationProbability'] if 'PrecipitationSummary' in weather_data and 'PrecipitationProbability' in weather_data['PrecipitationSummary'] else 0

            weather_condition = check_bad_weather(temperature, wind_speed, rain_probability)
            return jsonify({"weather_condition": weather_condition})
        else:
            return jsonify({"error": "Ошибка получения данных о погоде"}), 500
    except (KeyError, TypeError, requests.exceptions.RequestException) as e:
        return jsonify({"error": f"Ошибка: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)

