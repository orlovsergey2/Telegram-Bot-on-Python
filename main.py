import sqlite3

import requests
import telebot
from bs4 import BeautifulSoup
from keyboa import Keyboa
from telebot import types

bot = telebot.TeleBot('6924373299:AAEwaPfpRY7dSM5hjfLGMIV6G7XOEfOxIOc', skip_pending=True)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = ['Факультеты', 'ВУЗ и объединения']
    btn2 = ['Навигатор', "Студенту"]
    btn3 = ["СибАДИ на Stepik", "Новости"]
    btn4 = "Ведомость"
    markup.add(*btn)
    markup.add(*btn2)
    markup.add(*btn3)
    markup.add(btn4)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def get_user_text(message):
    if message.text == "ВУЗ и объединения":
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("СибАДИ ВК", url="https://vk.com/sibadilife")
        btn2 = types.InlineKeyboardButton('Сайт СибАДИ', url="https://sibadi.org/")
        btn3 = types.InlineKeyboardButton("Профком", url="https://vk.com/profkomsibadi")
        markup.row(btn1, btn2, btn3)
        bot.send_message(message.chat.id, "Выберите ВУЗ или объединение:", reply_markup=markup)
        start(message)
    elif message.text == "Навигатор":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        body = ["Корпус 1", "Корпус 2", "Корпус 3", "Корпус 4", "Корпус П", "Назад"]
        markup.add(*body)
        bot.send_message(message.chat.id, "Выберите корпус:", reply_markup=markup)
        bot.register_next_step_handler(message, callback_message)
    elif message.text == 'Факультеты':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = ['ИСЭиУ', 'АДПГС', 'АТНиСТ', "Назад"]
        markup.add(*btn)
        bot.send_message(message.chat.id, "Выберите факультет: ", reply_markup=markup)
        bot.register_next_step_handler(message, facult)
    elif message.text == 'Студенту':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = ['Портфолио', 'Библиотека', 'Портал']
        btn1 = ["Подразделения СибАДИ", "Информация о факультетах и кафедрах"]
        btn2 = ["Телефонная книжка", "Назад"]
        markup.add(*btn)
        markup.add(*btn1)
        markup.add(*btn2)
        bot.send_message(message.chat.id, "Выберите факультет: ", reply_markup=markup)
        bot.register_next_step_handler(message, student)
    elif message.text == "СибАДИ на Stepik":
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Основы строительного черчения. AutoCAD",
                                          url='https://stepik.org/course/75211/promo')
        btn2 = types.InlineKeyboardButton('Диагностирование и ремонт силовых агрегатов транспортных средств',
                                          url='https://stepik.org/course/10091/promo')
        btn3 = types.InlineKeyboardButton("Основы строительного черчения. NanoCAD",
                                          url='https://stepik.org/course/182335/promo')
        items = [[btn1], [btn2], [btn3]]
        kb = Keyboa(items).keyboard
        start(message)
        bot.send_message(message.chat.id, "Курсы:", reply_markup=kb)
    elif message.text == "Новости":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = ['1', '2', '3', "4", 'Назад']
        markup.add(*btn)
        bot.send_message(message.chat.id, "Выберите страницу новостей из сайта СибАДИ: ", reply_markup=markup)
        bot.register_next_step_handler(message, news)
    elif message.text == "Ведомость":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = ['ИСЭиУ', 'АДПГС', 'АТНиСТ', "Назад"]
        markup.add(*btn)
        bot.send_message(message.chat.id, "Выберите факультет: ", reply_markup=markup)
        bot.register_next_step_handler(message, vedomost)
    elif message.text == "Назад":
        start(message)
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю")
    delete_previous_messages(message)

@bot.message_handler(func=lambda message: True)
def vedomost(message):
    if message.text == "ИСЭиУ":
        show_courses_menu(message, courseISU)
    elif message.text == "АДПГС":
        show_courses_menu(message, courseADPGS)
    elif message.text == "АТНиСТ":
        show_courses_menu(message, courseATNiST)
    elif message.text == "Назад":
        start(message)

def show_courses_menu(message, course_function):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = ['курс 1', 'курс 2', 'курс 3', 'курс 4', 'курс 5']
    back = types.KeyboardButton("Назад")
    markup.add(*btn, back)
    bot.send_message(message.chat.id, "Выберите курс: ", reply_markup=markup)
    delete_previous_messages(message)
    def on_groups_select(message):
        if message.text == 'Назад':
            start(message)
            delete_previous_messages(message)
        else:
            course_function(message)
    bot.register_next_step_handler(message, on_groups_select)

@bot.message_handler(func=lambda message: True)
def courseATNiST(message):
    global curs
    if message.text in ['курс 1', 'курс 2', 'курс 3', 'курс 4', 'курс 5', 'Назад']:
        curs = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if message.text == 'курс 1':
            show_groups_menu(message, course1,  [
                'АПб-23Т1', 'АТб-23Т1', 'АТб-23Т2', 'АТТ-23Т1',
                'ГСУб-23Т1', 'ДНГб-23Т1', 'НСб-23Т1', 'ОДб-23Т1',
                'ПОб-23Т1', 'ПТС-23Т1', 'ПТС-23Т2', 'ТЛб-23Т1'
            ])
        if message.text == 'курс 2':
            show_groups_menu(message, course1, [
                'АТб-22Т1', 'АТб-22Т2', 'АТТ-22Т1', 'АТТ-22Т2',
                'БПб-22С1', 'ЗОСб-22С1', 'НСб-22Т1', 'ОДб-22Т1',
                'ПОб-22Т1', 'ПТС-22Т1', 'ПТС-22Т2', 'ТЛб-22Т1',
                'ЭУб-22Т1'
            ])
        if message.text == 'курс 3':
            show_groups_menu(message, course1, [
                'АТб-21Т1', 'АТТ-21Т1', 'БПб-21С1', 'ЗОСб-21С1',
                'НСб-21Т1', 'ОДб-21Т1', 'ПОб-21Т1', 'ПТС-21Т1',
                'ПТС-21Т2', 'ТЛб-21Т1'
            ])
        if message.text == 'курс 4':
            show_groups_menu(message, course1, [
                'АПб-20Т1', 'АТб-20Т1', 'АТТ-20Т1', 'ЗОСб-20С1',
                "ОДб-20Т1", 'ПТС-20Т1', 'СМб-20Т1', "ТЛб-20Т1",
                'ЭУб-20Т1'
            ])
        if message.text == 'курс 5':
            show_groups_menu(message, course1, ['АТТ-19Т1', 'ПТС-19Т1'])
    elif message.text == "Назад":
        start(message)
@bot.message_handler(func=lambda message: True)
def courseADPGS(message):
    global curs
    if message.text in ['курс 1', 'курс 2', 'курс 3', 'курс 4', 'курс 5', 'Назад']:
        curs = message.text
        if message.text == 'курс 1':
            show_groups_menu(message, course1, [
                'АДб-23С1', 'АДб-23С2', 'АДб-23СZ1', 'АДб-23СZ2',
                'АРХб-23С1', 'АРХб-23С2', 'ИДб-23С1', 'МТб-23С1',
                'ПГСб-23С1', 'ПГСб-23С2', 'ПГСб-23СZ1', 'ПГСб-23СZ2',
                'ПГСб-23СZ3', 'ПГСб-23СZ4', 'СУЗ-23С1', 'СЭМ-23С1', 'ТГВб-23С1'
            ])
        elif message.text == 'курс 2':
            show_groups_menu(message, course1, [
                'АДб-22С1', 'АДб-22С2', 'АДб-22СZ1', 'АДб-22СZ2',
                'АРХб-22С1', 'ГЕОб-22С1', 'ИДб-22С1', 'МТб-22С1',
                'ПГСб-22С1', 'ПГСб-22С2', 'ПГСб-22СZ1', 'ПГСб-22СZ2',
                'ПГСб-22СZ3', 'СУЗ-22С1', 'СЭМ-22С1', 'ТГВб-22С1'
            ])
        elif message.text == 'курс 3':
            show_groups_menu(message, course1,[
                'АДб-21С1', 'АРХб-21С1', 'ИДб-21С1', 'ИСб-21С1',
                'МТб-21С1', 'ПГСб-21С1', 'ПГСб-21С2', 'СЭМ-21С1'
            ])
        elif message.text == 'курс 4':
            show_groups_menu(message, course1,[
                'АДб-20С1', 'АРХб-20С1', 'ГЕОб-20С1', 'ИДб-20С1',
                "ИСб-20С1", 'МТб-20С1', 'ПГСб-20С1', "ПГСб-20С2",
                'СУЗ-20С1', 'СЭМ-20С1'
            ])
        elif message.text == 'курс 5':
            show_groups_menu(message, course1, ['АРХб-19С1', 'СУЗ-19С1', 'СЭМ-19С1'])
        elif message.text == "Назад":
            start(message)
@bot.message_handler(func=lambda message: True)
def courseISU(message):
    global curs
    if message.text in ['курс 1', 'курс 2', 'курс 3', 'курс 4', 'курс 5', 'Назад']:
        curs = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if message.text == 'курс 1':
            show_groups_menu(message, course1,[
                'АСб-23Э1', 'АСб-23Э2', 'БИ-23Э1', 'БИб-23Э1',
                'БИб-23ЭZ1', 'ЛОГб-23ЭZ1', 'ПИб-23Э1', 'Эб-23ЭZ1'
            ])
        if message.text == 'курс 2':
            show_groups_menu(message, course1, [
                'АСб-22Э1', 'АСб-22Э2', 'БИ-22Э1', 'БИб-22Э1',
                'БИб-22ЭZ1', 'ЛОГб-22ЭZ1', 'ПИб-22Э1', 'Эб-22ЭZ1','ЦЭб-22Э1'
            ])
        if message.text == 'курс 3':
            show_groups_menu(message, course1, [
                'АСб-21Э1', 'БИ-21Э1', 'БИб-21Э1', 'БИб-21ЭZ1',
                'ЛОГб-21ЭZ1', 'ЛОГб-21Э1', 'ПИб-21Э1', 'Эб-21ЭZ1', 'ЦЭб-21Э1'
            ])
        if message.text == 'курс 4':
            show_groups_menu(message, course1, [
                'АСб-20Э1', 'БИ-20Э1', 'БИб-20Э1', 'БИб-20ЭZ1',
                "БИб-20ЭZ2", 'ЛОГб-20Э1', 'ПИб-20Э1', "ПИб-20Э2",
                'Эб-20Э1', 'УКб-20Э1'
            ])
        if message.text == 'курс 5':
            show_groups_menu(message, course1, ['БИ-19Э1'])
    elif message.text == "Назад":
        show_groups_menu(message)

def show_groups_menu(message, next_function, groups):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = groups
    back = types.KeyboardButton("Назад")
    markup.add(*btn, back)
    bot.send_message(message.chat.id, "Выберите группу: ", reply_markup=markup)
    def on_groups_select(message):
        if message.text == 'Назад':
            start(message)
        else:
            next_function(message)

    #delete_previous_messages(message)
    bot.register_next_step_handler(message, on_groups_select)

@bot.message_handler(func=lambda message: True)
def course1(message):
    conn = sqlite3.connect('groups.db')
    cursor = conn.cursor()
    cursor.execute("SELECT GroupName, GroupID FROM Groups")
    rows = cursor.fetchall()
    url_dict = {row[0]: row[1] for row in rows}
    conn.close()
    if message.text in url_dict:
        url = f"https://umu.sibadi.org/Ved/?group={url_dict[message.text]}"
        vedomost1(url, message, url_dict)
@bot.message_handler(func=lambda message: True)
def vedomost1(url, message, url_dict):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='dxgvControl_MaterialCompact infoTable dxgv')
    data_rows = None  # Инициализируем переменную data_rows
    if table:
        data_rows = soup.find_all('tr')  # Находим все строки таблицы
        # Создаем сообщение с данными
        message_text = ""
        for row in data_rows:
            cells = row.find_all('td')  # Находим все ячейки в строке
            if len(cells) == 3:  # Проверяем, что у нас есть три ячейки
                discipline = cells[0].text.strip()  # Извлекаем название дисциплины
                exam_type = cells[1].text.strip()  # Извлекаем тип экзамена
                closed = cells[2].text.strip()  # Извлекаем статус "Закрыто"
                message_text += f"Дисциплина: {discipline}, Тип экзамена: {exam_type}, Закрыто: {closed}\n"
        bot.send_message(message.chat.id, message_text)
    else:
        print("Таблица не найдена")
    start(message)
    delete_previous_messages(message)

@bot.message_handler(func=lambda message: True)
def info(message):
    if message.text == "Информация о факультетах":
        desk = {'id': 'tableSibadiInstitute'}
        infoFacult(desk, message)
    elif message.text == "Информация о кафедрах":
        desk = {'id': 'tableSibadi'}
        infoCathedra(desk, message)
    elif message.text == "Назад":
        start(message)
        delete_previous_messages(message)
def infoFacult(desk, message):
    url = "https://sibadi.org/about/faculties/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', desk)
    data_rows = None
    if table:
        data_rows = soup.find_all('tr')
        message_text = ""
        for row in data_rows:
            cells = row.find_all('td')
            if len(cells) == 5:
                institut = cells[0].text.strip()
                sokr = cells[1].text.strip()
                direktor = cells[2].text.strip()
                telefon = cells[3].text.strip()
                cabinet = cells[4].text.strip()
                message_text += f"{'-'*64}\nИнститут: {institut}\nСокращение: {sokr}\nДиректор: {direktor}\nТелефон: {telefon}\nКабинет: {cabinet}\n"
        bot.send_message(message.chat.id, message_text)
    else:
        print("Таблица не найдена")
    delete_previous_messages(message)
    start(message)
def infoCathedra(desk, message):
    url = "https://sibadi.org/about/faculties/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', desk)
    data_rows = None  # Инициализируем переменную data_rows
    if table:
        data_rows = soup.find_all('tr')  # Находим все строки таблицы
        message_text = ""
        for row in data_rows:
            cells = row.find_all('td')  # Находим все ячейки в строке
            if len(cells) == 6:  # Проверяем, что у нас есть три ячейки
                cathedra = cells[0].text.strip()  # Извлекаем название дисциплины
                sokr = cells[1].text.strip()  # Извлекаем тип экзамена
                zavCathedra = cells[2].text.strip()  # Извлекаем статус "Закрыто"
                telefon = cells[3].text.strip()
                cabinet = cells[4].text.strip()
                email = cells[5].text.strip()
                message_text += f"{'-'*64}\nКафеда: {cathedra}\nСокращение: {sokr}\nТелефон: {telefon}\nКабинет: {cabinet}\nemail: {email}\n"
                max_message_length = 4096  # Определяем максимальную длину сообщения в символах
                message_parts = [message_text[i:i + max_message_length] for i in
                                 range(0, len(message_text), max_message_length)]  # Разбиваем текст на части
                for part in message_parts:  # Отправляем каждую часть текста как отдельное сообщение
                    bot.send_message(message.chat.id, part)
    else:
        print("Таблица не найдена")
    start(message)
    delete_previous_messages(message)

@bot.message_handler(func=lambda message: True)
def student(message):
    if message.text == "Библиотека":
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Библиотека СибАДИ", url='https://lib.sibadi.org/')
        btn2 = types.InlineKeyboardButton('Юрайт', url='https://urait.ru/')
        btn3 = types.InlineKeyboardButton("Лань", url='https://e.lanbook.com/')
        items = [[btn1, btn2], [btn3]]
        kb = Keyboa(items).keyboard
        bot.send_message(message.chat.id, "Библиотека:", reply_markup=kb)
        start(message)
        delete_previous_messages(message)
    elif message.text == "Портфолио":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("Портфолио", url='https://portfolio.sibadi.org/login')
        markup.row(btn)
        bot.send_message(message.chat.id, "Портфолио", reply_markup=markup)
        start(message)
        delete_previous_messages(message)
    elif message.text == "Портал":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("Портал", url='https://portal.sibadi.org/')
        markup.row(btn)
        bot.send_message(message.chat.id, "Портал", reply_markup=markup)
        start(message)
        delete_previous_messages(message)
    elif message.text == "Подразделения СибАДИ":
        url = "https://sibadi.org/sveden/struct/"
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', class_='sibadiTable')
        message_text = ""
        data_rows = None
        if table:
            data_rows = table.find_all('tr')
            for row in data_rows:
                cells = row.find_all('td')
                if len(cells) == 7:
                    position = cells[0].text.strip()
                    full_name = cells[1].text.strip()
                    degrees = cells[2].text.strip()
                    department = cells[3].text.strip()
                    address = cells[4].text.strip()
                    phone = cells[5].text.strip()
                    email = cells[6].text.strip()

                    # Удаление лишних пробелов в данных
                    position = position.replace("Смотреть", "").strip()
                    full_name = full_name.replace("Смотреть", "").strip()
                    degrees = degrees.replace("Смотреть", "").strip()
                    department = department.replace("Смотреть", "").strip()
                    address = address.replace("Смотреть", "").strip()
                    phone = phone.replace("Смотреть", "").strip()
                    email = email.replace("Смотреть", "").strip()

                    message_text += f"{'-' * 64}\n{position}| {full_name}| {degrees}| {department}| {address}| {phone}| {email}\n"

            max_message_length = 4096  # Определяем максимальную длину сообщения в символах
            message_parts = [message_text[i:i + max_message_length] for i in
                             range(0, len(message_text), max_message_length)]  # Разбиваем текст на части
            for part in message_parts:  # Отправляем каждую часть текста как отдельное сообщение
                bot.send_message(message.chat.id, part)
        else:
            print("Таблица не найдена")
        start(message)
    elif message.text == "Информация о факультетах и кафедрах":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = ["Информация о факультетах", "Информация о кафедрах", "Назад"]
        markup.add(*btn)
        bot.send_message(message.chat.id, "Выберите действие: ", reply_markup=markup)
        bot.register_next_step_handler(message, info)
    elif message.text == "Телефонная книжка":
        url = "https://sibadi.org/guide/"
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', class_='main-table')
        data_rows = None  # Инициализируем переменную data_rows
        if table:
            data_rows = soup.find_all('tr')  # Находим все строки таблицы
            message_text = ""
            for row in data_rows:
                cells = row.find_all('td')  # Находим все ячейки в строке
                if len(cells) == 5:  # Проверяем, что у нас есть три ячейки
                    otdel = cells[0].text.strip()  # Извлекаем название дисциплины
                    sokr = cells[1].text.strip()  # Извлекаем тип экзамена
                    fio = cells[2].text.strip()  # Извлекаем статус "Закрыто"
                    telefon = cells[3].text.strip()
                    cabinet = cells[4].text.strip()

                    message_text += f"{'-'*64}\nОтдел: {otdel}\nСокращение: {sokr}\nФИО: {fio}\nТелефон: {telefon}\nКабинет: {cabinet}\n"
            max_message_length = 4096  # Определяем максимальную длину сообщения в символах
            message_parts = [message_text[i:i + max_message_length] for i in
                             range(0, len(message_text), max_message_length)]  # Разбиваем текст на части
            for part in message_parts:  # Отправляем каждую часть текста как отдельное сообщение
                bot.send_message(message.chat.id, part)
        else:
            print("Таблица не найдена")
        start(message)
    elif message.text == "Назад":
        start(message)
    delete_previous_messages(message)

@bot.message_handler(func=lambda message: True)
def news(message):
    if message.text == "1":
        url = "https://sibadi.org/news/"
        news1(url, message)
    elif message.text == '2':
        url = "https://sibadi.org/news/?PAGEN_1=2"
        news1(url, message)
    elif message.text == '3':
        url = "https://sibadi.org/news/?PAGEN_1=3"
        news1(url, message)
    elif message.text == "4":
        url = "https://sibadi.org/news/?PAGEN_1=4"
        news1(url, message)
    elif message.text == "Назад":
        start(message)
@bot.message_handler(func=lambda message: True)
def news1(url, message):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    news_elements = soup.find_all('div', class_='billet')
    message_text = ""
    for news in news_elements:
        news_title = news.find('p', class_='news-name').text
        message_text += f"{news_title}\n "
    bot.send_message(message.chat.id, message_text)
    start(message)
    delete_previous_messages(message)

@bot.message_handler(func=lambda message: True)
def facult(message):
    if message.text == "ИСЭиУ":
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Сообщество ИСЭИУ", url="https://vk.com/isu.sibadi")
        btn2 = types.InlineKeyboardButton("Ссылка на справку", url="https://vk.com/isu.sibadi?w=app5708398_-192767535")
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, "ИСЭиУ:", reply_markup=markup)
        start(message)
        delete_previous_messages(message)
    if message.text == 'АДПГС':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Сообщество АДПГС', url="https://vk.com/sibadi_nst")
        markup.row(btn1)
        bot.send_message(message.chat.id, "АДПГС:", reply_markup=markup)
        start(message)
        delete_previous_messages(message)
    if message.text == "АТНиСТ":
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Сообщество АТНиСТ:', url="https://vk.com/sibadi_nst")
        btn2 = types.InlineKeyboardButton('Заказать справку', url='https://vk.com/app5708398')
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, "АТНиСТ:", reply_markup=markup)
        start(message)
        delete_previous_messages(message)
    elif message.text == "Назад":
        start(message)
        delete_previous_messages(message)

@bot.message_handler(func=lambda message: True)
def callback_message(message):
    global current_building
    if message.text in ["Корпус 1", "Корпус 2", "Корпус 3", "Корпус 4", "Корпус П"]:
        current_building = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = []
        if current_building == "Корпус 1" or current_building == "Корпус 2":
            buttons = ["Этаж 0", "Этаж 1", "Этаж 2", "Этаж 3", "Этаж 4"]
        elif current_building == "Корпус 3":
            buttons = ["Этаж 0", "Этаж 1", "Этаж 2", "Этаж 3", "Этаж 4", "Этаж 5"]
        elif current_building == "Корпус 4":
            buttons = ["Этаж 1", "Этаж 2", "Этаж 3", "Этаж 4"]
        elif current_building == "Корпус П":
            buttons = ["Этаж 1", "Этаж 2"]
        back = types.KeyboardButton("Назад")
        markup.add(*buttons, back)
        bot.send_message(message.chat.id, "Выберите этаж:", reply_markup=markup)
        delete_previous_messages(message)
        bot.register_next_step_handler(message, floor)
    elif message.text == "Назад":
        start(message)
        delete_previous_messages(message)

@bot.message_handler(func=lambda message: True)
def floor(message):
    global current_building
    # current_building = ""
    global current_floor
    current_floor = ""
    if message.text in ["Этаж 0", "Этаж 1", "Этаж 2", "Этаж 3", "Этаж 4", "Этаж 5", "Назад"]:
        current_floor = message.text
        if message.text == "Назад":
            start(message)
            delete_previous_messages(message)
        else:
            if current_building == 'Корпус 1':
                photo = open(f"./body1 flor{message.text[-1:]}.png", 'rb')
                bot.send_photo(message.chat.id, photo)
                start(message)
            if current_building == 'Корпус 2':
                photo = open(f"./body2 flor{message.text[-1:]}.png", 'rb')
                bot.send_photo(message.chat.id, photo)
                start(message)
            if current_building == 'Корпус 3':
                photo = open(f"./body3 flor{message.text[-1:]}.png", 'rb')
                start(message)
            if current_building == 'Корпус 4':
                photo = open(f"./body4 flor{message.text[-1:]}.png", 'rb')
                bot.send_photo(message.chat.id, photo)
                start(message)
            if current_building == 'Корпус П':
                photo = open(f"./bodyP flor{message.text[-1:]}.png", 'rb')
                bot.send_photo(message.chat.id, photo)
                start(message)
            delete_previous_messages(message)
def delete_previous_messages(message):
    chat_id = message.chat.id
    message_id = message.message_id
    for _ in range(2):
        bot.delete_message(chat_id, message_id)
        message_id -= 1
bot.polling(none_stop=True)
