import asyncio

import mysql.connector
from aitest.config import DbSettings
from aitest.logger import Logger

class DatabaseConnectionManager:
    def __init__(self, settings: DbSettings, logger: Logger):
        self.__logger = logger
        self.__POOL_CONFIGS = {
            'pool_name': "db_pool",
            'pool_size': 5
        }
        self.__WRITE_CREDENTIALS_DICT: dict[str] = {
            'user': settings.db_user,
            'host': settings.db_host,
            'passwd': settings.db_password,
            'database': settings.db_name,
        }

    def __enter__(self):
        # Connecting from the server
        self.__logger.get_logger().info("Connecting to DB...")
        self.__conn = mysql.connector.connect(**self.__POOL_CONFIGS, **self.__WRITE_CREDENTIALS_DICT)
        self.__cursorObject = self.__conn.cursor(dictionary=True)
        self.__logger.get_logger().info("Connected to DB")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # Rollback the transaction if there was an error and print it
        if (exc_type is not None and issubclass(exc_type, mysql.connector.Error)) or exc_value is not None:
            self.__logger.get_logger().error((exc_type, exc_value, exc_traceback))
            self.__logger.get_logger().error("Failed query: %s", exc_value)
            self.__conn.rollback()

        # Disconnecting the cursor
        self.__cursorObject.close()

        # Disconnecting from the server
        self.__conn.close()

    def execute_write(self, query, values=None):
        self.__logger.get_logger().info("Executing Write Query: %r, %r", query, values)
        self.__cursorObject.execute(query, values)

    def execute_write_with_commit(self, query, values=None):
        self.execute_write(query, values)
        self.__conn.commit()

    def execute_batch_write(self, query, values, commit=False):
        self.__cursorObject.executemany(query, values)
        if commit:
            self.__conn.commit()

    async def execute_async_write_with_commit(self, query, values=None):
        await asyncio.to_thread(self.execute_write_with_commit, query, values)

    async def execute_async_read(self, query, values=None):
        return await asyncio.to_thread(self.execute_read, query, values)

    def execute_read(self, query, values=None):
        self.__logger.get_logger().info("Executing Read Query: %r, %r", query, values)
        self.__cursorObject.execute(query, values)
        return self.__cursorObject.fetchall()

    def commit(self):
        self.__conn.commit()