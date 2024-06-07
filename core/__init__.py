import os
from dataclasses import dataclass


@dataclass(frozen=True)
class GlobalConstants:
    ENCRYPTION_SECRET_KEY: str = os.getenv('ENCRYPTION_SECRET_KEY')
    ENCRYPTION_ALGORITHM: str = os.getenv('ENCRYPTION_ALGORITHM')
    AES256_KEY: str = os.getenv('AES256_KEY')
    AES256_IV: str = os.getenv('AES256_IV')
    LOCAL_LLM: str = os.getenv('LOCAL_LLM')
    
