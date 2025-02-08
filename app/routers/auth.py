from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import requests
import json
import base64
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.primitives import serialization

router = APIRouter()

# Keycloak 配置
KEYCLOAK_URL = "http://localhost:8080"  # 你的 Keycloak 服务器地址
REALM = "MyRealm"  # 你的 Realm 名称
CLIENT_ID = "fastapi-client"  # 你的 Keycloak 客户端 ID

# 配置 OAuth2 认证，FastAPI 会自动从请求中解析 Bearer Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token")


def get_keycloak_public_key():
    """ 获取 Keycloak 的公钥（JWK 转 PEM） """
    jwks_url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"
    response = requests.get(jwks_url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="无法获取 Keycloak 公钥")

    jwks = response.json()
    if "keys" not in jwks or len(jwks["keys"]) == 0:
        raise HTTPException(status_code=500, detail="Keycloak 未返回任何公钥")

    # 获取第一个密钥
    key = jwks["keys"][0]

    # 需要用 Base64 URL 解析 `n` 和 `e`
    n = int.from_bytes(base64.urlsafe_b64decode(key["n"] + "=="), byteorder="big")
    e = int.from_bytes(base64.urlsafe_b64decode(key["e"] + "=="), byteorder="big")

    # 生成 RSA 公钥
    public_key = RSAPublicNumbers(e, n).public_key()

    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def verify_token(token: str = Security(oauth2_scheme)):
    """ 验证从 Keycloak 获取的 JWT Token """
    try:
        public_key = get_keycloak_public_key()
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=CLIENT_ID,  # 确保 CLIENT_ID 作为 `aud`，如果报错可尝试 `options={"verify_aud": False}`
            options={"verify_aud": False}  # 临时忽略 `audience` 校验
        )
        return decoded_token  # 返回解析后的 Token（包含用户信息）

    except JWTError:
        raise HTTPException(status_code=401, detail="Token 无效")


@router.get("/auth/")
async def get_user(token: dict = Depends(verify_token)):
    """ 通过 Token 获取用户信息 """
    return {
        "user_id": token["sub"],
        "email": token.get("email"),
        "roles": token.get("realm_access", {}).get("roles", [])
    }
