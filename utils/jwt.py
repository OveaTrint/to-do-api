import os

from dotenv import load_dotenv
from joserfc import jwt
from joserfc.jwk import OctKey

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
assert SECRET_KEY is not None, "Secret key not found in .env file"


def get_jwt(claims):
    header = {"alg": "HS256", "typ": "JWT"}
    key = OctKey.import_key(SECRET_KEY)

    token = jwt.encode(header, claims, key)

    return token


def verify_jwt():
    pass
