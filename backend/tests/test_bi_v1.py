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
    ano: int = 2026,
    trimestre: int = 1,
    ano_escolar: int = 1,
    fonte_avaliacao: str = "cnca",
    total: int = 20,
    leitura: int = 8,
    escrita: int = 10,
    matematica: int = 12,
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
    _create_indicador(client, turma["id"], ano_escolar=2, fonte_avaliacao="cnca")

    response = client.get("/bi/v1/indicadores-trimestrais")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    item = data[0]
    assert item["ano"] == 2026
    assert item["trimestre"] == 1
    assert item["ano_escolar"] == 2
    assert item["fonte_avaliacao"] == "cnca"
    assert item["turma_id"] == turma["id"]
    assert item["percentual_leitura"] == 40.0
    assert item["percentual_escrita"] == 50.0
    assert item["percentual_matematica"] == 60.0
    assert item["ima"] == 45.0


def test_bi_indicadores_trimestrais_filter_by_new_dimensions(client):
    _m, _e, turma = _create_hierarchy(client, "Mendes", "RJ", "Escola A", "Turma A")
    _create_indicador(client, turma["id"], ano=2026, trimestre=1, ano_escolar=2, fonte_avaliacao="cnca")
    _create_indicador(client, turma["id"], ano=2026, trimestre=2, ano_escolar=7, fonte_avaliacao="mec_anos_finais_bncc")

    response = client.get(
        "/bi/v1/indicadores-trimestrais?ano=2026&trimestre=2&ano_escolar=7&fonte_avaliacao=mec_anos_finais_bncc"
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["trimestre"] == 2
    assert data[0]["ano_escolar"] == 7


def test_bi_indicadores_trimestrais_invalid_trimestre_returns_422(client):
    response = client.get("/bi/v1/indicadores-trimestrais?trimestre=5")

    assert response.status_code == 422


def test_bi_indicadores_componentes_returns_component_contract(client):
    _m, _e, turma = _create_hierarchy(client, "Mendes", "RJ", "Escola A", "Turma A")
    _create_indicador(client, turma["id"], ano_escolar=6, fonte_avaliacao="mec_anos_finais_bncc")

    response = client.get("/bi/v1/indicadores-componentes")

    assert response.status_code == 200
    item = response.json()[0]
    assert item["ano_escolar"] == 6
    assert item["fonte_avaliacao"] == "mec_anos_finais_bncc"
    assert item["atingiu_esperado_leitura"] == 8
    assert item["atingiu_esperado_escrita"] == 10
    assert item["atingiu_esperado_matematica"] == 12
    assert item["percentual_matematica"] == 60.0


def test_bi_ima_returns_expected_shape(client):
    _m, _e, turma = _create_hierarchy(client, "Mendes", "RJ", "Escola A", "Turma A")
    _create_indicador(client, turma["id"], ano_escolar=2, fonte_avaliacao="cnca")

    response = client.get("/bi/v1/ima?group_by=turma")

    assert response.status_code == 200
    data = response.json()
    assert data["group_by"] == "turma"
    assert "filtros" in data
    assert "group_by" not in data["filtros"]
    assert "resumo" in data
    assert "itens" in data
    assert len(data["itens"]) == 1


def test_bi_desempenho_returns_expected_shape(client):
    _m, _e, turma = _create_hierarchy(client, "Mendes", "RJ", "Escola A", "Turma A")
    _create_indicador(client, turma["id"], ano_escolar=8, fonte_avaliacao="mec_anos_finais_bncc", total=20, leitura=10, escrita=12, matematica=14)

    response = client.get("/bi/v1/desempenho?group_by=turma&ano_escolar=8&fonte_avaliacao=mec_anos_finais_bncc")

    assert response.status_code == 200
    data = response.json()
    assert data["group_by"] == "turma"
    assert data["resumo"]["percentual_leitura_no_esperado"] == 50.0
    assert data["resumo"]["percentual_escrita_no_esperado"] == 60.0
    assert data["resumo"]["percentual_matematica_no_esperado"] == 70.0
    assert len(data["itens"]) == 1


def test_bi_ima_invalid_group_by_returns_422(client):
    response = client.get("/bi/v1/ima?group_by=rede")

    assert response.status_code == 422


def test_bi_endpoints_do_not_return_404_when_empty(client):
    indicadores = client.get("/bi/v1/indicadores-trimestrais?ano=2026&trimestre=1")
    componentes = client.get("/bi/v1/indicadores-componentes?ano=2026&trimestre=1")
    ima = client.get("/bi/v1/ima?ano=2026&trimestre=1")
    desempenho = client.get("/bi/v1/desempenho?ano=2026&trimestre=1")

    assert indicadores.status_code == 200
    assert indicadores.json() == []
    assert componentes.status_code == 200
    assert componentes.json() == []
    assert ima.status_code == 200
    assert ima.json()["resumo"]["total_registros"] == 0
    assert ima.json()["itens"] == []
    assert desempenho.status_code == 200
    assert desempenho.json()["resumo"]["total_registros"] == 0
    assert desempenho.json()["itens"] == []
