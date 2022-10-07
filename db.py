import sqlite3
import os.path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db.db")

class BotDB:

    def __init__(self):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ? AND `join_date` BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime')", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]
    
    def get_user_date(self, user_id):
        """ Достаем дату покупки подписки """

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()
    
    def delete_user(self,user_id):
        """Удаляем юзера из бд"""
        self.cursor.execute("DELETE FROM `users` WHERE `user_id` = ?", (user_id,))
    

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()