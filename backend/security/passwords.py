from passlib.context import CryptContext

from core.config import get_settings


class PasswordManager:
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=get_settings().schemes.split(','),
            deprecated=get_settings().deprecated,
            argon2__time_cost=get_settings().argon2__time_cost,
            argon2__memory_cost=get_settings().argon2__memory_cost,
            argon2__parallelism=get_settings().argon2__parallelism,
            bcrypt__rounds=get_settings().bcrypt__rounds,
            pbkdf2_sha256__rounds=get_settings().pbkdf2_sha256__rounds,
        )

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)
