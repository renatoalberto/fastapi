from typing import Optional, List
from pydantic import BaseModel as SCBaseModel
from pydantic import EmailStr

from schemas.artigo_schema import ArtigoSchema


class UsuarioSchema(SCBaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    admin: bool = False

    class Config:
        orm_mode = True


# Utilizado na criação
class UsuariosSchemaCreate(UsuarioSchema):
    senha: str


# Utilizado na consulta dos arquigos
class UsuarioSchemaArtigos(UsuarioSchema):
    artigos: Optional[List[ArtigoSchema]]


# utilizado na atualização dos dados
class UsuarioSchemaAtualizacao(UsuarioSchema):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    admin: Optional[bool]
