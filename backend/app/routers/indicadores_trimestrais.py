from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter(prefix="/indicadores-trimestrais", tags=["IndicadoresTrimestrais"])


@router.post("", response_model=schemas.IndicadorTrimestralRead, status_code=status.HTTP_201_CREATED)
def create_indicador_trimestral(
    payload: schemas.IndicadorTrimestralCreate,
    db: Session = Depends(get_db),
) -> schemas.IndicadorTrimestralRead:
    if not crud.get_turma(db, payload.turma_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="turma informada nao existe",
        )
    try:
        return crud.create_indicador_trimestral(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="ja existe indicador para esta turma, ano e trimestre",
        )


@router.get("", response_model=list[schemas.IndicadorTrimestralRead])
def list_indicadores_trimestrais(
    turma_id: UUID | None = Query(default=None),
    ano: int | None = Query(default=None, ge=2000, le=2100),
    trimestre: int | None = Query(default=None, ge=1, le=4),
    db: Session = Depends(get_db),
) -> list[schemas.IndicadorTrimestralRead]:
    return crud.list_indicadores_trimestrais(
        db,
        turma_id=turma_id,
        ano=ano,
        trimestre=trimestre,
    )


@router.get("/{indicador_id}", response_model=schemas.IndicadorTrimestralRead)
def get_indicador_trimestral(
    indicador_id: UUID,
    db: Session = Depends(get_db),
) -> schemas.IndicadorTrimestralRead:
    indicador = crud.get_indicador_trimestral(db, indicador_id)
    if not indicador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="indicador trimestral nao encontrado",
        )
    return indicador


@router.put("/{indicador_id}", response_model=schemas.IndicadorTrimestralRead)
def update_indicador_trimestral(
    indicador_id: UUID,
    payload: schemas.IndicadorTrimestralUpdate,
    db: Session = Depends(get_db),
) -> schemas.IndicadorTrimestralRead:
    indicador = crud.get_indicador_trimestral(db, indicador_id)
    if not indicador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="indicador trimestral nao encontrado",
        )
    if not crud.get_turma(db, payload.turma_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="turma informada nao existe",
        )
    try:
        return crud.update_indicador_trimestral(db, indicador, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="ja existe indicador para esta turma, ano e trimestre",
        )


@router.delete("/{indicador_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_indicador_trimestral(
    indicador_id: UUID,
    db: Session = Depends(get_db),
) -> Response:
    indicador = crud.get_indicador_trimestral(db, indicador_id)
    if not indicador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="indicador trimestral nao encontrado",
        )

    crud.delete_indicador_trimestral(db, indicador)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

