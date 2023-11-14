from cryptography.fernet import Fernet
import sqlite3
import getpass
import random
import string

# Генерація ключа для шифрування
def generate_key():
    return Fernet.generate_key()

# Ініціалізація шифрування за ключем
def initialize_cipher(key):
    return Fernet(key)

# Шифрування пароля
def encrypt_password(cipher, password):
    return cipher.encrypt(password.encode())

# Дешифрування пароля
def decrypt_password(cipher, encrypted_password):
    return cipher.decrypt(encrypted_password).decode()

# Створення таблиці паролів
def create_password_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL
        )
    ''')

# Додавання пароля
def add_password(cursor, cipher, service, username, password):
    encrypted_password = encrypt_password(cipher, password)
    cursor.execute('INSERT INTO passwords (service, username, encrypted_password) VALUES (?, ?, ?)', (service, username, encrypted_password))

# Генерація пароля різного рівня
def generate_password(level):
    if level == 1:
        return ''.join(random.choices(string.ascii_lowercase, k=8))
    elif level == 2:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    elif level == 3:
        return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
    elif level == 4:
        return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=16))
    elif level == 5:
        return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=20))

# Перегляд усіх паролів
def view_passwords(cursor, cipher):
    cursor.execute('SELECT * FROM passwords')
    passwords = cursor.fetchall()

    for password in passwords:
        decrypted_password = decrypt_password(cipher, password[3])
        print(f'ID: {password[0]}, Service: {password[1]}, Username: {password[2]}, Password: {decrypted_password}')

# Приклад виклику функцій
key = generate_key()
cipher = initialize_cipher(key)

conn = sqlite3.connect('password_manager.db')
cursor = conn.cursor()

create_password_table(cursor)

# Прикладові паролі різного рівня
example_passwords = [
    ('gmail', 'john.doe@gmail.com', generate_password(3)),
    ('facebook', 'john.doe', generate_password(4)),
    ('twitter', 'johndoe123', generate_password(5))
]

for example in example_passwords:
    add_password(cursor, cipher, *example)

view_passwords(cursor, cipher)

# Закриття з'єднання
conn.commit()
conn.close()
