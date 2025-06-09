import controller.DatabaseController as database
import re
from passlib.hash import pbkdf2_sha256
import controller.UserController as users

SQLI_PATTERN = re.compile(r"(?i)(\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|UNION|EXEC|EXECUTE|GRANT|REVOKE|TRUNCATE|MERGE|CALL|--|#)\b|['\";]|/\*|\*/|--|#)")

# Encripta la contraseña
async def encrypt_passwd(passwd):
    hash_passwd = pbkdf2_sha256.hash(passwd)
    return hash_passwd

# Verifica si la contraseña concuerda con la del hash
async def verify_passwd(passwd, hash):
    return pbkdf2_sha256.verify(passwd, hash)

### INICIOS DE SESIÓN ###
async def check_login(username: str, password: str) -> bool:
    user = await users.get_user_by_name(username)
    hash = user['password']

    if await verify_passwd(password, hash):
        return True
    else:
        return False
