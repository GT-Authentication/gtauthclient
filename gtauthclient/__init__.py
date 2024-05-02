import os
import jwt
import base64
import secrets
import string
from fastapi import Header, HTTPException
from datetime import timedelta
from Crypto.Cipher import AES
from hashlib import md5


class GTAuthClient:
    def __init__(self, key: str):
        self.key = key

    def verify_user(self, authorization: str = Header(None)):
        """
        Verify the user.

        Args:
            authorization (str, optional): The authorization header. Defaults to Header(None).

        Raises:
            HTTPException: Invalid token.

        Returns:
            dict: The user data.
        """
        try:
            authorization = (
                str(authorization).replace("Bearer ", "").replace("bearer ", "")
            )
            if authorization == self.key:
                return {"sub": "ADMIN", "role": "ADMIN"}
            return jwt.decode(
                jwt=authorization,
                key=self.key,
                algorithms=["HS256"],
                leeway=timedelta(seconds=90),
            )
        except:
            raise HTTPException(status_code=401, detail="Invalid token.")

    def encrypt(self, data):
        """
        Encrypt data.

        Args:
            data (str): The data to encrypt.

        Returns:
            str: The encrypted data.
        """
        passphrase = self.key
        passphrase = passphrase.encode("utf-8")
        salt = os.urandom(8)
        passphrase += salt
        key = md5(passphrase).digest()
        final_key = key
        while len(final_key) < 32 + 16:
            key = md5(key + passphrase).digest()
            final_key += key
        key_iv = final_key[: 32 + 16]
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = AES.new(key, AES.MODE_CBC, iv)
        padded_data = data.encode("utf-8") + (16 - len(data) % 16) * bytes(
            [16 - len(data) % 16]
        )
        encrypted_data = aes.encrypt(padded_data)
        encrypted = b"Salted__" + salt + encrypted_data
        return base64.b64encode(encrypted).decode("utf-8")

    def decrypt(self, data):
        """
        Decrypt data.

        Args:
            data (str): The data to decrypt.

        Returns:
            str: The decrypted data.
        """
        passphrase = self.key
        try:
            passphrase = passphrase.encode("utf-8")
            encrypted = base64.b64decode(data)
            assert encrypted[0:8] == b"Salted__"
            salt = encrypted[8:16]
            assert len(salt) == 8, len(salt)
            passphrase += salt
            key = md5(passphrase).digest()
            final_key = key
            while len(final_key) < 32 + 16:
                key = md5(key + passphrase).digest()
                final_key += key
            key_iv = final_key[: 32 + 16]
            key = key_iv[:32]
            iv = key_iv[32:]
            aes = AES.new(key, AES.MODE_CBC, iv)
            data = aes.decrypt(encrypted[16:])
            decrypted = data[: -(data[-1] if type(data[-1]) == int else ord(data[-1]))]
            return decrypted.decode("utf-8")
        except:
            return encrypted

    def new_secure_string(self):
        """
        Generate a new secure string.

        Returns:
            str: A new secure string.
        """
        return "".join(
            secrets.choice(string.ascii_letters + string.digits) for i in range(64)
        )
