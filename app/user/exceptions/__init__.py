from fastapi.exceptions import HTTPException


class UserAlreadyReviewedException(Exception):
    """Raised when a user already reviewed the system"""


class UserAlreadyReviewedHTTPException(HTTPException):
    def __init__(self, status_code=400, detail="User Already Reviewd the system") -> None:
        super().__init__(status_code, detail=detail)


class NotFoundException(Exception):
    """Erro retorno do model"""
