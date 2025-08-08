from datetime import datetime
from typing import Any, Dict, List

def _parse_utc(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))

def default_campaigns_provider() -> List[Dict[str, Any]]:
    return [
        {
            "game": "mygame",
            "name": "mycampaign",
            "priority": 10.5,
            "matchers": {
                "level": {"min": 1, "max": 3},
                "has": {"country": ["US", "RO", "CA"], "items": ["item_1"]},
                "does_not_have": {"items": ["item_4"]},
            },
            "start_date": "2022-01-25 00:00:00Z",
            "end_date": "2025-12-25 00:00:00Z",
            "enabled": True,
            "last_updated": "2021-07-13 11:46:58Z",
        }
    ]

def campaigns_provider() -> List[Dict[str, Any]]:
    return default_campaigns_provider()
