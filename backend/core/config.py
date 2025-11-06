from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    title: str

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: str

    schemes: str
    deprecated: str = 'auto'
    argon2__time_cost: int
    argon2__memory_cost: int
    argon2__parallelism: int
    bcrypt__rounds: int
    pbkdf2_sha256__rounds: int

    phone_number: str
    first_name: str
    last_name: str
    password: str

    secret: str
    algorithm: str
    default_expire_minutes: int = 2592000  # 30 days

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=False,
        env_nested_delimiter='__',
    )

    @property
    def database_url(self):
        return (
            f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}'
            f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'
        )

    @property
    def superuser_data(self):
        return {
            'phone_number': self.phone_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': self.password,
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
