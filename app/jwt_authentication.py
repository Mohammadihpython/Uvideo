import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from app.config import settings
from datetime import datetime, timedelta


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"])
    secret = settings.SECRET

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_text, hashed_password):
        return self.pwd_context.verify(plain_text, hashed_password)

    def encode_token(self, user_phone_number: str):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=40),
            'iat': datetime.utcnow(),
            'sub': user_phone_number
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm=settings.ALGORITHMHASH
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=settings.ALGORITHMHASH)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token has expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

    def auth_wraper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
