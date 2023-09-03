import csv
import sqlite3

# Соединение с базой данных
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

cursor.execute("DELETE FROM sqlite_sequence WHERE name='recipes_ingredients'")
cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('recipes_ingredients', 0)")

# Открываем CSV файл
with open('ingredients.csv', 'r', encoding='utf8') as file:
    reader = csv.DictReader(file)

    # Читаем данные из CSV файла и записываем их в базу данных
    for row in reader:
        name = row['name']
        unit = row['unit']

        # Вставляем данные в таблицу recipes_ingredients
        cursor.execute("INSERT INTO recipes_ingredients (name, unit) VALUES (?, ?)", (name, unit))

# Сохраняем изменения и закрываем соединение с базой данных
conn.commit()
conn.close()
