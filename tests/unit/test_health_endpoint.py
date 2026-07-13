import importlib
from unittest.mock import patch

from fastapi.testclient import TestClient


def test_api_health_returns_status_without_external_services(monkeypatch):
    monkeypatch.setenv("CLOUDINARY_CLOUD_NAME", "test-cloud")
    monkeypatch.setenv("CLOUDINARY_API_KEY", "test-key")
    monkeypatch.setenv("CLOUDINARY_API_SECRET", "test-secret")
    monkeypatch.setenv("PINECONE_API_KEY", "test-pinecone-key")

    backend_server = importlib.import_module("backend.backend_server")

    with (
        patch.object(backend_server, "get_cloudinary_service") as cloudinary_service,
        patch.object(backend_server, "get_pinecone_service") as pinecone_service,
    ):
        response = TestClient(backend_server.app).get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "feature_extractor": "ResNet-50",
        "retrieval_system": "Pinecone",
        "storage": "Cloudinary",
        "vectors": "Quantum-Enhanced",
    }
    cloudinary_service.assert_not_called()
    pinecone_service.assert_not_called()
