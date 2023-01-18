from typing import List, Optional, Any
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchema, UsuarioSchemaArtigos, UsuarioSchemaAtualizacao, UsuariosSchemaCreate
from core.depes import get_current_user, get_session
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

router = APIRouter()

# Get Logado
@router.get('/logado', response_model=UsuarioSchema)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado

# POST / Signup
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchema)
async def post_usuario(usuario: UsuariosSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
        admin=usuario.admin
    )

    try:

        async with db as session:
            session.add(novo_usuario)
            await session.commit()

            return novo_usuario
    except IntegrityError:
        raise HTTPException(detail='Email já está cadastrado.', status_code=status.HTTP_406_NOT_ACCEPTABLE)

# GET Usuarios
@router.get('/', response_model=List[UsuarioSchema])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List(UsuarioSchema) = result.scalars().unique().all()

        return usuarios

# GET Usuario
@router.get('/{usuario_id}', response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usário não encontrado', status_code=status.HTTP_404_NOT_FOUND)

# PUT Usuario
@router.put('/{usuario_id}', response_model=UsuarioSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaAtualizacao, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_atl: UsuarioSchema = result.scalars().unique().one_or_none()

        if usuario_atl:
            if usuario.nome:
                usuario_atl.nome = usuario.nome
            if usuario.sobrenome:
                usuario_atl.sobrenome = usuario.sobrenome                
            if usuario.email:
                usuario_atl.email = usuario.email
            if usuario.admin:
                usuario_atl.admin = usuario.admin
            if usuario.senha:
                usuario_atl.senha = gerar_hash_senha(usuario.senha)
            
            await session.commit()

            return usuario_atl
        else:
            raise HTTPException(detail='Usário não encontrado', status_code=status.HTTP_404_NOT_FOUND)

# DELETE Usuario
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()

        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Usário não encontrado', status_code=status.HTTP_404_NOT_FOUND)

# POST Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario: UsuarioSchema = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dados de acesso incorretos.')
    
    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id), "toke_type": "bearer"}, status_code=status.HTTP_200_OK)
