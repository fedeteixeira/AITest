import asyncio
import os
from dotenv import load_dotenv

from controllers.sql_agent import EvaluationDependencies, SQLAgent, SqlAgentDependencies
from database_connection_manager import DatabaseConnectionManager
from logger import Logger
from seeders.db_seeder import DbSeeder
from services.notes_service import NotesService
from services.user_service import UserService
from views.cli import CLI


def run_seeder_if_requested():
    seed_db = os.getenv("SEED_DB", "false").lower() in ("true", "1", "yes")
    if seed_db:
        print("Seeding database...")
        db_seeder = DbSeeder()
        db_seeder.seed_tables()
        db_seeder.seed_users()
        db_seeder.seed_notes()
        print("Database seeded successfully.")


async def main():
    user_id = 1
    load_dotenv()
    run_seeder_if_requested()
    sql_agent = SQLAgent(Logger("Agent"))
    with DatabaseConnectionManager(Logger("AgentQueries")) as db:
        user_service = UserService(db)
        notes_service = NotesService(db)
        db_context = {
            "users": await user_service.get_user_table_describe(),
            "notes": await notes_service.get_notes_table_describe()
        }
        user_object = await user_service.get_user_by_id(user_id)
        if not user_object:
            raise Exception(f"User with id {user_id} not found in the database")
        evaluation_dependencies = EvaluationDependencies(user_id=user_id)
        sql_agent_dependencies = SqlAgentDependencies(
            db=db,
            user_id=user_id,
            db_context=db_context,
            user_name=user_object.get_full_name(),
            evaluation_dependencies=evaluation_dependencies,
            user_service = user_service,
            notes_service = notes_service
        )
        cli = CLI(sql_agent_dependencies=sql_agent_dependencies, sql_agent=sql_agent)
        await cli.main()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")