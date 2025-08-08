from datetime import datetime, timezone
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.core.config import settings
from app.core.config import logger
from app.domain.models import PlayerProfile

engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    # Crear tablas
    PlayerProfile.__table__.create(bind=engine, checkfirst=True)

    # Seed mínimo si no hay datos
    with SessionLocal() as db:
        existing = db.scalar(select(PlayerProfile).limit(1))
        if existing:
            return
        db.add(
            PlayerProfile(
                player_id="97983be2-98b7-11e7-90cf-082e5f28d836",
                credential="apple_credential",
                created=datetime(2021, 1, 10, 13, 37, 17, tzinfo=timezone.utc),
                modified=datetime(2021, 1, 23, 13, 37, 17, tzinfo=timezone.utc),
                last_session=datetime(2021, 1, 23, 13, 37, 17, tzinfo=timezone.utc),
                total_spent=400.0,
                total_refund=0.0,
                total_transactions=5,
                last_purchase=datetime(2021, 1, 22, 13, 37, 17, tzinfo=timezone.utc),
                active_campaigns=[],
                devices=[{"id": 1, "model": "apple iphone 11", "carrier": "vodafone", "firmware": "123"}],
                level=3,
                xp=1000,
                total_playtime=144,
                country="CA",
                language="fr",
                birthdate=datetime(2000, 1, 10, 13, 37, 17, tzinfo=timezone.utc),
                gender="male",
                inventory={"cash": 123, "coins": 123, "item_1": 1, "item_34": 3, "item_55": 2},
                clan={"id": "123456", "name": "Hello world clan"},
                customfield="mycustom",
            )
        )
        db.commit()
        logger.info("Seeded sample player")
