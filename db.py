import sqlite3


conn = sqlite3.connect("users_info.db")
cursor = conn.cursor()


def add_chat_info(chat, user):
    chat_id = chat.chat_id
    token = chat.chat_token
    name = user.name
    phone = user.phone
    cursor.execute(f"INSERT INTO `chats`"
                   f"(`chat_id`, `token`,`u_name`, `u_phone`)"
                   f"VALUES (?, ?)",
                   (chat_id, token, name, phone))
    conn.commit()


def _init_db():
    """Инициализирует БД"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='users_info'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()

check_db_exists()