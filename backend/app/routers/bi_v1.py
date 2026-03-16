from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter(prefix="/bi/v1", tags=["BI v1"])


@router.get("/hierarquia", response_model=list[schemas.BIHierarquiaItem])
def get_bi_hierarquia(
    municipio_id: UUID | None = Query(default=None),
    escola_id: UUID | None = Query(default=None),
    turma_id: UUID | None = Query(default=None),
    estado: str | None = Query(default=None, min_length=2, max_length=2, pattern="^[A-Za-z]{2}$"),
    db: Session = Depends(get_db),
) -> list[schemas.BIHierarquiaItem]:
    return crud.list_bi_hierarquia(
        db,
        municipio_id=municipio_id,
        escola_id=escola_id,
        turma_id=turma_id,
        estado=estado,
    )


@router.get("/indicadores-trimestrais", response_model=list[schemas.BIIndicadorTrimestralItem])
def get_bi_indicadores_trimestrais(
    municipio_id: UUID | None = Query(default=None),
    escola_id: UUID | None = Query(default=None),
    turma_id: UUID | None = Query(default=None),
    ano: int | None = Query(default=None, ge=2000, le=2100),
    trimestre: int | None = Query(default=None, ge=1, le=4),
    ano_escolar: int | None = Query(default=None, ge=1, le=9),
    fonte_avaliacao: schemas.FonteAvaliacao | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[schemas.BIIndicadorTrimestralItem]:
    return crud.list_bi_indicadores_trimestrais(
        db,
        municipio_id=municipio_id,
        escola_id=escola_id,
        turma_id=turma_id,
        ano=ano,
        trimestre=trimestre,
        ano_escolar=ano_escolar,
        fonte_avaliacao=fonte_avaliacao,
    )


@router.get("/ima", response_model=schemas.BIIMAResponse)
def get_bi_ima(
    group_by: schemas.GroupBy = Query(default="municipio"),
    ano: int | None = Query(default=None, ge=2000, le=2100),
    trimestre: int | None = Query(default=None, ge=1, le=4),
    ano_escolar: int | None = Query(default=None, ge=1, le=9),
    fonte_avaliacao: schemas.FonteAvaliacao | None = Query(default=None),
    municipio_id: UUID | None = Query(default=None),
    escola_id: UUID | None = Query(default=None),
    turma_id: UUID | None = Query(default=None),
    db: Session = Depends(get_db),
) -> schemas.BIIMAResponse:
    return crud.get_bi_ima(
        db,
        group_by=group_by,
        ano=ano,
        trimestre=trimestre,
        ano_escolar=ano_escolar,
        fonte_avaliacao=fonte_avaliacao,
        municipio_id=municipio_id,
        escola_id=escola_id,
        turma_id=turma_id,
    )


@router.get("/indicadores-componentes", response_model=list[schemas.BIIndicadorComponenteItem])
def get_bi_indicadores_componentes(
    municipio_id: UUID | None = Query(default=None),
    escola_id: UUID | None = Query(default=None),
    turma_id: UUID | None = Query(default=None),
    ano: int | None = Query(default=None, ge=2000, le=2100),
    trimestre: int | None = Query(default=None, ge=1, le=4),
    ano_escolar: int | None = Query(default=None, ge=1, le=9),
    fonte_avaliacao: schemas.FonteAvaliacao | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[schemas.BIIndicadorComponenteItem]:
    return crud.list_bi_indicadores_componentes(
        db,
        municipio_id=municipio_id,
        escola_id=escola_id,
        turma_id=turma_id,
        ano=ano,
        trimestre=trimestre,
        ano_escolar=ano_escolar,
        fonte_avaliacao=fonte_avaliacao,
    )


@router.get("/desempenho", response_model=schemas.BIDesempenhoResponse)
def get_bi_desempenho(
    group_by: schemas.GroupBy = Query(default="municipio"),
    ano: int | None = Query(default=None, ge=2000, le=2100),
    trimestre: int | None = Query(default=None, ge=1, le=4),
    ano_escolar: int | None = Query(default=None, ge=1, le=9),
    fonte_avaliacao: schemas.FonteAvaliacao | None = Query(default=None),
    municipio_id: UUID | None = Query(default=None),
    escola_id: UUID | None = Query(default=None),
    turma_id: UUID | None = Query(default=None),
    db: Session = Depends(get_db),
) -> schemas.BIDesempenhoResponse:
    return crud.get_bi_desempenho(
        db,
        group_by=group_by,
        ano=ano,
        trimestre=trimestre,
        ano_escolar=ano_escolar,
        fonte_avaliacao=fonte_avaliacao,
        municipio_id=municipio_id,
        escola_id=escola_id,
        turma_id=turma_id,
    )
