import pytest
from app import app, db


@pytest.fixture()
def client(tmp_path, monkeypatch):
    database = tmp_path / "test-monolith.db"
    monkeypatch.setitem(app.config, "SQLALCHEMY_DATABASE_URI", f"sqlite:///{database}")
    app.config.update(TESTING=True)
    with app.app_context():
        db.drop_all()
        db.create_all()
    with app.test_client() as test_client:
        yield test_client
    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_health_endpoint(client):
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_process_rejects_missing_fields(client):
    response = client.post("/process", json={"user": "Ada"})
    assert response.status_code == 400
    assert response.json["error"] == "user and product are required"


def test_process_creates_order(client):
    response = client.post("/process", json={"user": "Ada", "product": "Book"})
    assert response.status_code == 201
    assert response.json["status"] == "accepted"
