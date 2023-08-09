import jwt
from fastapi import Header, HTTPException


class GTAuthClient:
    def __init__(self, encryption_secret: str):
        self.encryption_secret = encryption_secret

    def get_user(self, authorization: str = Header(None)):
        try:
            scheme, _, api_key = authorization.partition(" ")
            # decode the token using a secret key
            return jwt.decode(
                jwt=api_key,
                key=self.encryption_secret,
                algorithms=["HS256"],
            )
        except:
            raise HTTPException(status_code=401, detail="Invalid token.")
