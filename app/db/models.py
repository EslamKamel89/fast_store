# app/db/models.py

from app.apps.auth import models as auth_models
from app.apps.catalog import models as catalog_models
from app.apps.orders import models as orders_models
from app.apps.profiles import models as profiles_models
from app.apps.users import models as users_models

__all__ = [
    "auth_models",
    "catalog_models",
    "orders_models",
    "profiles_models",
    "users_models",
]
