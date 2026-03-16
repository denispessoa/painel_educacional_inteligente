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


def _payload(
    turma_id: str,
    *,
    ano: int = 2026,
    trimestre: int = 1,
    ano_escolar: int = 1,
    fonte_avaliacao: str = "cnca",
    total_alunos: int = 20,
    leitura: int = 8,
    escrita: int = 10,
    matematica: int = 12,
):
    return {
        "turma_id": turma_id,
        "ano": ano,
        "trimestre": trimestre,
        "ano_escolar": ano_escolar,
        "fonte_avaliacao": fonte_avaliacao,
        "total_alunos": total_alunos,
        "atingiu_esperado_leitura": leitura,
        "atingiu_esperado_escrita": escrita,
        "atingiu_esperado_matematica": matematica,
    }


def test_create_indicador_trimestral_success(client):
    turma = _create_turma(client)
    response = client.post("/indicadores-trimestrais", json=_payload(turma["id"]))

    assert response.status_code == 201
    data = response.json()
    assert data["turma_id"] == turma["id"]
    assert data["ano_escolar"] == 1
    assert data["fonte_avaliacao"] == "cnca"
    assert data["alfabetizados_leitura"] == 8
    assert data["alfabetizados_escrita"] == 10
    assert data["percentual_leitura"] == 40.0
    assert data["percentual_escrita"] == 50.0
    assert data["percentual_matematica"] == 60.0


def test_create_indicador_trimestral_total_zero_sets_percentual_zero(client):
    turma = _create_turma(client)
    response = client.post(
        "/indicadores-trimestrais",
        json=_payload(
            turma["id"],
            trimestre=2,
            total_alunos=0,
            leitura=0,
            escrita=0,
            matematica=0,
        ),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["percentual_leitura"] == 0.0
    assert data["percentual_escrita"] == 0.0
    assert data["percentual_matematica"] == 0.0


def test_create_indicador_trimestral_invalid_trimestre_returns_422(client):
    turma = _create_turma(client)

    response = client.post(
        "/indicadores-trimestrais",
        json=_payload(turma["id"], trimestre=5),
    )

    assert response.status_code == 422


def test_create_indicador_trimestral_matematica_gt_total_returns_422(client):
    turma = _create_turma(client)

    response = client.post(
        "/indicadores-trimestrais",
        json=_payload(turma["id"], matematica=21),
    )

    assert response.status_code == 422


def test_create_indicador_trimestral_invalid_fonte_for_grade_returns_422(client):
    turma = _create_turma(client)

    response = client.post(
        "/indicadores-trimestrais",
        json=_payload(turma["id"], ano_escolar=6, fonte_avaliacao="cnca"),
    )

    assert response.status_code == 422


def test_create_indicador_trimestral_with_missing_turma_returns_409(client):
    response = client.post(
        "/indicadores-trimestrais",
        json=_payload("0f57af7e-e7ce-4e9c-b5c9-b45e3df85801"),
    )

    assert response.status_code == 409


def test_create_indicador_trimestral_duplicate_period_returns_409(client):
    turma = _create_turma(client)
    payload = _payload(turma["id"], ano_escolar=5, fonte_avaliacao="cnca")

    first = client.post("/indicadores-trimestrais", json=payload)
    second = client.post("/indicadores-trimestrais", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409


def test_list_indicadores_trimestrais_filtered_by_turma(client):
    turma_1 = _create_turma(client)
    turma_2 = _create_turma(client)

    client.post("/indicadores-trimestrais", json=_payload(turma_1["id"], ano_escolar=2))
    client.post(
        "/indicadores-trimestrais",
        json=_payload(
            turma_2["id"],
            ano_escolar=7,
            fonte_avaliacao="mec_anos_finais_bncc",
        ),
    )

    response = client.get(f"/indicadores-trimestrais?turma_id={turma_1['id']}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["turma_id"] == turma_1["id"]


def test_list_indicadores_trimestrais_filtered_by_new_dimensions(client):
    turma = _create_turma(client)
    client.post("/indicadores-trimestrais", json=_payload(turma["id"], ano_escolar=2, fonte_avaliacao="cnca"))
    client.post(
        "/indicadores-trimestrais",
        json=_payload(
            turma["id"],
            trimestre=2,
            ano_escolar=6,
            fonte_avaliacao="mec_anos_finais_bncc",
        ),
    )

    response = client.get("/indicadores-trimestrais?ano_escolar=6&fonte_avaliacao=mec_anos_finais_bncc")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["ano_escolar"] == 6
    assert data[0]["fonte_avaliacao"] == "mec_anos_finais_bncc"


def test_get_indicador_trimestral_not_found_returns_404(client):
    response = client.get("/indicadores-trimestrais/0f57af7e-e7ce-4e9c-b5c9-b45e3df85801")

    assert response.status_code == 404


def test_update_indicador_trimestral_success_recalculates_percentuais(client):
    turma = _create_turma(client)
    created = client.post("/indicadores-trimestrais", json=_payload(turma["id"])).json()

    response = client.put(
        f"/indicadores-trimestrais/{created['id']}",
        json=_payload(
            turma["id"],
            trimestre=2,
            ano_escolar=6,
            fonte_avaliacao="mec_anos_finais_bncc",
            total_alunos=30,
            leitura=6,
            escrita=9,
            matematica=12,
        ),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["trimestre"] == 2
    assert data["ano_escolar"] == 6
    assert data["fonte_avaliacao"] == "mec_anos_finais_bncc"
    assert data["percentual_leitura"] == 20.0
    assert data["percentual_escrita"] == 30.0
    assert data["percentual_matematica"] == 40.0


def test_delete_indicador_trimestral_success_returns_204(client):
    turma = _create_turma(client)
    created = client.post("/indicadores-trimestrais", json=_payload(turma["id"])).json()

    response = client.delete(f"/indicadores-trimestrais/{created['id']}")

    assert response.status_code == 204


def test_delete_indicador_trimestral_not_found_returns_404(client):
    response = client.delete("/indicadores-trimestrais/0f57af7e-e7ce-4e9c-b5c9-b45e3df85801")

    assert response.status_code == 404
