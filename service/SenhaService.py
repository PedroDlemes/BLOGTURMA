
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

class SenhaService:

    def __init__(self):
        self.hasher = PasswordHasher()

    def GerarHash(self, senha):
        return self.hasher.hash(senha)

    def Verificar(self, senha, hash_senha):
        try:
            return self.hasher.verify(hash_senha, senha)
        except (VerifyMismatchError, VerificationError):
            return False
