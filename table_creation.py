import sqlite3

conn = sqlite3.connect("usersbase.db")
cursor = conn.cursor()


def create():
    # Создание таблицы  логин, почта, ФИО
    cursor.execute("""CREATE TABLE users 
        (id INTEGER PRIMARY KEY NOT NULL,
        name varchar(64) NOT NULL,
        email varchar(64) NOT NULL, 
        password varchar(64) NOT NULL)""")

    # заполнение таблицы
    cursor.execute("""INSERT INTO users (id, name, email, password)
     VALUES ('1','Jack', 'test@mail.ru', '12345'),
            ('2','Walter', 'rwerwer@mail.ru', 'rtf344'),
            ('3','Clyde', 'hgfhgft@mail.ru', 'qwerty12345'),
            ('4','Quentin', 'uytht@mail.ru', 'rewf234rfds'),
            ('5','Mark', 'rvcbt@mail.ru', 'rwef234'),
            ('6','Joseph', 'jhgjgt@mail.ru', 'vbv343'),
            ('7','Curtis', 'uytht@mail.ru', '1243e324'),
            ('8','Clifton', 'jbghf@mail.ru', 'vbvsf324'),
            ('9','Robert', 'tygyt@mail.ru', 'vsser234')
    """)

    # Сохранить изменения
    conn.commit()


try:
    create()
except sqlite3.OperationalError:
    print('Таблица уже создана!')
finally:
    cursor.close()
