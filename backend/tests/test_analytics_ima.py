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


def _create_indicador(client, turma_id: str, ano: int, trimestre: int, total: int, leitura: int, escrita: int):
    payload = {
        "turma_id": turma_id,
        "ano": ano,
        "trimestre": trimestre,
        "total_alunos": total,
        "alfabetizados_leitura": leitura,
        "alfabetizados_escrita": escrita,
    }
    response = client.post("/indicadores-trimestrais", json=payload)
    assert response.status_code == 201
    return response.json()


def test_analytics_ima_empty_returns_zero(client):
    response = client.get("/analytics/ima")

    assert response.status_code == 200
    data = response.json()
    assert data["resumo"]["total_registros"] == 0
    assert data["resumo"]["total_alunos"] == 0
    assert data["resumo"]["percentual_leitura_medio"] == 0.0
    assert data["resumo"]["percentual_escrita_medio"] == 0.0
    assert data["resumo"]["ima_medio"] == 0.0
    assert data["itens"] == []


def test_analytics_ima_summary_and_group_by_municipio(client):
    m1 = client.post("/municipios", json={"nome": "Mendes", "estado": "RJ"}).json()
    e1 = client.post("/escolas", json={"nome": "Escola A", "municipio_id": m1["id"]}).json()
    e2 = client.post("/escolas", json={"nome": "Escola B", "municipio_id": m1["id"]}).json()
    t1 = client.post("/turmas", json={"nome": "Turma A", "escola_id": e1["id"]}).json()
    t2 = client.post("/turmas", json={"nome": "Turma B", "escola_id": e2["id"]}).json()

    m2, _e3, t3 = _create_hierarchy(client, "Barra", "SP", "Escola C", "Turma C")

    _create_indicador(client, t1["id"], 2026, 1, 10, 5, 6)
    _create_indicador(client, t2["id"], 2026, 1, 20, 10, 8)
    _create_indicador(client, t3["id"], 2026, 1, 10, 9, 9)

    response = client.get("/analytics/ima")

    assert response.status_code == 200
    data = response.json()

    assert data["filtros"]["group_by"] == "municipio"
    assert data["resumo"]["total_registros"] == 3
    assert data["resumo"]["total_alunos"] == 40
    assert data["resumo"]["percentual_leitura_medio"] == pytest.approx(60.0, abs=0.01)
    assert data["resumo"]["percentual_escrita_medio"] == pytest.approx(57.5, abs=0.01)
    assert data["resumo"]["ima_medio"] == pytest.approx(58.75, abs=0.01)

    items_by_name = {item["nome"]: item for item in data["itens"]}
    assert len(items_by_name) == 2

    mendes = items_by_name["Mendes (RJ)"]
    assert mendes["total_registros"] == 2
    assert mendes["total_alunos"] == 30
    assert mendes["percentual_leitura_medio"] == pytest.approx(50.0, abs=0.01)
    assert mendes["percentual_escrita_medio"] == pytest.approx(46.67, abs=0.01)
    assert mendes["ima_medio"] == pytest.approx(48.34, abs=0.01)

    barra = items_by_name["Barra (SP)"]
    assert barra["total_registros"] == 1
    assert barra["total_alunos"] == 10
    assert barra["percentual_leitura_medio"] == pytest.approx(90.0, abs=0.01)
    assert barra["percentual_escrita_medio"] == pytest.approx(90.0, abs=0.01)
    assert barra["ima_medio"] == pytest.approx(90.0, abs=0.01)


def test_analytics_ima_filter_by_period(client):
    _m, _e, t = _create_hierarchy(client, "Mendes", "RJ", "Escola A", "Turma A")

    _create_indicador(client, t["id"], 2026, 1, 20, 10, 8)
    _create_indicador(client, t["id"], 2025, 4, 20, 20, 20)

    response = client.get("/analytics/ima?ano=2025&trimestre=4&group_by=turma")

    assert response.status_code == 200
    data = response.json()
    assert data["resumo"]["total_registros"] == 1
    assert data["resumo"]["total_alunos"] == 20
    assert data["resumo"]["percentual_leitura_medio"] == pytest.approx(100.0, abs=0.01)
    assert data["resumo"]["percentual_escrita_medio"] == pytest.approx(100.0, abs=0.01)
    assert data["resumo"]["ima_medio"] == pytest.approx(100.0, abs=0.01)


def test_analytics_ima_group_by_escola_and_turma(client):
    _m1, e1, t1 = _create_hierarchy(client, "Mendes", "RJ", "Escola A", "Turma A")
    _m1b, e2, t2 = _create_hierarchy(client, "Mendes", "RJ", "Escola B", "Turma B")

    _create_indicador(client, t1["id"], 2026, 1, 10, 5, 6)
    _create_indicador(client, t2["id"], 2026, 1, 10, 8, 9)

    by_escola = client.get("/analytics/ima?group_by=escola")
    assert by_escola.status_code == 200
    data_escola = by_escola.json()
    assert len(data_escola["itens"]) == 2
    ids_escola = {item["id"] for item in data_escola["itens"]}
    assert e1["id"] in ids_escola
    assert e2["id"] in ids_escola

    by_turma = client.get("/analytics/ima?group_by=turma")
    assert by_turma.status_code == 200
    data_turma = by_turma.json()
    assert len(data_turma["itens"]) == 2
    ids_turma = {item["id"] for item in data_turma["itens"]}
    assert t1["id"] in ids_turma
    assert t2["id"] in ids_turma


def test_analytics_ima_filter_by_municipio_id(client):
    m1, _e1, t1 = _create_hierarchy(client, "Mendes", "RJ", "Escola A", "Turma A")
    _m2, _e2, t2 = _create_hierarchy(client, "Barra", "SP", "Escola B", "Turma B")

    _create_indicador(client, t1["id"], 2026, 1, 20, 10, 8)
    _create_indicador(client, t2["id"], 2026, 1, 20, 20, 20)

    response = client.get(f"/analytics/ima?municipio_id={m1['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["resumo"]["total_registros"] == 1
    assert data["resumo"]["total_alunos"] == 20
    assert data["resumo"]["percentual_leitura_medio"] == pytest.approx(50.0, abs=0.01)
    assert data["resumo"]["percentual_escrita_medio"] == pytest.approx(40.0, abs=0.01)
    assert data["resumo"]["ima_medio"] == pytest.approx(45.0, abs=0.01)


def test_analytics_ima_invalid_group_by_returns_422(client):
    response = client.get("/analytics/ima?group_by=rede")

    assert response.status_code == 422
