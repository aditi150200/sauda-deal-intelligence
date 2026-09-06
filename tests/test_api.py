from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    assert client.get('/health').json() == {'status': 'ok'}


def test_deals_include_assessment():
    response = client.get('/api/deals')
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert 'risk_score' in response.json()[0]['assessment']


def test_unknown_deal_returns_404():
    assert client.get('/api/deals/not-real').status_code == 404

