
from app import create_app


def test_health_endpoint():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_candidates_endpoint():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/candidates")

    assert response.status_code == 200
    data = response.get_json()

    assert "candidates" in data
    assert isinstance(data["candidates"], list)
    assert len(data["candidates"]) > 0


def test_jobs_endpoint():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/jobs")

    assert response.status_code == 200
    data = response.get_json()

    assert "jobs" in data
    assert isinstance(data["jobs"], list)
    assert len(data["jobs"]) > 0
