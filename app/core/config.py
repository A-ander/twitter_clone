import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.host = os.environ["HOST"]
        self.port = int(os.environ["PORT"])
        self.db_host = os.environ["POSTGRES_HOST"]
        self.db_port = os.environ["POSTGRES_PORT"]
        self.db_name = os.environ["POSTGRES_NAME"]
        self.db_user = os.environ["POSTGRES_USER"]
        self.db_pass = os.environ["POSTGRES_PASSWORD"]
        self.db_url = (
            f"postgresql+asyncpg://{self.db_user}:"
            f"{self.db_pass}@{self.db_host}:"
            f"{self.db_port}/{self.db_name}"
        )


class DevSettings(Settings):
    DEBUG = True


class ProdSettings(Settings):
    DEBUG = False


class TestSettings(Settings):
    def __init__(self):
        super().__init__()
        self.db_host = os.environ["POSTGRES_HOST_TEST"]
        self.db_port = os.environ["POSTGRES_PORT_TEST"]
        self.db_name = os.environ["POSTGRES_NAME_TEST"]
        self.db_user = os.environ["POSTGRES_USER_TEST"]
        self.db_pass = os.environ["POSTGRES_PASSWORD_TEST"]
        self.db_url = (
            f"postgresql+asyncpg://{self.db_user}:"
            f"{self.db_pass}@{self.db_host}:"
            f"{self.db_port}/{self.db_name}"
        )


settings = DevSettings()
