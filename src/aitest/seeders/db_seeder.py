from faker import Faker

from aitest.database_connection_manager import DatabaseConnectionManager

class DbSeeder:
    def __init__(self, db: DatabaseConnectionManager):
        self.__USERS_TABLE = "users"
        self.__NOTES_TABLE = "notes"
        self.__fake = Faker()
        self.__db = db

    def ensure_tables_exist(self):
        self.__db.execute_write_with_commit(f"CREATE TABLE IF NOT EXISTS {self.__USERS_TABLE} (id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255))")
        self.__db.execute_write_with_commit(f"CREATE TABLE IF NOT EXISTS {self.__NOTES_TABLE} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), contents TEXT, user_id INT, FOREIGN KEY (user_id) REFERENCES {self.__USERS_TABLE}(id) ON DELETE CASCADE)")  # noqa: E501
        users = self.__db.execute_read(f"SELECT id FROM {self.__USERS_TABLE} LIMIT 1")
        if not users:
            self.__db.execute_write_with_commit(f"INSERT INTO {self.__USERS_TABLE} (id, first_name, last_name) VALUES (1, 'Default', 'User')")

    def seed_tables(self):
        self.__db.execute_write_with_commit(f"DROP TABLE IF EXISTS {self.__NOTES_TABLE}")
        self.__db.execute_write_with_commit(f"DROP TABLE IF EXISTS {self.__USERS_TABLE}")
        self.ensure_tables_exist()

    def seed_users(self):
        values = []
        for n in range(10):
            values.append((self.__fake.first_name(), self.__fake.last_name()))
        query = f"INSERT INTO {self.__USERS_TABLE} (first_name, last_name) VALUES (%s, %s)"
        self.__db.execute_batch_write(query, values, True)

    def seed_notes(self):
        query = f"SELECT * FROM {self.__USERS_TABLE}"
        user_rows = self.__db.execute_read(query)
        user_ids = [userRow['id'] for userRow in user_rows]
        values = []

        # Each user is seeded with at least 5 notes
        for user_id in user_ids:
            for _ in range(5):
                values.append((self.__fake.text(max_nb_chars=30), self.__fake.text(), user_id))
        query = f"INSERT INTO {self.__NOTES_TABLE} (name, contents, user_id) VALUES (%s, %s, %s)"
        self.__db.execute_batch_write(query, values, True)
