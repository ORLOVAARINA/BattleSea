import requests

# URL API для получения случайной активности
bored_api_url = "https://bored-api.appbrewery.com/random"

#Получения случайной активности из API
def get_random_activity():
    try:
        response = requests.get(bored_api_url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        return data.get("activity", "Не удалось получить идею :(") # Используем get, чтобы избежать ошибки KeyError
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return "Не удалось получить идею :("