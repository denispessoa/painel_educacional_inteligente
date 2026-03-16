import pytest


def _create_hierarchy(client, municipio_nome: str, estado: str, escola_nome: str, turma_nome: str):
    municipio = client.post("/municipios", json={"nome": municipio_nome, "estado": estado}).json()
    escola = client.post(
        "/escolas",
        json={"nome": escola_nome, "municipio_id": municipio["id"]},
    ).json()
    turma = client.post(
        "/turmas",
        json={"nome": turma_nome, "escola_id": escola["id"]},
    ).json()
    return municipio, escola, turma


def _create_indicador(
    client,
    turma_id: str,
    *,
    ano: int,
    trimestre: int,
    ano_escolar: int,
    fonte_avaliacao: str,
    total: int,
    leitura: int,
    escrita: int,
    matematica: int,
):
    response = client.post(
        "/indicadores-trimestrais",
        json={
            "turma_id": turma_id,
            "ano": ano,
            "trimestre": trimestre,
            "ano_escolar": ano_escolar,
            "fonte_avaliacao": fonte_avaliacao,
            "total_alunos": total,
            "atingiu_esperado_leitura": leitura,
            "atingiu_esperado_escrita": escrita,
            "atingiu_esperado_matematica": matematica,
        },
    )
    assert response.status_code == 201


def test_analytics_desempenho_empty_returns_zero(client):
    response = client.get("/analytics/desempenho")

    assert response.status_code == 200
    data = response.json()
    assert data["resumo"]["total_registros"] == 0
    assert data["resumo"]["total_alunos"] == 0
    assert data["resumo"]["percentual_leitura_no_esperado"] == 0.0
    assert data["resumo"]["percentual_escrita_no_esperado"] == 0.0
    assert data["resumo"]["percentual_matematica_no_esperado"] == 0.0
    assert data["itens"] == []


def test_analytics_desempenho_summary_and_filters(client):
    _m, _e, turma = _create_hierarchy(client, "Mendes", "RJ", "Escola A", "Turma A")
    _create_indicador(client, turma["id"], ano=2026, trimestre=1, ano_escolar=1, fonte_avaliacao="cnca", total=20, leitura=8, escrita=10, matematica=12)
    _create_indicador(client, turma["id"], ano=2026, trimestre=2, ano_escolar=6, fonte_avaliacao="mec_anos_finais_bncc", total=30, leitura=15, escrita=18, matematica=21)

    response = client.get("/analytics/desempenho?ano=2026&trimestre=2&ano_escolar=6&fonte_avaliacao=mec_anos_finais_bncc&group_by=turma")

    assert response.status_code == 200
    data = response.json()
    assert data["filtros"]["group_by"] == "turma"
    assert data["resumo"]["total_registros"] == 1
    assert data["resumo"]["total_alunos"] == 30
    assert data["resumo"]["percentual_leitura_no_esperado"] == pytest.approx(50.0, abs=0.01)
    assert data["resumo"]["percentual_escrita_no_esperado"] == pytest.approx(60.0, abs=0.01)
    assert data["resumo"]["percentual_matematica_no_esperado"] == pytest.approx(70.0, abs=0.01)
    assert len(data["itens"]) == 1
    assert data["itens"][0]["nome"] == "Turma A"


def test_analytics_desempenho_group_by_municipio(client):
    _m1, _e1, t1 = _create_hierarchy(client, "Mendes", "RJ", "Escola A", "Turma A")
    _m2, _e2, t2 = _create_hierarchy(client, "Barra", "SP", "Escola B", "Turma B")

    _create_indicador(client, t1["id"], ano=2026, trimestre=1, ano_escolar=2, fonte_avaliacao="cnca", total=20, leitura=10, escrita=12, matematica=14)
    _create_indicador(client, t2["id"], ano=2026, trimestre=1, ano_escolar=8, fonte_avaliacao="mec_anos_finais_bncc", total=10, leitura=8, escrita=7, matematica=9)

    response = client.get("/analytics/desempenho?group_by=municipio")

    assert response.status_code == 200
    data = response.json()
    items = {item["nome"]: item for item in data["itens"]}
    assert items["Barra (SP)"]["percentual_matematica_no_esperado"] == pytest.approx(90.0, abs=0.01)
    assert items["Mendes (RJ)"]["percentual_leitura_no_esperado"] == pytest.approx(50.0, abs=0.01)


def test_analytics_desempenho_invalid_group_by_returns_422(client):
    response = client.get("/analytics/desempenho?group_by=rede")

    assert response.status_code == 422
