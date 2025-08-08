from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict

class DeviceModel(BaseModel):
    id: int
    model: str
    carrier: str
    firmware: str

class ClanModel(BaseModel):
    id: str
    name: str

class PlayerProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    player_id: str
    credential: str
    created: datetime
    modified: datetime
    last_session: datetime
    total_spent: float
    total_refund: float
    total_transactions: int
    last_purchase: datetime
    active_campaigns: List[str]
    devices: List[DeviceModel]
    level: int
    xp: int
    total_playtime: int
    country: str
    language: str
    birthdate: datetime
    gender: str
    inventory: Dict[str, int]
    clan: ClanModel
    customfield: Optional[str] = Field(None, serialization_alias="_customfield")
