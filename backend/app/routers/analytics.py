from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/ima", response_model=schemas.IMAAnalyticsResponse)
def get_ima_analytics(
    group_by: str = Query(default="municipio", pattern="^(municipio|escola|turma)$"),
    ano: int | None = Query(default=None, ge=2000, le=2100),
    trimestre: int | None = Query(default=None, ge=1, le=4),
    municipio_id: UUID | None = Query(default=None),
    escola_id: UUID | None = Query(default=None),
    turma_id: UUID | None = Query(default=None),
    db: Session = Depends(get_db),
) -> schemas.IMAAnalyticsResponse:
    return crud.get_analytics_ima(
        db,
        group_by=group_by,
        ano=ano,
        trimestre=trimestre,
        municipio_id=municipio_id,
        escola_id=escola_id,
        turma_id=turma_id,
    )

