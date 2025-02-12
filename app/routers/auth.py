from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import requests
import json
import base64
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.primitives import serialization

router = APIRouter()

# Keycloak configuration
KEYCLOAK_URL = "http://localhost:8080"  # Your Keycloak server address
REALM = "WEHI"  # Your Realm name
CLIENT_ID = "fastapi-client"  # Your Keycloak client ID

# Configure OAuth2 authentication, FastAPI will automatically parse the Bearer Token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token")


def get_keycloak_public_key():
    """ Retrieve the Keycloak public key (JWK to PEM) """
    jwks_url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"
    response = requests.get(jwks_url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch Keycloak public key")

    jwks = response.json()
    if "keys" not in jwks or len(jwks["keys"]) == 0:
        raise HTTPException(status_code=500, detail="Keycloak did not return any public keys")

    # Retrieve the first key
    key = jwks["keys"][0]

    # Decode `n` and `e` from Base64 URL
    n = int.from_bytes(base64.urlsafe_b64decode(key["n"] + "=="), byteorder="big")
    e = int.from_bytes(base64.urlsafe_b64decode(key["e"] + "=="), byteorder="big")

    # Generate RSA public key
    public_key = RSAPublicNumbers(e, n).public_key()

    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def verify_token(token: str = Security(oauth2_scheme)):
    """ Verify the JWT Token obtained from Keycloak """
    try:
        public_key = get_keycloak_public_key()
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=CLIENT_ID,  # Ensure CLIENT_ID is present as `aud`, if an error occurs, try `options={"verify_aud": False}`
            options={"verify_aud": False}  # Temporarily disable `audience` verification
        )
        return decoded_token  # Return the decoded Token (containing user information)

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")


@router.get("/auth/")
async def get_user(token: dict = Depends(verify_token)):
    """ Retrieve user information via Token """
    return {
        "user_id": token["sub"],
        "email": token.get("email"),
        "roles": token.get("realm_access", {}).get("roles", [])
    }
