from typing import Literal
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator, model_validator

FonteAvaliacao = Literal["cnca", "mec_anos_finais_bncc"]
GroupBy = Literal["municipio", "escola", "turma"]


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
    ano_escolar: int = Field(..., ge=1, le=9)
    fonte_avaliacao: FonteAvaliacao
    total_alunos: int = Field(..., ge=0)
    atingiu_esperado_leitura: int = Field(
        ...,
        ge=0,
        validation_alias=AliasChoices("atingiu_esperado_leitura", "alfabetizados_leitura"),
    )
    atingiu_esperado_escrita: int = Field(
        ...,
        ge=0,
        validation_alias=AliasChoices("atingiu_esperado_escrita", "alfabetizados_escrita"),
    )
    atingiu_esperado_matematica: int = Field(..., ge=0)

    @field_validator("fonte_avaliacao")
    @classmethod
    def validate_fonte_avaliacao(cls, value: str) -> str:
        return value.strip().lower()

    @model_validator(mode="after")
    def validate_totais_e_fonte(self):
        if self.atingiu_esperado_leitura > self.total_alunos:
            raise ValueError("atingiu_esperado_leitura nao pode ser maior que total_alunos")
        if self.atingiu_esperado_escrita > self.total_alunos:
            raise ValueError("atingiu_esperado_escrita nao pode ser maior que total_alunos")
        if self.atingiu_esperado_matematica > self.total_alunos:
            raise ValueError("atingiu_esperado_matematica nao pode ser maior que total_alunos")

        if self.fonte_avaliacao == "cnca" and not 1 <= self.ano_escolar <= 5:
            raise ValueError("fonte_avaliacao cnca so pode ser usada do 1o ao 5o ano")
        if self.fonte_avaliacao == "mec_anos_finais_bncc" and not 6 <= self.ano_escolar <= 9:
            raise ValueError(
                "fonte_avaliacao mec_anos_finais_bncc so pode ser usada do 6o ao 9o ano"
            )

        return self


class IndicadorTrimestralCreate(IndicadorTrimestralBase):
    pass


class IndicadorTrimestralUpdate(IndicadorTrimestralBase):
    pass


class IndicadorTrimestralRead(IndicadorTrimestralBase):
    id: UUID
    alfabetizados_leitura: int
    alfabetizados_escrita: int
    percentual_leitura: float
    percentual_escrita: float
    percentual_matematica: float

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


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
    ano_escolar: int
    fonte_avaliacao: FonteAvaliacao
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
    atingiu_esperado_matematica: int
    percentual_matematica: float
    ima: float


class BIIndicadorComponenteItem(BaseModel):
    indicador_id: UUID
    ano: int
    trimestre: int
    ano_escolar: int
    fonte_avaliacao: FonteAvaliacao
    turma_id: UUID
    turma_nome: str
    escola_id: UUID
    escola_nome: str
    municipio_id: UUID
    municipio_nome: str
    municipio_estado: str
    total_alunos: int
    atingiu_esperado_leitura: int
    atingiu_esperado_escrita: int
    atingiu_esperado_matematica: int
    percentual_leitura: float
    percentual_escrita: float
    percentual_matematica: float


class IMAAnalyticsFiltros(BaseModel):
    group_by: GroupBy
    ano: int | None = None
    trimestre: int | None = None
    ano_escolar: int | None = None
    fonte_avaliacao: FonteAvaliacao | None = None
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
    nivel: GroupBy
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


class DesempenhoAnalyticsFiltros(BaseModel):
    group_by: GroupBy
    ano: int | None = None
    trimestre: int | None = None
    ano_escolar: int | None = None
    fonte_avaliacao: FonteAvaliacao | None = None
    municipio_id: UUID | None = None
    escola_id: UUID | None = None
    turma_id: UUID | None = None


class DesempenhoAnalyticsResumo(BaseModel):
    total_registros: int
    total_alunos: int
    percentual_leitura_no_esperado: float
    percentual_escrita_no_esperado: float
    percentual_matematica_no_esperado: float


class DesempenhoAnalyticsItem(BaseModel):
    nivel: GroupBy
    id: UUID
    nome: str
    total_registros: int
    total_alunos: int
    percentual_leitura_no_esperado: float
    percentual_escrita_no_esperado: float
    percentual_matematica_no_esperado: float


class DesempenhoAnalyticsResponse(BaseModel):
    filtros: DesempenhoAnalyticsFiltros
    resumo: DesempenhoAnalyticsResumo
    itens: list[DesempenhoAnalyticsItem]


class BIIMAFiltros(BaseModel):
    ano: int | None = None
    trimestre: int | None = None
    ano_escolar: int | None = None
    fonte_avaliacao: FonteAvaliacao | None = None
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
    nivel: GroupBy
    id: UUID
    nome: str
    total_registros: int
    total_alunos: int
    percentual_leitura_medio: float
    percentual_escrita_medio: float
    ima_medio: float


class BIIMAResponse(BaseModel):
    group_by: GroupBy
    filtros: BIIMAFiltros
    resumo: BIIMAResumo
    itens: list[BIIMAItem]


class BIDesempenhoFiltros(BaseModel):
    ano: int | None = None
    trimestre: int | None = None
    ano_escolar: int | None = None
    fonte_avaliacao: FonteAvaliacao | None = None
    municipio_id: UUID | None = None
    escola_id: UUID | None = None
    turma_id: UUID | None = None


class BIDesempenhoResumo(BaseModel):
    total_registros: int
    total_alunos: int
    percentual_leitura_no_esperado: float
    percentual_escrita_no_esperado: float
    percentual_matematica_no_esperado: float


class BIDesempenhoItem(BaseModel):
    nivel: GroupBy
    id: UUID
    nome: str
    total_registros: int
    total_alunos: int
    percentual_leitura_no_esperado: float
    percentual_escrita_no_esperado: float
    percentual_matematica_no_esperado: float


class BIDesempenhoResponse(BaseModel):
    group_by: GroupBy
    filtros: BIDesempenhoFiltros
    resumo: BIDesempenhoResumo
    itens: list[BIDesempenhoItem]
