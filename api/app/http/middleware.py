import jwt
from hashlib import sha256

access_token = ""

decoded = jwt.decode(access_token, "secret", algorithms=["HS256"])
print(decoded)

password_hash = sha256("admin".encode("utf-8")).hexdigest()
print(password_hash)
