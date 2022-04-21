from alembic import command
from alembic.config import Config


class AlembicManager(Config):
    """Менеджер alembic"""

    def __init__(self, migrations_file_path: str, database_url: str):
        super().__init__()
        self.migrations_file_path = migrations_file_path
        self.database_url = database_url

    def migrate(self) -> None:
        """Метод для приминения миграций(аналог migrate Django)"""

        self.set_main_option('script_location', self.migrations_file_path)
        self.set_main_option('sqlalchemy.url', self.database_url)
        command.upgrade(self, 'head')
