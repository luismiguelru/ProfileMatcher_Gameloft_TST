from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.domain.models import PlayerProfile

class PlayerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, player_id: str) -> Optional[PlayerProfile]:
        return self.db.scalar(
            select(PlayerProfile).where(PlayerProfile.player_id == player_id)
        )

    def save(self, player: PlayerProfile) -> None:
        self.db.add(player)
