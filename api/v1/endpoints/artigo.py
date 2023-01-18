from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema
from schemas.usuario_schema import UsuarioSchema
from core.depes import get_session, get_current_user


router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(artigo: ArtigoSchema, usuario_logado: UsuarioModel = Depends(get_current_user), db:AsyncSession = Depends(get_session)):
    novo_artigo: ArtigoModel = ArtigoModel(
        titulo=artigo.titulo,
        descricao=artigo.descricao,
        url_font=artigo.url_font,
        usuario_id=usuario_logado.id
    )

    db.add(novo_artigo)
    await db.commit()

    return novo_artigo

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos: List[ArtigoSchema] = result.scalars().unique().all()

        return artigos

@router.get('/{artigo_id}', status_code=status.HTTP_200_OK, response_model=ArtigoSchema)
async def get_artigo(artigo_id: int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id==artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()

        if artigo:
            return artigo
        else:
            raise HTTPException(detail='Artigo não encontrado', status_code=status.HTTP_404_NOT_FOUND)

@router.put('/{artigo_id}', status_code=status.HTTP_202_ACCEPTED, response_model=ArtigoSchema)
async def put_artigo(artigo_id: int, artigo:ArtigoSchema, db:AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id==artigo_id)
        result = await session.execute(query)
        artigo_alterado: ArtigoModel = result.scalars().unique().one_or_none()

        if artigo_alterado:
            if artigo.titulo:
                artigo_alterado.titulo = artigo.titulo
            if artigo.descricao:
                artigo_alterado.descricao = artigo.descricao
            if artigo.url_font:
                artigo_alterado.url_font = artigo.url_font
            if usuario_logado.id != artigo_alterado.usuario_id:                
                artigo_alterado.usuario_id = usuario_logado.id
            
            await session.commit()

            return artigo_alterado
        else:
            raise HTTPException(detail='Artigo não encontrado', status_code=status.HTTP_404_NOT_FOUND)

@router.delete('/{artigo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(artigo_id: int, db:AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id==artigo_id).filter(ArtigoModel.usuario_id==usuario_logado.id)
        result = await session.execute(query)
        artigo_deletado: ArtigoModel = result.scalars().unique().one_or_none()

        if artigo_deletado:
            await session.delete(artigo_deletado)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Artigo não encontrado', status_code=status.HTTP_404_NOT_FOUND)
