from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timezone
from fastapi.testclient import TestClient
import pytest

from app.main import create_app
from app.domain.models import PlayerProfile
from app.core import db as core_db

@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    # fresh engine per test
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

    # patch app's DB to use test engine/session
    monkeypatch.setattr(core_db, "engine", engine, raising=True)
    monkeypatch.setattr(core_db, "SessionLocal", TestingSessionLocal, raising=True)

    # create schema
    from app.domain.models import BaseModel as Base
    Base.metadata.create_all(bind=engine)

    # seed once per test
    with TestingSessionLocal() as db:
        db.add(
            PlayerProfile(
                player_id="p1",
                credential="apple_credential",
                created=datetime(2021,1,10,13,37,17,tzinfo=timezone.utc),
                modified=datetime(2021,1,23,13,37,17,tzinfo=timezone.utc),
                last_session=datetime(2021,1,23,13,37,17,tzinfo=timezone.utc),
                total_spent=400.0, total_refund=0.0, total_transactions=5,
                last_purchase=datetime(2021,1,22,13,37,17,tzinfo=timezone.utc),
                active_campaigns=[],
                devices=[{"id":1,"model":"apple iphone 11","carrier":"vodafone","firmware":"123"}],
                level=3, xp=1000, total_playtime=144, country="CA", language="fr",
                birthdate=datetime(2000,1,10,13,37,17,tzinfo=timezone.utc), gender="male",
                inventory={"cash":123,"coins":123,"item_1":1,"item_34":3,"item_55":2},
                clan={"id":"123456","name":"Hello world clan"},
                customfield="mycustom",
            )
        )
        db.commit()

    yield

    # teardown: drop schema so nothing leaks
    Base.metadata.drop_all(bind=engine)


def test_get_client_config_updates_and_returns():
    app = create_app()
    client = TestClient(app)
    r = client.get("/get_client_config/p1")
    assert r.status_code == 200
    body = r.json()
    assert "mycampaign" in body["active_campaigns"]
    assert body["_customfield"] == "mycustom"

def test_health_ok():
    app = create_app()
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] in ("ok", "degraded")

def test_get_client_config_user_not_found():
    app = create_app()
    client = TestClient(app)
    r = client.get("/get_client_config/does-not-exist")
    assert r.status_code == 404
    body = r.json()
    assert body["detail"] == "Player not found"


def test_get_client_config_no_matching_campaigns(monkeypatch):
    # Override of campaigns_provider so there is no match
    from app.core import deps as core_deps

    def no_match_campaigns():
        # require country US and item that player doesn't have
        return [
            {
                "game": "mygame",
                "name": "never_match",
                "priority": 999,
                "matchers": {
                    "level": {"min": 99, "max": 100},      # out of range
                    "has": {"country": ["US"], "items": ["nonexistent_item"]},
                    "does_not_have": {"items": []},
                },
                "start_date": "2022-01-25 00:00:00Z",
                "end_date": "2025-12-25 00:00:00Z",
                "enabled": True,
                "last_updated": "2025-01-01 00:00:00Z",
            }
        ]

    app = create_app()
    app.dependency_overrides[core_deps.campaigns_provider_dep] = no_match_campaigns

    client = TestClient(app)
    r = client.get("/get_client_config/p1")
    assert r.status_code == 200
    body = r.json()

    assert body["active_campaigns"] == []

    # cleaning the override
    app.dependency_overrides.pop(core_deps.campaigns_provider_dep, None)

