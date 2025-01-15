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
             f'Город: г.{town}')
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
             f'Город: г.{town}')
    return otvet

def correct_zametka(messagetext: str)->bool:
    pattern = r'\d+\s+\w+'
    match = re.match(pattern, messagetext)
    return True if match else False # проверка правильности заметки


def rounder(time: datetime) -> datetime:
    """
    Функция округляет объект времени до ближайшего часа, который делится на 3.
    Args:
       time (datetime): объект времени, который нужно округлить.
    Returns:
       datetime: новый объект времени, который округлен до ближайшего часа, который делится на 3.
    """
    hours = math.floor(time.hour / 3) * 3
    rounded_time = time.replace(hour=hours, minute=0, second=0, microsecond=0)
    return rounded_time


def get_tomorrow_index() -> int:
    current_time = datetime.now()
    today = datetime.now().date()
    day = today.day
    month = today.month
    year = today.year
    tomorrow = datetime(year=year, month=month, day=day+1, hour=12, minute=0, second=0)
    delta = tomorrow - rounder(current_time)
    return int(delta.total_seconds() // 3600 / 3)



def weather_tomorrow(index: int) -> str:  
    url = 'https://api.openweathermap.org/data/2.5/forecast?q=' + CITY +'&units=metric&lang=ru&appid=a8db06017af6e030b1ef9d31cc9f5536'
    data = requests.get(url).json()
    temp = data['list'][index]['main']['temp']
    feel_temp = data['list'][index]['main']['feels_like']
    humidity = data['list'][index]['main']['humidity']
    wind = data['list'][index]['wind']['speed']
    description = data['list'][index]['weather'][0]['description']
    data_time = data['list'][index]['dt_txt']
    town = data['city']['name']
    otvet = (f'Настоящим докладываю тебе прогноз погоды\n'
             f'Температура: {round(temp, 1)} градусов\n'
             f'Ощущается как: {round(feel_temp, 1)} градусов\n'
             f'Влажность: {humidity} процентов\n'
             f'Скорость ветра: {wind} м/с\n'
             f'Характеристика погоды: {description}\n'
             f'Дата и время измерения: {data_time}\n'
             f'Город: г.{town}')
    return otvet


def get_morning_index() -> int:
    current_time = datetime.now()
    today = datetime.now().date()
    day = today.day
    month = today.month
    year = today.year
    tomorrow = datetime(year=year, month=month, day=day+1, hour=6, minute=0, second=0)
    delta = tomorrow - rounder(current_time)
    return int(delta.total_seconds() // 3600 / 3)


def get_4_day_index() -> dict:
    current_time = datetime.now()
    today = datetime.now().date()
    day = today.day
    month = today.month
    year = today.year
    
    first = datetime(year=year, month=month, day=day+1, hour=12, minute=0, second=0)
    second = datetime(year=year, month=month, day=day+2, hour=12, minute=0, second=0)
    third = datetime(year=year, month=month, day=day+3, hour=12, minute=0, second=0)
    fourth = datetime(year=year, month=month, day=day+4, hour=12, minute=0, second=0)
    
    delta_1 = first - rounder(current_time)
    delta_2 = second - rounder(current_time)
    delta_3 = third - rounder(current_time)
    delta_4 = fourth - rounder(current_time)
    
    index_1 = int(delta_1.total_seconds() // 3600 / 3)
    index_2 = int(delta_2.total_seconds() // 3600 / 3)
    index_3 = int(delta_3.total_seconds() // 3600 / 3)
    index_4 = int(delta_4.total_seconds() // 3600 / 3)
    
    return {
        first.date().day: index_1,
        second.date().day: index_2,
        third.date().day: index_3,
        fourth.date().day: index_4
    }
    

def get_week_dates() -> dict:
    current_time = datetime.now()
    today = datetime.now().date()
    day = today.day
    month = today.month
    year = today.year
    
    first = datetime(year=year, month=month, day=day+1, hour=12, minute=0, second=0)
    second = datetime(year=year, month=month, day=day+2, hour=12, minute=0, second=0)
    third = datetime(year=year, month=month, day=day+3, hour=12, minute=0, second=0)
    fourth = datetime(year=year, month=month, day=day+4, hour=12, minute=0, second=0)
    
    return {
        1: first.date().day,
        2: second.date().day,
        3: third.date().day,
        4: fourth.date().day
    }


def weather_4_days() -> dict:
    weather = {}
    indexes = get_4_day_index()
    for date, index in indexes.items():
        pass