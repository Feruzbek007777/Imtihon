import sqlite3

class Database:
    def __init__(self, db_name: str = 'main.db'):
        self.database = db_name

    def execute(self, sql, *args, commit: bool = False, fetchone: bool = False, fetchall: bool = False):
        with sqlite3.connect(self.database) as db:
            cursor = db.cursor()
            cursor.execute(sql, args)

            result = None
            if fetchone:
                result = cursor.fetchone()
            elif fetchall:
                result = cursor.fetchall()

            if commit:
                db.commit()

        return result

    def create_table_books(self):
        sql = '''CREATE TABLE IF NOT EXISTS books(
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_name TEXT
        )'''
        self.execute(sql, commit=True)

    def insert_books(self, book_name):
        sql = '''INSERT INTO books(book_name) VALUES (?)'''
        self.execute(sql, book_name, commit=True)

    def select_books(self):
        sql = "SELECT * FROM books"
        return self.execute(sql, fetchall=True)

    def create_table_info(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS book_info(
            info_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            info_text TEXT
        )
        '''
        self.execute(sql, commit=True)

    def insert_book_info(self, book_id, info_text):
        sql = '''INSERT INTO book_info(book_id, info_text) VALUES (?, ?)'''
        self.execute(sql, book_id, info_text, commit=True)

    def select_books_info(self, book_id):
        sql = "SELECT info_id, info_text FROM book_info WHERE book_id = ?"
        return self.execute(sql, book_id, fetchall=True)

    def update_book_info(self, info_id, new_text):
        sql = '''UPDATE book_info SET info_text = ? WHERE info_id = ?'''
        self.execute(sql, new_text, info_id, commit=True)

    def delete_book_info(self, info_id):
        sql = '''DELETE FROM book_info WHERE info_id = ?'''
        self.execute(sql, info_id, commit=True)
