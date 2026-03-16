from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter(prefix="/escolas", tags=["Escolas"])


@router.post("", response_model=schemas.EscolaRead, status_code=status.HTTP_201_CREATED)
def create_escola(
    payload: schemas.EscolaCreate,
    db: Session = Depends(get_db),
) -> schemas.EscolaRead:
    if not crud.get_municipio(db, payload.municipio_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="municipio informado nao existe",
        )
    return crud.create_escola(db, payload)


@router.get("", response_model=list[schemas.EscolaRead])
def list_escolas(
    nome: str | None = Query(default=None),
    municipio_id: UUID | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[schemas.EscolaRead]:
    return crud.list_escolas(db, nome=nome, municipio_id=municipio_id)


@router.get("/{escola_id}", response_model=schemas.EscolaRead)
def get_escola(
    escola_id: UUID,
    db: Session = Depends(get_db),
) -> schemas.EscolaRead:
    escola = crud.get_escola(db, escola_id)
    if not escola:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="escola nao encontrada")
    return escola


@router.put("/{escola_id}", response_model=schemas.EscolaRead)
def update_escola(
    escola_id: UUID,
    payload: schemas.EscolaUpdate,
    db: Session = Depends(get_db),
) -> schemas.EscolaRead:
    escola = crud.get_escola(db, escola_id)
    if not escola:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="escola nao encontrada")
    if not crud.get_municipio(db, payload.municipio_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="municipio informado nao existe",
        )
    return crud.update_escola(db, escola, payload)


@router.delete("/{escola_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_escola(
    escola_id: UUID,
    db: Session = Depends(get_db),
) -> Response:
    escola = crud.get_escola(db, escola_id)
    if not escola:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="escola nao encontrada")

    try:
        crud.delete_escola(db, escola)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="escola possui turmas vinculadas",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

