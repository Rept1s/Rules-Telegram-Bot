from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    token: str
    adm_id: int


@dataclass
class Settings:
    bots: Bots

@dataclass
class Database:
    database: str


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            token=env.str("TOKEN"),
            adm_id=env.int("ADM_ID")
        )
    )


def get_database():
    env = Env()
    env.read_env('input')

    return Database(database=env.str("DB_PATCH"))


def settings_all():
    return get_settings('input')
