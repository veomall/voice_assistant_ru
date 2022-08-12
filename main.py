import speech_recognition
import webbrowser
from telethon import TelegramClient
from datetime import datetime
import os
import pyttsx3
import time
import pyautogui
import re
import psutil
from lib.sound import Sound


api_id = 16694872
api_hash = '98daacb8cb7d382f97c74306a5e942ff'

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

language = 'ru'
engine = pyttsx3.init()
engine.setProperty('rate', 200)     # скорость речи
engine.setProperty('volume', 1)

commands_dict = {
    'commands': {
        'create_task': ["создай задачу", "новая задача", "добавь в список дел", "добавь список дел", "заметка",
                        'добавь задачу', 'добавь заметку', "создай заметку"],
        'show_tasks': ["список дел", "покажи список дел", "мои задачи"],
        "clear_todo_list": ['очисти список дел', "очисти список", 'очисти заметики'],
        'play_music': ["включи музыку", "музыка"],
        'yandex_search': ['найди в интернете', "найди в сети", "найди в яндексе", "поиск"],
        'send_message': ['отправь сообщение', "напиши сообщение", "напиши"],
        'open_youtube': ["открой youtube", 'youtube'],
        'search_in_youtube': ["найди в youtube"],
        'current_time': ["который час", "сколько время", "который сейчас час", "текущее время"],
        'current_date': ["какой сегодня день", "какой сейчас день", "текущая дата"],
        'pc_shutdown': ["выключи компьютер"],
        'pc_reboot': ["перезагрузи компьютер"],
        'battery_status': ["заряд аккумулятора", "какой заряд аккумулятора", "состояние батареи", "заряд батареи"],
        'reduce_sound': ["уменьши звук", "потише"],
        'increase_sound': ["увеличь звук", "погромче"],
        'mute': ["выключи звук", "убери звук"],
        'speak': ["включи звук"],
        'set_volume': ["установи уровень звука", "измени уровень звука", "установи громкость"],
        'new_browser_tab': ["новая вкладка", "открой новую вкладку"],
        'new_browser_window': ["новое окно", "открой новое окно"],
        'new_incognito_window': ["анонимное окно", "открой анонимное окно"],
        'close_tab': ["закрой вкладку"],
        'close_window': ["закрой окно"],
    },
    'names': {
        '@ch1r1nk0v': ["зубков", "артур", "зубков артур", "артур зубков"],
        '@Ender8991': ["метельский", "андрей", "метельский андрей", "андрей метельский"],
        '@ene_gue': ["минец", "женя", "минец женя", "женя минец"],
        '@gauntether': ["денисюк", "артем", "денисюк артем", "артем денисюк"],
        1216036752: ["кошлатый", "кирилл", "кошлатый кирилл", "кирилл кошлатый"],
    },
    'programs': {
        'muck': ['mac', 'мак'],
        'scrcpy': ['screen copy', 'транслировать экран', "скрин копия"],
        'unity hub': ["юнити хаб"],
    }
}


def listen_command():
    # Возвращает прознесенную команду или "Повторите команду"
    # Говорите четко иначе фраза повторите команду может вызвать ошибку(не могу гарантировать правильность всех функций)
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
        return query
    except speech_recognition.UnknownValueError:
        return 'Повторите команду'


def voice_text(text_val):
    # Озвучка текста
    engine.say(text_val)
    engine.runAndWait()


def greeting():
    # Стартовое сообщение, можно написать что угодно
    return 'Привет!'


def create_task():
    # Создание заметки
    print('Что добавить?')
    voice_text('Что добавить?')
    query = listen_command()
    if query == "Повторите команду":
        return 'Не понял'
    with open('todo-list.txt', 'a') as file:
        file.write(f"{query}\n")
    return f'Задача {query} добавлена в список'


def show_tasks():
    # Озвучка заметок
    with open('todo-list.txt', 'r') as file:
        tasks = file.readlines()
    for task in tasks:
        if tasks.index(task) == len(tasks) - 1:
            print(task)
            voice_text(task)
        else:
            print(task, end='')
            voice_text(task)
    return 'Вот ваши задачи'


def clear_todo_list():
    # Очистка списка заметок
    f = open('todo-list.txt', 'w')
    f.close()
    return 'Список дел очищен'


def play_music():
    # Включение музыки
    webbrowser.open(f'https://music.yandex.by', new=1)
    time.sleep(3)
    pyautogui.moveTo(600, 550)
    pyautogui.click()
    return 'Играет Яндекс Музыка}'


def start_program(program):
    # Запуск программы которая есть на компьютере через поиск
    for k, v in commands_dict['programs'].items():
        if program in v:
            program = k
            break
    os.system(f'echo {program}|clip')
    pyautogui.press('win')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    return f'Запустил {program}'


def yandex_search():
    # Поиск в Яндекс
    print('Что найти?')
    voice_text('Что найти?')
    query = listen_command()
    words = query.split()
    search = '+'.join(words)
    webbrowser.open(f'https://yandex.ru/search/?clid=1882628&text={search}&l10n=ru&lr=21392', new=2)
    return f'Ищу {query} в Яндексе'


def send_message():
    # Отправка сообщений
    print("Кому написать?")
    voice_text("Кому написать?")
    name = listen_command()
    user = ''
    for k, v in commands_dict['names'].items():
        if name in v:
            user = k
            break
    print("Что написать?")
    voice_text("Что написать?")
    message = listen_command()
    with TelegramClient('anon', api_id, api_hash) as client:
        try:
            client.loop.run_until_complete(client.send_message(user, message))
        except:
            print(user, message)
    return f'Написал {message} пользователю {name}'


def open_youtube():
    # Открытие Youtube
    webbrowser.open('https://www.youtube.com', new=2)
    return 'Открыл Youtube'


def search_in_youtube():
    # Поиск в Youtube
    print('Что найти?')
    voice_text('Что найти?')
    query = listen_command()
    words = query.split()
    search = '+'.join(words)
    webbrowser.open(f'https://www.youtube.com/results?search_query={search}', new=2)
    return f'Ищу {query} в Youtube'


def current_time():
    # Текущее время
    now = datetime.now()

    if now.hour % 10 == 1:
        hour_case = 'час'
    elif 2 <= now.hour % 10 <= 4 and now.hour // 10 != 1:
        hour_case = 'часа'
    else:
        hour_case = 'часов'

    if now.minute % 10 == 1:
        minute_case = 'минута'
    elif 2 <= now.minute % 10 <= 4 and now.minute // 10 != 1:
        minute_case = 'минуты'
    else:
        minute_case = 'минут'

    return f"{now.hour} {hour_case} {now.minute} {minute_case}"


def current_date():
    # Текущая дата
    now = datetime.now()
    return f'{now.day}.{now.month}.{now.year}'


def pc_reboot():
    # Перезагрузка компьютера
    os.system('shutdown -r -t 3')
    return 'Перезагружаю'


def pc_shutdown():
    # Выключение компьютера
    os.system("shutdown /s /t 3")
    return 'Выключаю'


def battery_status():
    # Заряд батареи
    battery = psutil.sensors_battery()
    percent = int(battery.percent)
    return f'Заряд аккумулятора {percent}%'


def reduce_sound():
    # Уменьшение звука
    Sound.volume_down()
    return f"Уровень звука {Sound.current_volume()}"


def increase_sound():
    # Увеличение звука
    Sound.volume_up()
    return f"Уровень звука {Sound.current_volume()}"


def mute():
    # Режим без звука
    Sound.mute()
    return ''


def speak():
    # Включение звука
    Sound.volume_set(20)
    return 'Уровень звука 20'


def set_volume():
    # Установить конкретный уровень звука
    print('Какой уровень громкости установить?')
    voice_text('Какой уровень громкости установить?')
    volume = int(listen_command())
    Sound.volume_set(volume)
    return f'Установлен уровень громкости {volume}'


def new_browser_tab():
    # Новая вкладка браузера
    pyautogui.hotkey('ctrl', 't')
    return 'Открыл новую вкладку'


def new_browser_window():
    # Новое окно браузера
    pyautogui.hotkey('ctrl', 'n')
    return 'Открыл новое окно'


def new_incognito_window():
    # Новое анонимное окно
    pyautogui.hotkey('ctrl', 'shift', 'n')
    return 'Открыл новое анонимное окно'


def close_tab():
    # Закрытие вкладки
    pyautogui.hotkey('ctrl', 'w')
    return 'Закрыл вкладку'


def close_window():
    # Закрытие приложения(любого)
    pyautogui.hotkey('alt', 'f4')
    return 'Закрыл окно'


def main():
    print(greeting())
    voice_text(greeting())
    while True:
        query = listen_command()
        if query == 'привет алекс' or query == "алекс":
            while True:
                print("Что сделать?")
                voice_text("Что сделать?")
                query = listen_command()
                print(query)
                for k, v in commands_dict['commands'].items():
                    if query in v:
                        command_text = globals()[k]()
                        print(command_text)
                        voice_text(command_text)
                        break
                else:
                    if re.match("запусти", query) is not None:
                        if re.match("запустить", query) is not None:
                            print(start_program(query[10:]))
                        else:
                            print(start_program(query[8:]))
                    elif re.match("открой", query) is not None:
                        print(start_program(query[7:]))
                print("Что-нибудь еще?")
                voice_text("Что-нибудь еще?")
                query = listen_command()
                if query == "да":
                    continue
                else:
                    print('Пока')
                    voice_text('Пока')
                    break
        elif query == 'выключись':
            raise SystemExit(1)


if __name__ == '__main__':
    main()
