from database_connection_manager import DatabaseConnectionManager

class NotesService:
    def __init__(self, db:DatabaseConnectionManager):
        self.__db = db

    async def get_notes_table_describe(self):
        return await self.__db.execute_async_read("DESCRIBE notes")

    async def get_user_notes_by_id(self, id):
        return await self.__db.execute_async_read("SELECT * from notes as n where n.user_id = %s", (id, ))

    async def create_user_notes_by_id(self, user_id, note_name, note_contents):
        return await self.__db.execute_async_write_with_commit("INSERT INTO notes (user_id, name, contents) VALUES (%s, %s, %s)", (user_id, note_name, note_contents))

