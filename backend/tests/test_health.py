def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "x-request-id" in response.headers


def test_health_dependencies(client):
    response = client.get("/health/dependencies")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "dependencies": {"database": "ok"},
    }


def test_metrics(client):
    client.get("/health")
    client.get("/health/dependencies")

    response = client.get("/metrics")
    payload = response.json()

    assert response.status_code == 200
    assert payload["requests_total"] == 2
    assert payload["requests_by_status"] == {"2xx": 2, "4xx": 0, "5xx": 0}
    assert "started_at" in payload
    assert payload["uptime_seconds"] >= 0
    assert payload["avg_latency_ms"] >= 0
