from datetime import datetime, timezone
from typing import Any, Dict, List
from app.domain.models import PlayerProfile
from app.domain.providers import _parse_utc

class CampaignMatcher:
    @staticmethod
    def _inventory_has(player: PlayerProfile, item: str) -> bool:
        inv = player.inventory or {}
        return bool(inv.get(item, 0))

    @staticmethod
    def _now_utc() -> datetime:
        return datetime.now(timezone.utc)

    @classmethod
    def matches(cls, player: PlayerProfile, campaign: Dict[str, Any]) -> bool:
        if not campaign.get("enabled", False):
            return False

        try:
            start = _parse_utc(campaign["start_date"])
            end = _parse_utc(campaign["end_date"])
        except Exception:
            return False

        now = cls._now_utc()
        if not (start <= now <= end):
            return False

        matchers = campaign.get("matchers", {})

        lvl = matchers.get("level")
        if lvl:
            if not (lvl.get("min", -10**9) <= player.level <= lvl.get("max", 10**9)):
                return False

        has = matchers.get("has", {})
        countries = has.get("country")
        if countries and player.country not in countries:
            return False

        for it in has.get("items", []):
            if not cls._inventory_has(player, it):
                return False

        for it in matchers.get("does_not_have", {}).get("items", []):
            if cls._inventory_has(player, it):
                return False

        return True

    @classmethod
    def apply(cls, player: PlayerProfile, campaigns: List[Dict[str, Any]]) -> List[str]:
        matched = [c for c in campaigns if cls.matches(player, c)]

        def sort_key(c: Dict[str, Any]):
            prio = float(c.get("priority", 0))
            lu = c.get("last_updated") or "1970-01-01 00:00:00Z"
            try:
                from app.domain.providers import _parse_utc
                lu_dt = _parse_utc(lu)
            except Exception:
                lu_dt = datetime(1970, 1, 1, tzinfo=timezone.utc)
            return (-prio, -lu_dt.timestamp())

        matched.sort(key=sort_key)
        names = [c["name"] for c in matched if "name" in c]

        current = set(player.active_campaigns or [])
        current.update(names)
        player.active_campaigns = sorted(current)
        player.modified = cls._now_utc()
        return names
