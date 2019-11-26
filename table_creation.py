import sqlite3

conn = sqlite3.connect("usersbase.db")
cursor = conn.cursor()


def create():
                # Создание таблицы  логин, почта, ФИО
    cursor.execute("""CREATE TABLE users
					  (name text, email text, password text)
				   """)

    # заполнение таблицы
    cursor.execute("""INSERT INTO users
					  VALUES ('Jack', 'test@mail.ru', '12345'),
					  ('Walter', 'rwerwer@mail.ru', 'rtf344'),
					  ('Clyde', 'hgfhgft@mail.ru', 'qwerty12345'),
					  ('Quentin', 'uytht@mail.ru', 'rewf234rfds'),
					  ('Mark', 'rvcbt@mail.ru', 'rwef234'),
					  ('Joseph', 'jhgjgt@mail.ru', 'vbv343'),
					  ('Curtis', 'uytht@mail.ru', '1243e324'),
					  ('Clifton', 'jbghf@mail.ru', 'vbvsf324'),
					  ('Robert', 'tygyt@mail.ru', 'vsser234')
					  """)

    # Сохранить изменения
    conn.commit()


try:
    create()
except sqlite3.OperationalError:
    print('Таблица уже создана!')


def clear():
    cursor.execute("""DELETE FROM users
					WHERE login = "werwer";""")
    conn.commit()


cursor.close()
