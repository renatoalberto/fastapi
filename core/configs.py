from typing import List

from pydantic import BaseSettings

from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings) : 
    API_V1_STR : str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://renato:131232@localhost:5432/faculdade' # banco de dados:// usuario : senha @ localhost : porta / nome do banco de dados
    DB_BASE_MODEL = declarative_base()

    JWT_SECRETE: str = 'y3vJUFyjMCcH3HNPhFnHlzxnnHWwRo3B_h1Dui6KT48'   # Chave segredo gerado com a biblioteca secrets
    ALGORITHM: str = 'HS256'                                           # Char hash 256
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7                     # Tempo expiração do token (uma semana em minutos)

    class Config:
        case_sensitive = True

settings: Settings = Settings() 

"""
geração do JWT_SECRETS:

import secrets
token:str = secrets.token_urlsafe(32)
"""
