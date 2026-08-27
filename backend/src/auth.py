import os
import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWKClient, InvalidTokenError, ExpiredSignatureError, decode
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import User

COGNITO_REGION = os.getenv("COGNITO_REGION", "us-east-1")
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID", "us-east-1_izKTUwo0G")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID", "31o3ue4c6mdqqftjuvogtqdm13")
COGNITO_ISSUER = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
COGNITO_JWKS_URL = f"{COGNITO_ISSUER}/.well-known/jwks.json"
COGNITO_API_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_from_token(session: Session, token: str) -> User:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        signing_key = PyJWKClient(COGNITO_JWKS_URL).get_signing_key_from_jwt(token)
        payload = decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False},
            issuer=COGNITO_ISSUER,
        )
    except ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive guard for Cognito outages
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    cognito_id = payload.get("sub")
    if (
        not cognito_id
        or payload.get("token_use") != "access"
        or payload.get("client_id") != COGNITO_CLIENT_ID
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = session.execute(select(User).where(User.cognito_id == cognito_id)).scalar_one_or_none()
    if user is None:
        print("HERE")
        cognito_user_attributes = get_cognito_user(token)

        email = cognito_user_attributes.get("email")
        email_verified = cognito_user_attributes.get("email_verified")

        if not email or email_verified != "true":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email address is not verified",
            )
        
        user = User(
            cognito_id=cognito_id,
            email=email,
        )

        session.add(user)
        session.commit()
        session.refresh(user)
    
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    return get_user_from_token(session, token)


def get_cognito_user(access_token: str) -> dict[str, str]:
    response = requests.post(
        COGNITO_API_URL,
        headers={
            "Content-Type": "application/x-amz-json-1.1",
            "X-Amz-Target": "AWSCognitoIdentityProviderService.GetUser",
        },
        json={
            "AccessToken": access_token,
        },
        timeout=5,
    )

    print(f"status code: {response.status_code}")

    if response.status_code != 200:
        print(response.status_code, response.text)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not retrieve Cognito user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    attributes = response.json().get("UserAttributes", [])

    return {
        attribute["Name"]: attribute["Value"] for attribute in attributes
    }