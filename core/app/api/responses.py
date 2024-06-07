from typing import Any
from fastapi import status as st
from core.app.api.exception import CustomException
from fastapi.responses import JSONResponse as Response
from dataclasses import dataclass


class APIResponse(Response):

    def __init__(self, status_code: int = st.HTTP_200_OK, message: str = 'SUCCESS', details: Any = None):
        self.content = {"status_code": status_code,
                        "message": message,
                        "details": str(details) if isinstance(details, CustomException) else details}
        super().__init__(self.content, status_code)


class JSONResponse:

    def __init__(self, status_code: int = st.HTTP_200_OK, message: str = 'SUCCESS', details: Any = None):
        self.status_code = status_code
        self.message = message
        self.details = details


@dataclass(frozen=False)
class ResponseErrorMessages:
    ERROR_SIGNATURE_EXPIRED: str = 'Your session has expired. Please log in again to continue.'
    ERROR_INVALID_CREDENTIALS: str = 'Invalid login credentials. Please check email address & password.'
    ERROR_INCORRECT_EMAIL: str = 'Not an existing user.'
    ERROR_PASSWORD_MISMATCH: str = 'Your new password entered in the new password and retype password field do not match.'
    ERROR_SAME_OLD_NEW_PASSWORD: str = 'Your old password and new password are same, Please choose a different password.'
    ERROR_OLD_PASSWORD: str = 'Incorrect current password. Please try again.'
    ERROR_OTP_INCORRECT: str = 'Invalid verification code. Please double-check and try again.'
    ERROR_OTP_EXPIRED: str = 'The verification code has expired. Please request a new code.'
    ERROR_OTP_NOT_VERIFIED: str = 'The verification code is not verified, Please verify before continuing.'
    ERROR_ACCESS_DENIED: str = 'Access denied. Please check with admin'
    ERROR_DUPLICATE_USER: str = 'Another user is already associated with this email.'


@dataclass(frozen=False)
class ResponseSuccessMessages:
    SUCCESSFUL_LOGIN: str = 'Welcome! You have successfully logged into your account.'
    SUCCESSFUL_CHANGE_PASSWORD: str = 'You have successfully changed your password. You may login with your new password now.'
    SUCCESSFUL_OTP_SEND: str = 'Verification code has sent to your email address.'
    SUCCESSFUL_OTP_VERIFICATION: str = 'Verification code has been verified successfully.'
    SUCCESSFUL_USER_ADD: str = 'Congratulations! Registration successfull.'


class ResponseMessages(ResponseErrorMessages, ResponseSuccessMessages):
    ...
