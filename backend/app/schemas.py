from uuid import UUID
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class _NomeMixin(BaseModel):
    nome: str = Field(..., min_length=1)

    @field_validator("nome")
    @classmethod
    def validate_nome(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("nome nao pode ser vazio")
        return normalized


class MunicipioBase(_NomeMixin):
    nome: str = Field(..., min_length=1, max_length=150)
    estado: str = Field(..., min_length=2, max_length=2)

    @field_validator("estado")
    @classmethod
    def validate_estado(cls, value: str) -> str:
        normalized = value.strip().upper()
        if len(normalized) != 2 or not normalized.isalpha():
            raise ValueError("estado deve ter exatamente 2 letras")
        return normalized


class MunicipioCreate(MunicipioBase):
    pass


class MunicipioUpdate(MunicipioBase):
    pass


class MunicipioRead(MunicipioBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class EscolaBase(_NomeMixin):
    nome: str = Field(..., min_length=1, max_length=200)
    municipio_id: UUID


class EscolaCreate(EscolaBase):
    pass


class EscolaUpdate(EscolaBase):
    pass


class EscolaRead(EscolaBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class TurmaBase(_NomeMixin):
    nome: str = Field(..., min_length=1, max_length=50)
    escola_id: UUID


class TurmaCreate(TurmaBase):
    pass


class TurmaUpdate(TurmaBase):
    pass


class TurmaRead(TurmaBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class IndicadorTrimestralBase(BaseModel):
    turma_id: UUID
    ano: int = Field(..., ge=2000, le=2100)
    trimestre: int = Field(..., ge=1, le=4)
    total_alunos: int = Field(..., ge=0)
    alfabetizados_leitura: int = Field(..., ge=0)
    alfabetizados_escrita: int = Field(..., ge=0)

    @model_validator(mode="after")
    def validate_totais(self):
        if self.alfabetizados_leitura > self.total_alunos:
            raise ValueError("alfabetizados_leitura nao pode ser maior que total_alunos")
        if self.alfabetizados_escrita > self.total_alunos:
            raise ValueError("alfabetizados_escrita nao pode ser maior que total_alunos")
        return self


class IndicadorTrimestralCreate(IndicadorTrimestralBase):
    pass


class IndicadorTrimestralUpdate(IndicadorTrimestralBase):
    pass


class IndicadorTrimestralRead(IndicadorTrimestralBase):
    id: UUID
    percentual_leitura: float
    percentual_escrita: float

    model_config = ConfigDict(from_attributes=True)


class BIHierarquiaItem(BaseModel):
    municipio_id: UUID
    municipio_nome: str
    municipio_estado: str
    escola_id: UUID
    escola_nome: str
    turma_id: UUID
    turma_nome: str


class BIIndicadorTrimestralItem(BaseModel):
    indicador_id: UUID
    ano: int
    trimestre: int
    turma_id: UUID
    turma_nome: str
    escola_id: UUID
    escola_nome: str
    municipio_id: UUID
    municipio_nome: str
    municipio_estado: str
    total_alunos: int
    alfabetizados_leitura: int
    alfabetizados_escrita: int
    percentual_leitura: float
    percentual_escrita: float
    ima: float


class IMAAnalyticsFiltros(BaseModel):
    group_by: Literal["municipio", "escola", "turma"]
    ano: int | None = None
    trimestre: int | None = None
    municipio_id: UUID | None = None
    escola_id: UUID | None = None
    turma_id: UUID | None = None


class IMAAnalyticsResumo(BaseModel):
    total_registros: int
    total_alunos: int
    percentual_leitura_medio: float
    percentual_escrita_medio: float
    ima_medio: float


class IMAAnalyticsItem(BaseModel):
    nivel: Literal["municipio", "escola", "turma"]
    id: UUID
    nome: str
    total_registros: int
    total_alunos: int
    percentual_leitura_medio: float
    percentual_escrita_medio: float
    ima_medio: float


class IMAAnalyticsResponse(BaseModel):
    filtros: IMAAnalyticsFiltros
    resumo: IMAAnalyticsResumo
    itens: list[IMAAnalyticsItem]


class BIIMAFiltros(BaseModel):
    ano: int | None = None
    trimestre: int | None = None
    municipio_id: UUID | None = None
    escola_id: UUID | None = None
    turma_id: UUID | None = None


class BIIMAResumo(BaseModel):
    total_registros: int
    total_alunos: int
    percentual_leitura_medio: float
    percentual_escrita_medio: float
    ima_medio: float


class BIIMAItem(BaseModel):
    nivel: Literal["municipio", "escola", "turma"]
    id: UUID
    nome: str
    total_registros: int
    total_alunos: int
    percentual_leitura_medio: float
    percentual_escrita_medio: float
    ima_medio: float


class BIIMAResponse(BaseModel):
    group_by: Literal["municipio", "escola", "turma"]
    filtros: BIIMAFiltros
    resumo: BIIMAResumo
    itens: list[BIIMAItem]
