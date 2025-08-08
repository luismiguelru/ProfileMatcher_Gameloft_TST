from datetime import datetime, timezone
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.deps import get_db_dep as get_db, campaigns_provider_dep as campaigns_provider
from app.domain.schemas import PlayerProfileResponse
from app.domain.repositories import PlayerRepository
from app.domain.services import CampaignMatcher

router = APIRouter()

@router.get("/get_client_config/{player_id}", response_model=PlayerProfileResponse, tags=["profile"])
def get_client_config(
    player_id: str,
    db: Session = Depends(get_db),
    campaigns: List[Dict[str, Any]] = Depends(campaigns_provider),
):
    repo = PlayerRepository(db)
    player = repo.get_by_id(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    CampaignMatcher.apply(player, campaigns)
    repo.save(player)  # flush/commit gestionado en get_db
    return PlayerProfileResponse.model_validate(player)

@router.get("/health", tags=["health"])
def health(
    db: Session = Depends(get_db),
    campaigns: List[Dict[str, Any]] = Depends(campaigns_provider),
):
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    try:
        camp_ok = isinstance(campaigns, list)
        camp_count = len(campaigns) if camp_ok else 0
    except Exception:
        camp_ok = False
        camp_count = 0

    status = "ok" if (db_ok and camp_ok) else "degraded"
    return {
        "status": status,
        "database": "ok" if db_ok else "error",
        "campaigns_provider": "ok" if camp_ok else "error",
        "campaigns_count": camp_count,
        "time": datetime.now(timezone.utc).isoformat(),
    }
