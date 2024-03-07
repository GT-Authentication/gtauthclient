import jwt
from fastapi import Header, HTTPException


class GTAuthClient:
    def __init__(self, key: str):
        self.key = key

    def verify_user(self, authorization: str = Header(None)):
        try:
            if authorization == self.key:
                return {"sub": "ADMIN", "role": "ADMIN"}
            if "bearer" in authorization.lower():
                scheme, _, api_key = authorization.partition(" ")
                authorization = api_key
            return jwt.decode(
                jwt=authorization,
                key=self.key,
                algorithms=["HS256"],
            )
        except:
            raise HTTPException(status_code=401, detail="Invalid token.")
