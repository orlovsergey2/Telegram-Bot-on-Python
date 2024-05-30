import sqlite3
import requests

# Получаем данные с API
url = "https://umu.sibadi.org/api/raspGrouplist?year=2023-2024"
response = requests.get(url)
data = response.json()

# Подключаемся к базе данных SQLite
conn = sqlite3.connect('groups.db')
cursor = conn.cursor()
# Удаляем таблицу, если она уже существует
cursor.execute('''DROP TABLE IF EXISTS Groups''')
# Создаем таблицу для хранения информации о группах с правильной структурой
cursor.execute('''CREATE TABLE IF NOT EXISTS Groups (
                    GroupID INTEGER PRIMARY KEY,
                    GroupName TEXT,
                    Kurs INTEGER,
                    Facul TEXT,
                    YearName TEXT,
                    FacultyID INTEGER
                )''')
# Добавляем данные о группах в базу данных
for group in data['data']:
    cursor.execute("INSERT INTO Groups (GroupID, GroupName, Kurs, Facul, YearName, FacultyID) VALUES (?, ?, ?, ?, ?, ?)",
                    (group['id'], group['name'], group['kurs'], group['facul'], group['yearName'], group['facultyID']))
# Сохраняем изменения и закрываем соединение с базой данных SQLite
conn.commit()
conn.close()
