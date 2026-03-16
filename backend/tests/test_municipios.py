def test_create_municipio_success(client):
    payload = {"nome": "Mendes", "estado": "rj"}

    response = client.post("/municipios", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Mendes"
    assert data["estado"] == "RJ"
    assert "id" in data


def test_create_municipio_invalid_estado_returns_422(client):
    payload = {"nome": "Mendes", "estado": "Rio"}

    response = client.post("/municipios", json=payload)

    assert response.status_code == 422


def test_get_municipio_not_found_returns_404(client):
    response = client.get("/municipios/0f57af7e-e7ce-4e9c-b5c9-b45e3df85801")

    assert response.status_code == 404


def test_update_municipio_success(client):
    created = client.post("/municipios", json={"nome": "Mendes", "estado": "RJ"}).json()

    response = client.put(
        f"/municipios/{created['id']}",
        json={"nome": "Mendes Atualizado", "estado": "SP"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Mendes Atualizado"
    assert data["estado"] == "SP"


def test_delete_municipio_without_dependencies_returns_204(client):
    created = client.post("/municipios", json={"nome": "Mendes", "estado": "RJ"}).json()

    response = client.delete(f"/municipios/{created['id']}")

    assert response.status_code == 204


def test_delete_municipio_with_dependencies_returns_409(client):
    municipio = client.post("/municipios", json={"nome": "Mendes", "estado": "RJ"}).json()
    client.post(
        "/escolas",
        json={"nome": "Escola A", "municipio_id": municipio["id"]},
    )

    response = client.delete(f"/municipios/{municipio['id']}")

    assert response.status_code == 409

