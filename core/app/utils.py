import string
import random
from jose import jwt, JWTError
from core import GlobalConstants
from binascii import hexlify, unhexlify
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Request, HTTPException, status
from core.app.api.responses import ResponseMessages
from cryptography.hazmat.backends import default_backend
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from cryptography.hazmat.primitives.padding import PaddingContext, PKCS7
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes, AEADEncryptionContext, AEADDecryptionContext


class JWTAccessBearer(HTTPBearer):

    def __init__(self):
        super(JWTAccessBearer, self).__init__()

    async def __call__(self, request: Request) -> str:
        credentials: HTTPAuthorizationCredentials = await super(JWTAccessBearer, self).__call__(request)
        return AuthHelper().verify_token(request, credentials, 'access')


class AuthHelper(GlobalConstants, ResponseMessages):
    pwd_context: CryptContext = CryptContext(
        schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hash_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hash_password)

    @classmethod
    def generate_password(cls, length: int) -> str:
        special_characters = "!@#$%^&*()_-+=<>?"
        password_characters = [random.choice(string.ascii_uppercase), random.choice(
            string.digits), random.choice(special_characters)]
        password_characters.extend(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits +
                                                  special_characters, k=length - 3))
        random.shuffle(password_characters)
        return ''.join(password_characters)

    def generate_access_token(self, data: dict, expires_at: timedelta = None, vas: bool = False, token_type: int = 1) -> str:
        expires_at: timedelta = expires_at or timedelta(minutes=30)
        expiry_date: datetime = datetime.utcnow() + expires_at
        _data = data.copy()
        if token_type == 2:
            del _data['access_token']
        _data['token_type'] = 'access' if token_type == 1 else 'refresh'
        _data['iat'] = int(datetime.now().timestamp())
        _data["exp"] = expiry_date
        return jwt.encode(_data, self.ENCRYPTION_SECRET_KEY, self.ENCRYPTION_ALGORITHM)

    def verify_token(self, request: Request, credentials: HTTPAuthorizationCredentials, token_type: str) -> str:
        try:
            if not credentials:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            token: str = credentials.credentials
            payload: dict = jwt.decode(
                token, self.ENCRYPTION_SECRET_KEY, self.ENCRYPTION_ALGORITHM)
            payload['base_url'] = request.base_url

            if payload.get('token_type') != token_type:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail={"status_code": 401, "message": "Invalid Token"})

            request.state.token_payload = payload
            return credentials.credentials
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"status_code": 401,
                        "message": self.ERROR_SIGNATURE_EXPIRED, "details": repr(e)}
            )


class GlobalHelpers(AuthHelper):
    def AES256_encryption(self, plaintext: str) -> str:
        _padding: PaddingContext = PKCS7(128).padder()
        padded_plaintext: bytes = _padding.update(
            plaintext.encode()) + _padding.finalize()
        cipher: Cipher = Cipher(algorithms.AES(self.AES256_KEY), modes.CBC(
            self.AES256_IV), backend=default_backend())
        encryptor: AEADEncryptionContext = cipher.encryptor()
        ciphertext: bytes = encryptor.update(
            padded_plaintext) + encryptor.finalize()
        return hexlify(ciphertext).decode()

    def AES256_decryption(self, ciphertext: str) -> str:
        cipher: Cipher = Cipher(algorithms.AES(self.AES256_KEY), modes.CBC(
            self.AES256_IV), backend=default_backend())
        decryptor: AEADDecryptionContext = cipher.decryptor()
        padded_plaintext: bytes = decryptor.update(
            unhexlify(ciphertext)) + decryptor.finalize()
        unpadder: PaddingContext = PKCS7(128).unpadder()
        plaintext: bytes = unpadder.update(
            padded_plaintext) + unpadder.finalize()
        return plaintext.decode()
