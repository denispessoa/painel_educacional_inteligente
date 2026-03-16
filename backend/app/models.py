import uuid
from decimal import Decimal

from sqlalchemy import CHAR, CheckConstraint, ForeignKey, Index, Numeric, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Municipio(Base):
    __tablename__ = "municipios"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    estado: Mapped[str] = mapped_column(CHAR(2), nullable=False)

    escolas: Mapped[list["Escola"]] = relationship(back_populates="municipio")


class Escola(Base):
    __tablename__ = "escolas"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    municipio_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("municipios.id", ondelete="RESTRICT"),
        nullable=False,
    )
    nome: Mapped[str] = mapped_column(String(200), nullable=False)

    municipio: Mapped["Municipio"] = relationship(back_populates="escolas")
    turmas: Mapped[list["Turma"]] = relationship(back_populates="escola")


class Turma(Base):
    __tablename__ = "turmas"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    escola_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("escolas.id", ondelete="RESTRICT"),
        nullable=False,
    )
    nome: Mapped[str] = mapped_column(String(50), nullable=False)

    escola: Mapped["Escola"] = relationship(back_populates="turmas")
    indicadores_trimestrais: Mapped[list["IndicadorTrimestral"]] = relationship(
        back_populates="turma"
    )


class IndicadorTrimestral(Base):
    __tablename__ = "indicadores_trimestrais"
    __table_args__ = (
        CheckConstraint("ano >= 2000 AND ano <= 2100", name="ck_indicadores_ano"),
        CheckConstraint("trimestre >= 1 AND trimestre <= 4", name="ck_indicadores_trimestre"),
        CheckConstraint("total_alunos >= 0", name="ck_indicadores_total_alunos"),
        CheckConstraint(
            "alfabetizados_leitura >= 0 AND alfabetizados_leitura <= total_alunos",
            name="ck_indicadores_alfabetizados_leitura",
        ),
        CheckConstraint(
            "alfabetizados_escrita >= 0 AND alfabetizados_escrita <= total_alunos",
            name="ck_indicadores_alfabetizados_escrita",
        ),
        CheckConstraint(
            "percentual_leitura >= 0 AND percentual_leitura <= 100",
            name="ck_indicadores_percentual_leitura",
        ),
        CheckConstraint(
            "percentual_escrita >= 0 AND percentual_escrita <= 100",
            name="ck_indicadores_percentual_escrita",
        ),
        UniqueConstraint("turma_id", "ano", "trimestre", name="uq_indicadores_turma_ano_trimestre"),
        Index("idx_indicadores_turma_id", "turma_id"),
        Index("idx_indicadores_ano_trimestre", "ano", "trimestre"),
        Index("idx_indicadores_turma_ano_trimestre", "turma_id", "ano", "trimestre"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    turma_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("turmas.id", ondelete="RESTRICT"),
        nullable=False,
    )
    ano: Mapped[int] = mapped_column(nullable=False)
    trimestre: Mapped[int] = mapped_column(nullable=False)
    total_alunos: Mapped[int] = mapped_column(nullable=False)
    alfabetizados_leitura: Mapped[int] = mapped_column(nullable=False)
    alfabetizados_escrita: Mapped[int] = mapped_column(nullable=False)
    percentual_leitura: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    percentual_escrita: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)

    turma: Mapped["Turma"] = relationship(back_populates="indicadores_trimestrais")
