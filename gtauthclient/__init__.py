import jwt
from fastapi import Header, HTTPException


class GTAuthClient:
    def __init__(self, key: str):
        self.key = key

    def verify_user(self, authorization: str = Header(None)):
        try:
            scheme, _, api_key = authorization.partition(" ")
            if scheme != "Bearer":
                raise HTTPException(status_code=401, detail="Invalid token.")
            return jwt.decode(
                jwt=api_key,
                key=self.key,
                algorithms=["HS256"],
            )
        except:
            raise HTTPException(status_code=401, detail="Invalid token.")
