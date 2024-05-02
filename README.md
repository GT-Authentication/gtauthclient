# GT Auth Client

This is the Python GT Auth Client for FastAPI. It is used to authenticate with the GT Auth API and for general encryption and decryption functions.

## Installation

You can install the package using pip:

```bash
pip install gtauthclient
```

## Usage

An example of how to use the package is shown below:

```python
from fastapi import FastAPI, Depends
from gtauthclient import GTAuthClient

auth = GTAuthClient(key="Your encryption key")
app = FastAPI()

@app.get("/v1/users", dependencies=[Depends(auth.verify_user)])
async def list_users():
    return ["John", "Jane", "Jack"]
```

### Generating an encryption key

```python
from gtauthclient import GTAuthClient

encryption_key = GTAuthClient(key="").new_secure_string()
print(f"Encryption key: {encryption_key}")
auth = GTAuthClient(key=encryption_key)
```

```text
Encryption key: HexwwUHSnMb0dE4kvYn9HZHHP9s4sUktEwm774Vac86TjC0nzVIFjz8DA5astSEl
```

### Encrypting a string

```python
encrypted_string = auth.encrypt(data="This is a test string!")
print(f"Encrypted string: {encrypted_string}")
```

Response:

```text
Encrypted string: U2FsdGVkX19QpGhuABCP13Mqo6vxEkd9u3Wxs9GXOrAeC8JT9D0h9xerM8m5IQeQ
```

### Decrypting a string

```python
decrypted_string = auth.decrypt(data=encrypted_string)
print(f"Decrypted string: {decrypted_string}")
```

Response:

```text
Decrypted string: This is a test string!
```

### Decrypting a JWT

```python
decrypted_jwt = auth.verify_user(authorization=encryption_key)
print(f"Decrypted JWT: {decrypted_jwt}")
```

Response:

```text
Decrypted JWT: {'sub': 'ADMIN', 'role': 'ADMIN'}
```

See the [Tests notebook](tests.ipynb) for examples.
