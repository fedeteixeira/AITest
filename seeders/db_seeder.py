from database_connection_manager import DatabaseConnectionManager
from faker import Faker

from logger import Logger

class DbSeeder:
    def __init__(self):
        self.__USERS_TABLE = "users"
        self.__NOTES_TABLE = "notes"
        self.__fake = Faker()

    def seed_tables(self):
        with DatabaseConnectionManager(Logger("DbSeeder")) as db:
            db.execute_write(f"DROP TABLE IF EXISTS {self.__NOTES_TABLE}")
            db.execute_write(f"DROP TABLE IF EXISTS {self.__USERS_TABLE}")
            db.execute_write(f"CREATE TABLE IF NOT EXISTS {self.__USERS_TABLE} (id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255))")
            db.execute_write(f"CREATE TABLE IF NOT EXISTS {self.__NOTES_TABLE} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), contents TEXT, user_id INT, FOREIGN KEY (user_id) REFERENCES {self.__USERS_TABLE}(id) ON DELETE CASCADE)")  # noqa: E501

    def seed_users(self):
        with DatabaseConnectionManager(Logger("DbSeeder")) as db:
            for n in range(10):
                query = f"INSERT INTO {self.__USERS_TABLE} (first_name, last_name) VALUES (%s, %s)"
                values = (self.__fake.first_name(), self.__fake.last_name())

                db.execute_write(query, values)
            db.commit()

    def seed_notes(self):
        with DatabaseConnectionManager(Logger("DbSeeder")) as db:
            query = f"SELECT * FROM {self.__USERS_TABLE}"
            user_rows = db.execute_read(query)
            user_ids = [userRow['id'] for userRow in user_rows]

            for user_id in user_ids:
                # Each user is seeded with at least 5 notes
                for _ in range(5):
                    query = f"INSERT INTO {self.__NOTES_TABLE} (name, contents, user_id) VALUES (%s, %s, %s)"
                    values = (self.__fake.text(max_nb_chars=30), self.__fake.text(), user_id)
                    db.execute_write(query, values)
            db.commit()