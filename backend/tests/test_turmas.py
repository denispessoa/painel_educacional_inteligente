def test_create_turma_success(client):
    municipio = client.post("/municipios", json={"nome": "Mendes", "estado": "RJ"}).json()
    escola = client.post(
        "/escolas",
        json={"nome": "Escola A", "municipio_id": municipio["id"]},
    ).json()

    response = client.post(
        "/turmas",
        json={"nome": "Turma 1", "escola_id": escola["id"]},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Turma 1"
    assert data["escola_id"] == escola["id"]


def test_list_turmas_by_escola_id(client):
    municipio = client.post("/municipios", json={"nome": "Mendes", "estado": "RJ"}).json()
    escola_1 = client.post(
        "/escolas",
        json={"nome": "Escola A", "municipio_id": municipio["id"]},
    ).json()
    escola_2 = client.post(
        "/escolas",
        json={"nome": "Escola B", "municipio_id": municipio["id"]},
    ).json()

    client.post("/turmas", json={"nome": "Turma A", "escola_id": escola_1["id"]})
    client.post("/turmas", json={"nome": "Turma B", "escola_id": escola_2["id"]})

    response = client.get(f"/turmas?escola_id={escola_1['id']}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nome"] == "Turma A"


def test_delete_turma_without_dependencies_returns_204(client):
    municipio = client.post("/municipios", json={"nome": "Mendes", "estado": "RJ"}).json()
    escola = client.post(
        "/escolas",
        json={"nome": "Escola A", "municipio_id": municipio["id"]},
    ).json()
    turma = client.post(
        "/turmas",
        json={"nome": "Turma A", "escola_id": escola["id"]},
    ).json()

    response = client.delete(f"/turmas/{turma['id']}")

    assert response.status_code == 204

