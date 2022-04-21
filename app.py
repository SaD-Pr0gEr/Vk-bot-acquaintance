import sys

from config import USER_TOKEN, BOT_TOKEN, DATABASE_URL, BASE_DIR
from main_bot import User, ServerBot
from utils.db.dumpdata import dump_data, save_dump_data
from utils.managers.alembic_ import AlembicManager
from work_with_db_alchemy import initial_genders, initial_statuses, insert_into_country, initial_towns


def help_commands() -> None:
    """Список всех команд"""

    print("""
    Commands:
        alembic revision --autogenerate: For make migrations\n
        migrate(-mg): For run migrations\n
        dumpdata(-dp): For dump database data(file dump.json)\n
        initialdata(-ind): For insert starter data to database\n
        --help or help(-h): Commands list
    """)


def bot_runner() -> None:
    """Запуск бота"""

    try:
        print("Bot started")
        user = User()
        some_user = ServerBot(user, USER_TOKEN, BOT_TOKEN)
        some_user.talking()
    except KeyboardInterrupt:
        print("Bot stopped")


def run():
    alembic_manager = AlembicManager(str(BASE_DIR / "migrations"), DATABASE_URL)
    if not len(sys.argv) > 1:
        print("No command selected (--help to see command list)")
    elif sys.argv[1] == "migrate" or sys.argv[1] == "-mg":
        alembic_manager.migrate()
        print("Successful run migrations")
    elif sys.argv[1] == "dumpdata" or sys.argv[1] == "-dp":
        dump = dump_data()
        print(f"Successful dump data! File saved path: {save_dump_data(dump)}")
    elif sys.argv[1] == "initialdata" or sys.argv[1] == "-ind":
        initial_genders()
        initial_statuses()
        insert_into_country()
        initial_towns()
        print(f"Start data added for genders, user status and user country!")
    elif sys.argv[1] == "run":
        bot_runner()
    elif sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "help":
        help_commands()
    else:
        print("command not found")
    exit(0)


if __name__ == "__main__":
    run()
