from datetime import datetime, timedelta

from jose import jwt

from app.auth.schemas.auth import SessionCreate, TokenPayload, Tokens
from app.common.exceptions import AuthException
from app.common.models.users import Users
from app.common.utils.password import check_password
from app.core.settings import JWT_REFRESH_SECRET_KEY, JWT_SECRET_KEY
from app.user.services.user_service import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
        self.REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
        self.ALGORITHM = "HS256"
        self.JWT_REFRESH_SECRET_KEY = JWT_REFRESH_SECRET_KEY
        self.JWT_SECRET_KEY = JWT_SECRET_KEY

    def create_tokens(self, session_create: SessionCreate) -> Tokens:
        user: Users = self.user_service.get_user_by_email(session_create.email)

        if not (check_password(session_create.password, user.password_hash)):
            raise AuthException(detail="Wrong password")

        return Tokens(
            access_token=self.create_access_token(session_create=session_create, user=user),
            refresh_token=self.create_refresh_token(session_create=session_create, user=user),
        )

    def create_access_token(self, session_create: SessionCreate, user: Users) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = TokenPayload(
            exp=expires_delta,
            sub=str(user.id_user),
            id_user=str(user.id_user),
            email=user.email,
            name=f"{user.firstname} {user.surname}",
        ).dict()

        encoded_jwt = jwt.encode(to_encode, self.JWT_SECRET_KEY, self.ALGORITHM)

        return encoded_jwt

    def create_refresh_token(self, session_create: SessionCreate, user: Users) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = TokenPayload(
            exp=expires_delta,
            sub=str(user.id_user),
            id_user=str(user.id_user),
            email=user.email,
            name=f"{user.firstname} {user.surname}",
        ).dict()

        encoded_jwt = jwt.encode(to_encode, self.JWT_REFRESH_SECRET_KEY, self.ALGORITHM)

        return encoded_jwt
