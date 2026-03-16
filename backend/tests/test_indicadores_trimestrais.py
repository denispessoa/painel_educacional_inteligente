def _create_turma(client):
    municipio = client.post("/municipios", json={"nome": "Mendes", "estado": "RJ"}).json()
    escola = client.post(
        "/escolas",
        json={"nome": "Escola A", "municipio_id": municipio["id"]},
    ).json()
    turma = client.post(
        "/turmas",
        json={"nome": "Turma A", "escola_id": escola["id"]},
    ).json()
    return turma


def test_create_indicador_trimestral_success(client):
    turma = _create_turma(client)
    payload = {
        "turma_id": turma["id"],
        "ano": 2026,
        "trimestre": 1,
        "total_alunos": 20,
        "alfabetizados_leitura": 8,
        "alfabetizados_escrita": 10,
    }

    response = client.post("/indicadores-trimestrais", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["turma_id"] == turma["id"]
    assert data["percentual_leitura"] == 40.0
    assert data["percentual_escrita"] == 50.0


def test_create_indicador_trimestral_total_zero_sets_percentual_zero(client):
    turma = _create_turma(client)
    payload = {
        "turma_id": turma["id"],
        "ano": 2026,
        "trimestre": 2,
        "total_alunos": 0,
        "alfabetizados_leitura": 0,
        "alfabetizados_escrita": 0,
    }

    response = client.post("/indicadores-trimestrais", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["percentual_leitura"] == 0.0
    assert data["percentual_escrita"] == 0.0


def test_create_indicador_trimestral_invalid_trimestre_returns_422(client):
    turma = _create_turma(client)
    payload = {
        "turma_id": turma["id"],
        "ano": 2026,
        "trimestre": 5,
        "total_alunos": 20,
        "alfabetizados_leitura": 8,
        "alfabetizados_escrita": 10,
    }

    response = client.post("/indicadores-trimestrais", json=payload)

    assert response.status_code == 422


def test_create_indicador_trimestral_leitura_gt_total_returns_422(client):
    turma = _create_turma(client)
    payload = {
        "turma_id": turma["id"],
        "ano": 2026,
        "trimestre": 1,
        "total_alunos": 20,
        "alfabetizados_leitura": 21,
        "alfabetizados_escrita": 10,
    }

    response = client.post("/indicadores-trimestrais", json=payload)

    assert response.status_code == 422


def test_create_indicador_trimestral_with_missing_turma_returns_409(client):
    payload = {
        "turma_id": "0f57af7e-e7ce-4e9c-b5c9-b45e3df85801",
        "ano": 2026,
        "trimestre": 1,
        "total_alunos": 20,
        "alfabetizados_leitura": 8,
        "alfabetizados_escrita": 10,
    }

    response = client.post("/indicadores-trimestrais", json=payload)

    assert response.status_code == 409


def test_create_indicador_trimestral_duplicate_period_returns_409(client):
    turma = _create_turma(client)
    payload = {
        "turma_id": turma["id"],
        "ano": 2026,
        "trimestre": 1,
        "total_alunos": 20,
        "alfabetizados_leitura": 8,
        "alfabetizados_escrita": 10,
    }

    first = client.post("/indicadores-trimestrais", json=payload)
    second = client.post("/indicadores-trimestrais", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409


def test_list_indicadores_trimestrais_filtered_by_turma(client):
    turma_1 = _create_turma(client)
    turma_2 = _create_turma(client)
    payload_1 = {
        "turma_id": turma_1["id"],
        "ano": 2026,
        "trimestre": 1,
        "total_alunos": 20,
        "alfabetizados_leitura": 8,
        "alfabetizados_escrita": 10,
    }
    payload_2 = {
        "turma_id": turma_2["id"],
        "ano": 2026,
        "trimestre": 1,
        "total_alunos": 22,
        "alfabetizados_leitura": 11,
        "alfabetizados_escrita": 12,
    }

    client.post("/indicadores-trimestrais", json=payload_1)
    client.post("/indicadores-trimestrais", json=payload_2)

    response = client.get(f"/indicadores-trimestrais?turma_id={turma_1['id']}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["turma_id"] == turma_1["id"]


def test_list_indicadores_trimestrais_filtered_by_ano_trimestre(client):
    turma = _create_turma(client)
    payload_1 = {
        "turma_id": turma["id"],
        "ano": 2026,
        "trimestre": 1,
        "total_alunos": 20,
        "alfabetizados_leitura": 8,
        "alfabetizados_escrita": 10,
    }
    payload_2 = {
        "turma_id": turma["id"],
        "ano": 2025,
        "trimestre": 4,
        "total_alunos": 20,
        "alfabetizados_leitura": 8,
        "alfabetizados_escrita": 10,
    }

    client.post("/indicadores-trimestrais", json=payload_1)
    client.post("/indicadores-trimestrais", json=payload_2)

    response = client.get("/indicadores-trimestrais?ano=2026&trimestre=1")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["ano"] == 2026
    assert data[0]["trimestre"] == 1


def test_get_indicador_trimestral_not_found_returns_404(client):
    response = client.get("/indicadores-trimestrais/0f57af7e-e7ce-4e9c-b5c9-b45e3df85801")

    assert response.status_code == 404


def test_update_indicador_trimestral_success_recalculates_percentuais(client):
    turma = _create_turma(client)
    payload = {
        "turma_id": turma["id"],
        "ano": 2026,
        "trimestre": 1,
        "total_alunos": 20,
        "alfabetizados_leitura": 8,
        "alfabetizados_escrita": 10,
    }
    created = client.post("/indicadores-trimestrais", json=payload).json()

    update_payload = {
        "turma_id": turma["id"],
        "ano": 2026,
        "trimestre": 2,
        "total_alunos": 30,
        "alfabetizados_leitura": 6,
        "alfabetizados_escrita": 9,
    }
    response = client.put(f"/indicadores-trimestrais/{created['id']}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["trimestre"] == 2
    assert data["percentual_leitura"] == 20.0
    assert data["percentual_escrita"] == 30.0


def test_delete_indicador_trimestral_success_returns_204(client):
    turma = _create_turma(client)
    payload = {
        "turma_id": turma["id"],
        "ano": 2026,
        "trimestre": 1,
        "total_alunos": 20,
        "alfabetizados_leitura": 8,
        "alfabetizados_escrita": 10,
    }
    created = client.post("/indicadores-trimestrais", json=payload).json()

    response = client.delete(f"/indicadores-trimestrais/{created['id']}")

    assert response.status_code == 204


def test_delete_indicador_trimestral_not_found_returns_404(client):
    response = client.delete("/indicadores-trimestrais/0f57af7e-e7ce-4e9c-b5c9-b45e3df85801")

    assert response.status_code == 404
