from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter(prefix="/municipios", tags=["Municipios"])


@router.post("", response_model=schemas.MunicipioRead, status_code=status.HTTP_201_CREATED)
def create_municipio(
    payload: schemas.MunicipioCreate,
    db: Session = Depends(get_db),
) -> schemas.MunicipioRead:
    return crud.create_municipio(db, payload)


@router.get("", response_model=list[schemas.MunicipioRead])
def list_municipios(
    nome: str | None = Query(default=None),
    estado: str | None = Query(default=None, min_length=2, max_length=2),
    db: Session = Depends(get_db),
) -> list[schemas.MunicipioRead]:
    return crud.list_municipios(db, nome=nome, estado=estado)


@router.get("/{municipio_id}", response_model=schemas.MunicipioRead)
def get_municipio(
    municipio_id: UUID,
    db: Session = Depends(get_db),
) -> schemas.MunicipioRead:
    municipio = crud.get_municipio(db, municipio_id)
    if not municipio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="municipio nao encontrado")
    return municipio


@router.put("/{municipio_id}", response_model=schemas.MunicipioRead)
def update_municipio(
    municipio_id: UUID,
    payload: schemas.MunicipioUpdate,
    db: Session = Depends(get_db),
) -> schemas.MunicipioRead:
    municipio = crud.get_municipio(db, municipio_id)
    if not municipio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="municipio nao encontrado")
    return crud.update_municipio(db, municipio, payload)


@router.delete("/{municipio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_municipio(
    municipio_id: UUID,
    db: Session = Depends(get_db),
) -> Response:
    municipio = crud.get_municipio(db, municipio_id)
    if not municipio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="municipio nao encontrado")

    try:
        crud.delete_municipio(db, municipio)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="municipio possui escolas vinculadas",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

