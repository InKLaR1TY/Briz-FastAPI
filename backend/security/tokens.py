import jwt
from schemas.auth import DecodedToken

tokens = None


class TokenManager:
    def __init__(self, secret: str, algorithm: str) -> None:
        self.secret = secret
        self.algorithm = algorithm

    def generate(self, decode: DecodedToken) -> str:
        return jwt.encode(
            decode.model_dump(), self.secret, algorithm=self.algorithm
        )

    def decode(self, encode: str) -> dict:
        return jwt.decode(encode, self.secret, algorithms=[self.algorithm])
