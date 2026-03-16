from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter(prefix="/turmas", tags=["Turmas"])


@router.post("", response_model=schemas.TurmaRead, status_code=status.HTTP_201_CREATED)
def create_turma(
    payload: schemas.TurmaCreate,
    db: Session = Depends(get_db),
) -> schemas.TurmaRead:
    if not crud.get_escola(db, payload.escola_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="escola informada nao existe",
        )
    return crud.create_turma(db, payload)


@router.get("", response_model=list[schemas.TurmaRead])
def list_turmas(
    nome: str | None = Query(default=None),
    escola_id: UUID | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[schemas.TurmaRead]:
    return crud.list_turmas(db, nome=nome, escola_id=escola_id)


@router.get("/{turma_id}", response_model=schemas.TurmaRead)
def get_turma(
    turma_id: UUID,
    db: Session = Depends(get_db),
) -> schemas.TurmaRead:
    turma = crud.get_turma(db, turma_id)
    if not turma:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="turma nao encontrada")
    return turma


@router.put("/{turma_id}", response_model=schemas.TurmaRead)
def update_turma(
    turma_id: UUID,
    payload: schemas.TurmaUpdate,
    db: Session = Depends(get_db),
) -> schemas.TurmaRead:
    turma = crud.get_turma(db, turma_id)
    if not turma:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="turma nao encontrada")
    if not crud.get_escola(db, payload.escola_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="escola informada nao existe",
        )
    return crud.update_turma(db, turma, payload)


@router.delete("/{turma_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_turma(
    turma_id: UUID,
    db: Session = Depends(get_db),
) -> Response:
    turma = crud.get_turma(db, turma_id)
    if not turma:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="turma nao encontrada")
    crud.delete_turma(db, turma)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

