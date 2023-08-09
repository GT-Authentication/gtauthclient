[![GitHub](https://img.shields.io/badge/GitHub-Sponsor%20Josh%20XT-blue?logo=github&style=plastic)](https://github.com/sponsors/Josh-XT) [![PayPal](https://img.shields.io/badge/PayPal-Sponsor%20Josh%20XT-blue.svg?logo=paypal&style=plastic)](https://paypal.me/joshxt) [![Ko-Fi](https://img.shields.io/badge/Kofi-Sponsor%20Josh%20XT-blue.svg?logo=kofi&style=plastic)](https://ko-fi.com/joshxt)
# GT Auth Client

This is the Python GT Auth Client for FastAPI. It is used to authenticate with the GT Auth API.
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