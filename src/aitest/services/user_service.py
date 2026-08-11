from aitest.database_connection_manager import DatabaseConnectionManager
from aitest.models.user import User

class UserService:
    def __init__(self, db:DatabaseConnectionManager):
        self.__db = db

    async def get_user_table_describe(self):
        return await self.__db.execute_async_read("DESCRIBE users")

    async def get_user_by_id(self, id):
        results = await self.__db.execute_async_read("SELECT u.first_name, u.last_name from users as u where u.id = %s", (id, ))
        if not results:
            return None
        return User(id=id, first_name=results[0]["first_name"], last_name=results[0]["last_name"])

