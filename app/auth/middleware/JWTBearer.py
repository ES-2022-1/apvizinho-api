from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.services.auth_service import AuthService
from app.common.exceptions import AuthExceptionHTTPException


class JWTBearer(HTTPBearer):
    def __init__(self, auth_service: AuthService, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.auth_service = auth_service

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthExceptionHTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.auth_service.auth(token=credentials.credentials):
                raise AuthExceptionHTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise AuthExceptionHTTPException(status_code=403, detail="Invalid authorization code.")
