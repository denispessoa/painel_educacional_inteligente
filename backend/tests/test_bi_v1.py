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


def test_bi_hierarquia_empty_returns_200_and_empty_list(client):
    response = client.get("/bi/v1/hierarquia")

    assert response.status_code == 200
    assert response.json() == []


def test_bi_hierarquia_returns_complete_rows_and_ordered(client):
    _m2, _e2, _t2 = _create_hierarchy(client, "Zeta", "RJ", "Escola Z", "Turma Z")
    m1, e1, t1 = _create_hierarchy(client, "Alfa", "SP", "Escola A", "Turma A")

    response = client.get("/bi/v1/hierarquia")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["municipio_nome"] == "Alfa"
    assert data[0]["escola_nome"] == "Escola A"
    assert data[0]["turma_nome"] == "Turma A"
    assert data[0]["municipio_estado"] == "SP"
    assert data[0]["municipio_id"] == m1["id"]
    assert data[0]["escola_id"] == e1["id"]
    assert data[0]["turma_id"] == t1["id"]


def test_bi_hierarquia_invalid_estado_returns_422(client):
    response = client.get("/bi/v1/hierarquia?estado=R")

    assert response.status_code == 422


def test_bi_indicadores_trimestrais_returns_contract_fields_with_ima(client):
    _m, _e, turma = _create_hierarchy(client, "Mendes", "RJ", "Escola A", "Turma A")
    _create_indicador(client, turma["id"], 2026, 1, 20, 8, 10)

    response = client.get("/bi/v1/indicadores-trimestrais")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    item = data[0]
    assert item["ano"] == 2026
    assert item["trimestre"] == 1
    assert item["turma_id"] == turma["id"]
    assert item["percentual_leitura"] == 40.0
    assert item["percentual_escrita"] == 50.0
    assert item["ima"] == 45.0
    assert "municipio_nome" in item
    assert "escola_nome" in item
    assert "turma_nome" in item
    assert "indicador_id" in item


def test_bi_indicadores_trimestrais_filter_by_ano_trimestre(client):
    _m, _e, turma = _create_hierarchy(client, "Mendes", "RJ", "Escola A", "Turma A")
    _create_indicador(client, turma["id"], 2026, 1, 20, 10, 10)
    _create_indicador(client, turma["id"], 2026, 2, 20, 8, 8)

    response = client.get("/bi/v1/indicadores-trimestrais?ano=2026&trimestre=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["ano"] == 2026
    assert data[0]["trimestre"] == 2


def test_bi_indicadores_trimestrais_invalid_trimestre_returns_422(client):
    response = client.get("/bi/v1/indicadores-trimestrais?trimestre=5")

    assert response.status_code == 422


def test_bi_ima_returns_expected_shape(client):
    _m, _e, turma = _create_hierarchy(client, "Mendes", "RJ", "Escola A", "Turma A")
    _create_indicador(client, turma["id"], 2026, 1, 20, 10, 8)

    response = client.get("/bi/v1/ima?group_by=turma")

    assert response.status_code == 200
    data = response.json()
    assert data["group_by"] == "turma"
    assert "filtros" in data
    assert "group_by" not in data["filtros"]
    assert "resumo" in data
    assert "itens" in data
    assert len(data["itens"]) == 1


def test_bi_ima_invalid_group_by_returns_422(client):
    response = client.get("/bi/v1/ima?group_by=rede")

    assert response.status_code == 422


def test_bi_endpoints_do_not_return_404_when_empty(client):
    indicadores = client.get("/bi/v1/indicadores-trimestrais?ano=2026&trimestre=1")
    ima = client.get("/bi/v1/ima?ano=2026&trimestre=1")

    assert indicadores.status_code == 200
    assert indicadores.json() == []
    assert ima.status_code == 200
    assert ima.json()["resumo"]["total_registros"] == 0
    assert ima.json()["itens"] == []
