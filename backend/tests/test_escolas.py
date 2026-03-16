def test_create_escola_success(client):
    municipio = client.post("/municipios", json={"nome": "Mendes", "estado": "RJ"}).json()

    response = client.post(
        "/escolas",
        json={"nome": "Escola Central", "municipio_id": municipio["id"]},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Escola Central"
    assert data["municipio_id"] == municipio["id"]


def test_create_escola_with_missing_municipio_returns_409(client):
    response = client.post(
        "/escolas",
        json={
            "nome": "Escola Invalida",
            "municipio_id": "0f57af7e-e7ce-4e9c-b5c9-b45e3df85801",
        },
    )

    assert response.status_code == 409


def test_list_escolas_filtered_by_municipio_id(client):
    m1 = client.post("/municipios", json={"nome": "Mendes", "estado": "RJ"}).json()
    m2 = client.post("/municipios", json={"nome": "Outra Cidade", "estado": "SP"}).json()

    client.post("/escolas", json={"nome": "Escola A", "municipio_id": m1["id"]})
    client.post("/escolas", json={"nome": "Escola B", "municipio_id": m2["id"]})

    response = client.get(f"/escolas?municipio_id={m1['id']}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nome"] == "Escola A"


def test_delete_escola_with_turma_returns_409(client):
    municipio = client.post("/municipios", json={"nome": "Mendes", "estado": "RJ"}).json()
    escola = client.post(
        "/escolas",
        json={"nome": "Escola A", "municipio_id": municipio["id"]},
    ).json()
    client.post("/turmas", json={"nome": "Turma 1", "escola_id": escola["id"]})

    response = client.delete(f"/escolas/{escola['id']}")

    assert response.status_code == 409

