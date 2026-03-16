from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app import models, schemas


def create_municipio(db: Session, payload: schemas.MunicipioCreate) -> models.Municipio:
    municipio = models.Municipio(nome=payload.nome, estado=payload.estado)
    db.add(municipio)
    db.commit()
    db.refresh(municipio)
    return municipio


def list_municipios(
    db: Session,
    nome: str | None = None,
    estado: str | None = None,
) -> list[models.Municipio]:
    stmt = select(models.Municipio)

    if nome:
        stmt = stmt.where(models.Municipio.nome.ilike(f"%{nome.strip()}%"))
    if estado:
        stmt = stmt.where(models.Municipio.estado == estado.strip().upper())

    return list(db.scalars(stmt.order_by(models.Municipio.nome)))


def get_municipio(db: Session, municipio_id: UUID) -> models.Municipio | None:
    return db.get(models.Municipio, municipio_id)


def update_municipio(
    db: Session,
    municipio: models.Municipio,
    payload: schemas.MunicipioUpdate,
) -> models.Municipio:
    municipio.nome = payload.nome
    municipio.estado = payload.estado
    db.commit()
    db.refresh(municipio)
    return municipio


def delete_municipio(db: Session, municipio: models.Municipio) -> None:
    db.delete(municipio)
    db.commit()


def create_escola(db: Session, payload: schemas.EscolaCreate) -> models.Escola:
    escola = models.Escola(nome=payload.nome, municipio_id=payload.municipio_id)
    db.add(escola)
    db.commit()
    db.refresh(escola)
    return escola


def list_escolas(
    db: Session,
    nome: str | None = None,
    municipio_id: UUID | None = None,
) -> list[models.Escola]:
    stmt = select(models.Escola)

    if nome:
        stmt = stmt.where(models.Escola.nome.ilike(f"%{nome.strip()}%"))
    if municipio_id:
        stmt = stmt.where(models.Escola.municipio_id == municipio_id)

    return list(db.scalars(stmt.order_by(models.Escola.nome)))


def get_escola(db: Session, escola_id: UUID) -> models.Escola | None:
    return db.get(models.Escola, escola_id)


def update_escola(
    db: Session,
    escola: models.Escola,
    payload: schemas.EscolaUpdate,
) -> models.Escola:
    escola.nome = payload.nome
    escola.municipio_id = payload.municipio_id
    db.commit()
    db.refresh(escola)
    return escola


def delete_escola(db: Session, escola: models.Escola) -> None:
    db.delete(escola)
    db.commit()


def create_turma(db: Session, payload: schemas.TurmaCreate) -> models.Turma:
    turma = models.Turma(nome=payload.nome, escola_id=payload.escola_id)
    db.add(turma)
    db.commit()
    db.refresh(turma)
    return turma


def list_turmas(
    db: Session,
    nome: str | None = None,
    escola_id: UUID | None = None,
) -> list[models.Turma]:
    stmt = select(models.Turma)

    if nome:
        stmt = stmt.where(models.Turma.nome.ilike(f"%{nome.strip()}%"))
    if escola_id:
        stmt = stmt.where(models.Turma.escola_id == escola_id)

    return list(db.scalars(stmt.order_by(models.Turma.nome)))


def get_turma(db: Session, turma_id: UUID) -> models.Turma | None:
    return db.get(models.Turma, turma_id)


def update_turma(
    db: Session,
    turma: models.Turma,
    payload: schemas.TurmaUpdate,
) -> models.Turma:
    turma.nome = payload.nome
    turma.escola_id = payload.escola_id
    db.commit()
    db.refresh(turma)
    return turma


def delete_turma(db: Session, turma: models.Turma) -> None:
    db.delete(turma)
    db.commit()


def _calculate_percentual(alfabetizados: int, total_alunos: int) -> Decimal:
    if total_alunos == 0:
        return Decimal("0.00")
    percentual = (Decimal(alfabetizados) * Decimal("100")) / Decimal(total_alunos)
    return percentual.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def create_indicador_trimestral(
    db: Session,
    payload: schemas.IndicadorTrimestralCreate,
) -> models.IndicadorTrimestral:
    indicador = models.IndicadorTrimestral(
        turma_id=payload.turma_id,
        ano=payload.ano,
        trimestre=payload.trimestre,
        total_alunos=payload.total_alunos,
        alfabetizados_leitura=payload.alfabetizados_leitura,
        alfabetizados_escrita=payload.alfabetizados_escrita,
        percentual_leitura=_calculate_percentual(payload.alfabetizados_leitura, payload.total_alunos),
        percentual_escrita=_calculate_percentual(payload.alfabetizados_escrita, payload.total_alunos),
    )
    db.add(indicador)
    db.commit()
    db.refresh(indicador)
    return indicador


def list_indicadores_trimestrais(
    db: Session,
    turma_id: UUID | None = None,
    ano: int | None = None,
    trimestre: int | None = None,
) -> list[models.IndicadorTrimestral]:
    stmt = select(models.IndicadorTrimestral)

    if turma_id:
        stmt = stmt.where(models.IndicadorTrimestral.turma_id == turma_id)
    if ano is not None:
        stmt = stmt.where(models.IndicadorTrimestral.ano == ano)
    if trimestre is not None:
        stmt = stmt.where(models.IndicadorTrimestral.trimestre == trimestre)

    stmt = stmt.order_by(
        models.IndicadorTrimestral.ano.desc(),
        models.IndicadorTrimestral.trimestre.desc(),
    )
    return list(db.scalars(stmt))


def get_indicador_trimestral(
    db: Session,
    indicador_id: UUID,
) -> models.IndicadorTrimestral | None:
    return db.get(models.IndicadorTrimestral, indicador_id)


def update_indicador_trimestral(
    db: Session,
    indicador: models.IndicadorTrimestral,
    payload: schemas.IndicadorTrimestralUpdate,
) -> models.IndicadorTrimestral:
    indicador.turma_id = payload.turma_id
    indicador.ano = payload.ano
    indicador.trimestre = payload.trimestre
    indicador.total_alunos = payload.total_alunos
    indicador.alfabetizados_leitura = payload.alfabetizados_leitura
    indicador.alfabetizados_escrita = payload.alfabetizados_escrita
    indicador.percentual_leitura = _calculate_percentual(
        payload.alfabetizados_leitura,
        payload.total_alunos,
    )
    indicador.percentual_escrita = _calculate_percentual(
        payload.alfabetizados_escrita,
        payload.total_alunos,
    )
    db.commit()
    db.refresh(indicador)
    return indicador


def delete_indicador_trimestral(db: Session, indicador: models.IndicadorTrimestral) -> None:
    db.delete(indicador)
    db.commit()


def _build_ima_base_stmt():
    return (
        select(
            models.IndicadorTrimestral.id.label("indicador_id"),
            models.IndicadorTrimestral.ano,
            models.IndicadorTrimestral.trimestre,
            models.IndicadorTrimestral.total_alunos,
            models.IndicadorTrimestral.alfabetizados_leitura,
            models.IndicadorTrimestral.alfabetizados_escrita,
            models.Turma.id.label("turma_id"),
            models.Turma.nome.label("turma_nome"),
            models.Escola.id.label("escola_id"),
            models.Escola.nome.label("escola_nome"),
            models.Municipio.id.label("municipio_id"),
            models.Municipio.nome.label("municipio_nome"),
            models.Municipio.estado.label("municipio_estado"),
        )
        .select_from(models.IndicadorTrimestral)
        .join(models.Turma, models.IndicadorTrimestral.turma_id == models.Turma.id)
        .join(models.Escola, models.Turma.escola_id == models.Escola.id)
        .join(models.Municipio, models.Escola.municipio_id == models.Municipio.id)
    )


def _apply_ima_filters(
    stmt,
    ano: int | None,
    trimestre: int | None,
    municipio_id: UUID | None,
    escola_id: UUID | None,
    turma_id: UUID | None,
):
    if ano is not None:
        stmt = stmt.where(models.IndicadorTrimestral.ano == ano)
    if trimestre is not None:
        stmt = stmt.where(models.IndicadorTrimestral.trimestre == trimestre)
    if municipio_id is not None:
        stmt = stmt.where(models.Municipio.id == municipio_id)
    if escola_id is not None:
        stmt = stmt.where(models.Escola.id == escola_id)
    if turma_id is not None:
        stmt = stmt.where(models.Turma.id == turma_id)
    return stmt


def _compute_ima_metrics(total_alunos: int, leitura_total: int, escrita_total: int) -> tuple[float, float, float]:
    if total_alunos <= 0:
        return 0.0, 0.0, 0.0

    percentual_leitura = round((leitura_total / total_alunos) * 100, 2)
    percentual_escrita = round((escrita_total / total_alunos) * 100, 2)
    ima_medio = round((percentual_leitura + percentual_escrita) / 2, 2)
    return percentual_leitura, percentual_escrita, ima_medio


def get_analytics_ima(
    db: Session,
    group_by: str = "municipio",
    ano: int | None = None,
    trimestre: int | None = None,
    municipio_id: UUID | None = None,
    escola_id: UUID | None = None,
    turma_id: UUID | None = None,
) -> dict:
    base_stmt = _build_ima_base_stmt()
    base_stmt = _apply_ima_filters(
        base_stmt,
        ano=ano,
        trimestre=trimestre,
        municipio_id=municipio_id,
        escola_id=escola_id,
        turma_id=turma_id,
    )
    rows = db.execute(base_stmt).mappings().all()

    total_registros = len(rows)
    total_alunos = sum(row["total_alunos"] for row in rows)
    leitura_total = sum(row["alfabetizados_leitura"] for row in rows)
    escrita_total = sum(row["alfabetizados_escrita"] for row in rows)
    percentual_leitura, percentual_escrita, ima_medio = _compute_ima_metrics(
        total_alunos,
        leitura_total,
        escrita_total,
    )

    group_key_map = {
        "municipio": ("municipio_id", "municipio_nome", "municipio_estado"),
        "escola": ("escola_id", "escola_nome", None),
        "turma": ("turma_id", "turma_nome", None),
    }
    id_key, name_key, state_key = group_key_map[group_by]

    grouped: dict[UUID, dict] = {}
    for row in rows:
        group_id = row[id_key]
        item = grouped.setdefault(
            group_id,
            {
                "id": group_id,
                "nome": row[name_key],
                "total_registros": 0,
                "total_alunos": 0,
                "leitura_total": 0,
                "escrita_total": 0,
            },
        )
        if state_key:
            item["nome"] = f"{row[name_key]} ({row[state_key]})"
        item["total_registros"] += 1
        item["total_alunos"] += row["total_alunos"]
        item["leitura_total"] += row["alfabetizados_leitura"]
        item["escrita_total"] += row["alfabetizados_escrita"]

    itens = []
    for item in grouped.values():
        p_leitura, p_escrita, ima_item = _compute_ima_metrics(
            item["total_alunos"],
            item["leitura_total"],
            item["escrita_total"],
        )
        itens.append(
            {
                "nivel": group_by,
                "id": item["id"],
                "nome": item["nome"],
                "total_registros": item["total_registros"],
                "total_alunos": item["total_alunos"],
                "percentual_leitura_medio": p_leitura,
                "percentual_escrita_medio": p_escrita,
                "ima_medio": ima_item,
            }
        )

    itens.sort(key=lambda x: x["nome"])

    return {
        "filtros": {
            "group_by": group_by,
            "ano": ano,
            "trimestre": trimestre,
            "municipio_id": municipio_id,
            "escola_id": escola_id,
            "turma_id": turma_id,
        },
        "resumo": {
            "total_registros": total_registros,
            "total_alunos": total_alunos,
            "percentual_leitura_medio": percentual_leitura,
            "percentual_escrita_medio": percentual_escrita,
            "ima_medio": ima_medio,
        },
        "itens": itens,
    }


def _to_float(value: float | Decimal) -> float:
    if isinstance(value, Decimal):
        return float(value)
    return float(value)


def list_bi_hierarquia(
    db: Session,
    municipio_id: UUID | None = None,
    escola_id: UUID | None = None,
    turma_id: UUID | None = None,
    estado: str | None = None,
) -> list[dict]:
    stmt = (
        select(
            models.Municipio.id.label("municipio_id"),
            models.Municipio.nome.label("municipio_nome"),
            models.Municipio.estado.label("municipio_estado"),
            models.Escola.id.label("escola_id"),
            models.Escola.nome.label("escola_nome"),
            models.Turma.id.label("turma_id"),
            models.Turma.nome.label("turma_nome"),
        )
        .select_from(models.Turma)
        .join(models.Escola, models.Turma.escola_id == models.Escola.id)
        .join(models.Municipio, models.Escola.municipio_id == models.Municipio.id)
    )

    if municipio_id is not None:
        stmt = stmt.where(models.Municipio.id == municipio_id)
    if escola_id is not None:
        stmt = stmt.where(models.Escola.id == escola_id)
    if turma_id is not None:
        stmt = stmt.where(models.Turma.id == turma_id)
    if estado:
        stmt = stmt.where(models.Municipio.estado == estado.strip().upper())

    stmt = stmt.order_by(
        models.Municipio.nome,
        models.Escola.nome,
        models.Turma.nome,
    )
    rows = db.execute(stmt).mappings().all()
    return [dict(row) for row in rows]


def _list_bi_indicadores_from_view(
    db: Session,
    municipio_id: UUID | None = None,
    escola_id: UUID | None = None,
    turma_id: UUID | None = None,
    ano: int | None = None,
    trimestre: int | None = None,
) -> list[dict] | None:
    bind = db.get_bind()
    if bind is None or bind.dialect.name != "postgresql":
        return None

    where_clauses: list[str] = []
    params: dict = {}

    if municipio_id is not None:
        where_clauses.append("municipio_id = :municipio_id")
        params["municipio_id"] = str(municipio_id)
    if escola_id is not None:
        where_clauses.append("escola_id = :escola_id")
        params["escola_id"] = str(escola_id)
    if turma_id is not None:
        where_clauses.append("turma_id = :turma_id")
        params["turma_id"] = str(turma_id)
    if ano is not None:
        where_clauses.append("ano = :ano")
        params["ano"] = ano
    if trimestre is not None:
        where_clauses.append("trimestre = :trimestre")
        params["trimestre"] = trimestre

    sql = """
        SELECT
            indicador_id,
            ano,
            trimestre,
            turma_id,
            turma_nome,
            escola_id,
            escola_nome,
            municipio_id,
            municipio_nome,
            municipio_estado,
            total_alunos,
            alfabetizados_leitura,
            alfabetizados_escrita,
            percentual_leitura,
            percentual_escrita,
            ima
        FROM vw_ima
    """
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)

    sql += " ORDER BY ano DESC, trimestre DESC, municipio_nome, escola_nome, turma_nome"

    try:
        rows = db.execute(text(sql), params).mappings().all()
    except Exception:
        # In local/dev environments the view might not exist yet. Fallback to ORM join.
        db.rollback()
        return None

    items: list[dict] = []
    for row in rows:
        items.append(
            {
                "indicador_id": row["indicador_id"],
                "ano": row["ano"],
                "trimestre": row["trimestre"],
                "turma_id": row["turma_id"],
                "turma_nome": row["turma_nome"],
                "escola_id": row["escola_id"],
                "escola_nome": row["escola_nome"],
                "municipio_id": row["municipio_id"],
                "municipio_nome": row["municipio_nome"],
                "municipio_estado": row["municipio_estado"],
                "total_alunos": row["total_alunos"],
                "alfabetizados_leitura": row["alfabetizados_leitura"],
                "alfabetizados_escrita": row["alfabetizados_escrita"],
                "percentual_leitura": round(_to_float(row["percentual_leitura"]), 2),
                "percentual_escrita": round(_to_float(row["percentual_escrita"]), 2),
                "ima": round(_to_float(row["ima"]), 2),
            }
        )
    return items


def list_bi_indicadores_trimestrais(
    db: Session,
    municipio_id: UUID | None = None,
    escola_id: UUID | None = None,
    turma_id: UUID | None = None,
    ano: int | None = None,
    trimestre: int | None = None,
) -> list[dict]:
    view_rows = _list_bi_indicadores_from_view(
        db,
        municipio_id=municipio_id,
        escola_id=escola_id,
        turma_id=turma_id,
        ano=ano,
        trimestre=trimestre,
    )
    if view_rows is not None:
        return view_rows

    stmt = (
        select(
            models.IndicadorTrimestral.id.label("indicador_id"),
            models.IndicadorTrimestral.ano,
            models.IndicadorTrimestral.trimestre,
            models.Turma.id.label("turma_id"),
            models.Turma.nome.label("turma_nome"),
            models.Escola.id.label("escola_id"),
            models.Escola.nome.label("escola_nome"),
            models.Municipio.id.label("municipio_id"),
            models.Municipio.nome.label("municipio_nome"),
            models.Municipio.estado.label("municipio_estado"),
            models.IndicadorTrimestral.total_alunos,
            models.IndicadorTrimestral.alfabetizados_leitura,
            models.IndicadorTrimestral.alfabetizados_escrita,
            models.IndicadorTrimestral.percentual_leitura,
            models.IndicadorTrimestral.percentual_escrita,
        )
        .select_from(models.IndicadorTrimestral)
        .join(models.Turma, models.IndicadorTrimestral.turma_id == models.Turma.id)
        .join(models.Escola, models.Turma.escola_id == models.Escola.id)
        .join(models.Municipio, models.Escola.municipio_id == models.Municipio.id)
    )

    if municipio_id is not None:
        stmt = stmt.where(models.Municipio.id == municipio_id)
    if escola_id is not None:
        stmt = stmt.where(models.Escola.id == escola_id)
    if turma_id is not None:
        stmt = stmt.where(models.Turma.id == turma_id)
    if ano is not None:
        stmt = stmt.where(models.IndicadorTrimestral.ano == ano)
    if trimestre is not None:
        stmt = stmt.where(models.IndicadorTrimestral.trimestre == trimestre)

    stmt = stmt.order_by(
        models.IndicadorTrimestral.ano.desc(),
        models.IndicadorTrimestral.trimestre.desc(),
        models.Municipio.nome,
        models.Escola.nome,
        models.Turma.nome,
    )

    rows = db.execute(stmt).mappings().all()
    items: list[dict] = []
    for row in rows:
        percentual_leitura = round(_to_float(row["percentual_leitura"]), 2)
        percentual_escrita = round(_to_float(row["percentual_escrita"]), 2)
        items.append(
            {
                "indicador_id": row["indicador_id"],
                "ano": row["ano"],
                "trimestre": row["trimestre"],
                "turma_id": row["turma_id"],
                "turma_nome": row["turma_nome"],
                "escola_id": row["escola_id"],
                "escola_nome": row["escola_nome"],
                "municipio_id": row["municipio_id"],
                "municipio_nome": row["municipio_nome"],
                "municipio_estado": row["municipio_estado"],
                "total_alunos": row["total_alunos"],
                "alfabetizados_leitura": row["alfabetizados_leitura"],
                "alfabetizados_escrita": row["alfabetizados_escrita"],
                "percentual_leitura": percentual_leitura,
                "percentual_escrita": percentual_escrita,
                "ima": round((percentual_leitura + percentual_escrita) / 2, 2),
            }
        )
    return items


def get_bi_ima(
    db: Session,
    group_by: str = "municipio",
    ano: int | None = None,
    trimestre: int | None = None,
    municipio_id: UUID | None = None,
    escola_id: UUID | None = None,
    turma_id: UUID | None = None,
) -> dict:
    data = get_analytics_ima(
        db,
        group_by=group_by,
        ano=ano,
        trimestre=trimestre,
        municipio_id=municipio_id,
        escola_id=escola_id,
        turma_id=turma_id,
    )
    return {
        "group_by": group_by,
        "filtros": {
            "ano": ano,
            "trimestre": trimestre,
            "municipio_id": municipio_id,
            "escola_id": escola_id,
            "turma_id": turma_id,
        },
        "resumo": data["resumo"],
        "itens": data["itens"],
    }
