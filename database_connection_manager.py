import asyncio

from logger import Logger
import os
import mysql.connector
from dotenv import load_dotenv

class DatabaseConnectionManager:
    def __init__(self, logger: Logger):
        self.__lock = asyncio.Lock()
        self.__logger = logger
        load_dotenv()
        self.__WRITE_CREDENTIALS_DICT = {
            'user': os.getenv('DB_USER'),
            'host': os.getenv('DB_HOST'),
            'passwd': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME')
        }

    def __enter__(self):
        # Connecting from the server
        self.__logger.get_logger().info("Connecting to DB...")
        self.__conn = mysql.connector.connect(**self.__WRITE_CREDENTIALS_DICT)
        self.__cursorObject = self.__conn.cursor(dictionary=True)
        self.__logger.get_logger().info("Connected to DB")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # Rollback the transaction if there was an error and print it
        if exc_type is mysql.connector.Error or exc_value is not None:
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

    async def execute_async_write_with_commit(self, query, values=None):
        async with self.__lock:
            await asyncio.to_thread(self.execute_write_with_commit, query, values)

    async def execute_async_read(self, query, values=None):
        async with self.__lock:
            return await asyncio.to_thread(self.execute_read, query, values)

    def execute_read(self, query, values=None):
        self.__logger.get_logger().info("Executing Read Query: %r, %r", query, values)
        self.__cursorObject.execute(query, values)
        return self.__cursorObject.fetchall()

    def commit(self):
        self.__conn.commit()