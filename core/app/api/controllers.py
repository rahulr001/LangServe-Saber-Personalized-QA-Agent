import sys
from fastapi import status
from core.app import Session
from core.app.api.models import Users
from core.app.utils import GlobalHelpers
from sqlalchemy.exc import SQLAlchemyError
from core.app.api.responses import APIResponse
from core.app.api.exception import CustomException
from core.app.api.schemas import UserRegisterSchema


class CoreController(GlobalHelpers):
    def register(self, params: UserRegisterSchema):
        try:
            with Session() as session:
                user: Users = (session.query(Users).filter(
                    Users.email == self.AES256_encryption(params.email)).first())

            if user:
                return APIResponse(status.HTTP_226_IM_USED, self.ERROR_DUPLICATE_USER, 'DUPLICATE USER')

            elif self.verify_password(params.password1, user.password):
                return APIResponse(status.HTTP_406_NOT_ACCEPTABLE, self.ERROR_SAME_OLD_NEW_PASSWORD, "SAME PASSWORD")

            elif params.password1 != params.password2:
                return APIResponse(status.HTTP_406_NOT_ACCEPTABLE, self.ERROR_PASSWORD_MISMATCH, "PASSWORD MISMATCH")

            plain_password: str = self.generate_password(8)
            with Session() as session:
                try:
                    session.add(Users(
                        name=self.AES256_encryption(params.name),
                        email=self.AES256_encryption(params.email),
                        password=self.hash_password(plain_password),
                        role=params.role
                    ))
                    session.commit()
                except SQLAlchemyError as se:
                    session.rollback()
                    return APIResponse(status.HTTP_424_FAILED_DEPENDENCY, "FAILED DEPENDENCY", CustomException(repr(se), sys))
                finally:
                    session.close()

            return APIResponse(status.HTTP_201_CREATED, self.SUCCESSFUL_USER_ADD, "CREATED")
        except Exception as e:
            return APIResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "INTERNAL SERVER ERROR", CustomException(repr(e), sys))
