from fastapi import APIRouter

from app.scenarios.user.create_user.presentation_handler import (
    create_user_router,
)
from app.scenarios.user.deactivate_user.presentation_handler import (
    deactivate_user_router,
)
from app.scenarios.user.delete_own_user.presentation_handler import (
    delete_own_user_router,
)
from app.scenarios.user.get_own_user.presentation_handler import (
    get_own_user_router,
)
from app.scenarios.user.grant_admin.presentation_handler import (
    grant_admin_router,
)
from app.scenarios.user.list_users.presentation_handler import (
    list_users_router,
)
from app.scenarios.user.reactivate_user.presentation_handler import (
    reactivate_user_router,
)
from app.scenarios.user.revoke_admin.presentation_handler import (
    revoke_admin_router,
)

users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

users_sub_routers = (
    create_user_router,
    list_users_router,
    get_own_user_router,
    delete_own_user_router,
    deactivate_user_router,
    reactivate_user_router,
    grant_admin_router,
    revoke_admin_router,
)

for router in users_sub_routers:
    users_router.include_router(router)
