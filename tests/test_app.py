from app import app


def test_health_endpoint():
    response = app.test_client().get("/health/live")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_process_rejects_missing_fields():
    response = app.test_client().post("/process", json={"user": "Ada"})
    assert response.status_code == 400
    assert response.json["error"] == "user and product are required"


def test_process_rejects_non_json():
    response = app.test_client().post("/process", data="not-json", content_type="text/plain")
    assert response.status_code == 400
