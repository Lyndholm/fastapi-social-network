from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_string(string: str):
    return crypt_context.hash(string)
