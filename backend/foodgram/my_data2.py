import csv
import psycopg2
import os

host = os.getenv("DB_HOST")
database = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
port = os.getenv("DB_PORT")

# Подключение к базе данных
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    port=port
)
cursor = conn.cursor()

cursor.execute("TRUNCATE TABLE ingredients RESTART IDENTITY")

# Открываем CSV файл
with open('ingredients.csv', 'r', encoding='utf8') as file:
    reader = csv.DictReader(file)

    # Читаем данные из CSV файла и записываем их в базу данных
    for row in reader:
        name = row['name']
        measurement_unit = row['unit']

        # Вставляем данные в таблицу ingredients
        cursor.execute("INSERT INTO ingredients (name, measurement_unit) VALUES (%s, %s)", (name, measurement_unit))

# Сохраняем изменения и закрываем соединение с базой данных
conn.commit()
conn.close()
