import re
from config import CATEGORIES, CITY
from datetime import datetime, timedelta
import requests
import math

def correct_variant(text: str)-> bool:
    date_pattern = r'\d{2}\.\d{2}\.\d{2}'
    integer_pattern = r'-?\d+'
    word_pattern = rf'({"|".join(CATEGORIES)})'
    pattern = rf'{date_pattern}\s*{integer_pattern}\s*{word_pattern}'
    match = re.match(pattern, text)
    return True if match else False

def get_last_seven_days()->list:
    # Получаем текущую дату
    today = datetime.now()
    dates = []
    for i in range(7):
        date = today - timedelta(days=i)
        formatted_date = f"{date.day:02d}.{date.month:02d}.{date.year % 100}"
        dates.append(formatted_date)
    return dates

def correct_with_number(text: str)-> bool:
    date_pattern = r'\d{2}\.\d{2}\.\d{2}'
    integer_pattern = r'-?\d+'
    word_pattern = rf'({"|".join(CATEGORIES)})'
    pattern = rf'{integer_pattern}\s*{date_pattern}\s*{integer_pattern}\s*{word_pattern}'
    match = re.match(pattern, text)
    return True if match else False

def forecaster()->str:
    url = 'https://api.openweathermap.org/data/2.5/forecast?q=' + CITY +'&units=metric&lang=ru&appid=a8db06017af6e030b1ef9d31cc9f5536'
    data = requests.get(url).json()
    temp = data['list'][0]['main']['temp']
    feel_temp = data['list'][0]['main']['feels_like']
    humidity = data['list'][0]['main']['humidity']
    wind = data['list'][0]['wind']['speed']
    description = data['list'][0]['weather'][0]['description']
    data_time = data['list'][0]['dt_txt']
    town = data['city']['name']
    otvet = (f'Привет, Хозяин, настоящим докладываю тебе прогноз погоды\n'
             f'Температура: {round(temp, 1)} градусов\n'
             f'Ощущается как: {round(feel_temp, 1)} градусов\n'
             f'Влажность: {humidity} процентов\n'
             f'Скорость ветра: {wind} м/с\n'
             f'Характеристика погоды: {description}\n'
             f'Дата и время измерения: {data_time}\n'
             f'Город: {town}')
    return otvet

def weaher_9pm()->str:
    url = 'https://api.openweathermap.org/data/2.5/forecast?q=' + CITY +'&units=metric&lang=ru&appid=a8db06017af6e030b1ef9d31cc9f5536'
    data = requests.get(url).json()
    temp = data['list'][3]['main']['temp']
    feel_temp = data['list'][3]['main']['feels_like']
    humidity = data['list'][3]['main']['humidity']
    wind = data['list'][3]['wind']['speed']
    description = data['list'][3]['weather'][0]['description']
    data_time = data['list'][3]['dt_txt']
    town = data['city']['name']
    otvet = (f'Настоящим докладываю тебе прогноз погоды на ЗАВТРА 06:00\n'
             f'Температура: {round(temp, 1)} градусов\n'
             f'Ощущается как: {round(feel_temp, 1)} градусов\n'
             f'Влажность: {humidity} процентов\n'
             f'Скорость ветра: {wind} м/с\n'
             f'Характеристика погоды: {description}\n'
             f'Дата и время измерения: {data_time}\n'
             f'Город: {town}')
    return otvet

def correct_zametka(messagetext: str)->bool:
    pattern = r'\d+\s+\w+'
    match = re.match(pattern, messagetext)
    return True if match else False # проверка правильности заметки