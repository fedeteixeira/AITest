import asyncio
import os
from dotenv import load_dotenv

from controllers.sql_agent import SQLAgent
from logger import Logger
from seeders.db_seeder import DbSeeder


def run_seeder_if_requested():
    seed_db = os.getenv("SEED_DB", "false").lower() in ("true", "1", "yes")
    if seed_db:
        print("Seeding database...")
        db_seeder = DbSeeder()
        db_seeder.seed_tables()
        db_seeder.seed_users()
        db_seeder.seed_notes()
        print("Database seeded successfully.")


def main():
    load_dotenv()
    run_seeder_if_requested()
    agent = SQLAgent(Logger("Agent"))
    asyncio.run(agent.main())


if __name__ == "__main__":
    main()