import controller.DatabaseController as database
import re
import bcrypt

SQLI_PATTERN = re.compile(r"(?i)(\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|UNION|EXEC|EXECUTE|GRANT|REVOKE|TRUNCATE|MERGE|CALL|--|#)\b|['\";]|/\*|\*/|--|#)")

##### Hashes ####
async def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


async def verify_password(password: str, hashed: str) -> bool:
    if bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')):
        return True
    else:
        return False


### INICIOS DE SESIÓN ###
async def check_login(username: str, password: str) -> bool:
    if await verify_password(username, password):
        return True
    else:
        return False
