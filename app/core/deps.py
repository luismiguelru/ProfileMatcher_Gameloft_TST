from app.core.db import get_db
from app.domain.providers import campaigns_provider

# Reexport to use in Depends
get_db_dep = get_db
campaigns_provider_dep = campaigns_provider
