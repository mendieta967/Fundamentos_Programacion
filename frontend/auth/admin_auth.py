import hashlib


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9"


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def validate_admin(username, password):
    username = username.strip()

    if username != ADMIN_USERNAME:
        return False

    return hash_password(password) == ADMIN_PASSWORD_HASH
