from hashlib import sha256

from app.application.security.token_generator import TokenGenerator


class SHA256TokenGenerator(TokenGenerator):
    def __init__(self, salt: str):
        self._salt = salt

    def generate(self, input: str) -> str:
        salted_input = input + self._salt
        return sha256(salted_input.encode("utf-8")).hexdigest()[-5:]

    def validate(self, id: str, token: str) -> bool:
        return self.generate(id) == token
