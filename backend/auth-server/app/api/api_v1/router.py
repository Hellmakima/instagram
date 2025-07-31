"""
### File: app/api/api_v1/router.py

Combines all the routers from api folder making it easier to import
"""
# api/routes.py

from fastapi import APIRouter
from app.api.api_v1.endpoints.auth import router as auth_router

router = APIRouter()

router.include_router(auth_router, tags=["auth"], prefix="/auth")


from fastapi import APIRouter

# Import the routers from each module
from .endpoints.auth.router import router as auth_router
# from .endpoints.password.router import router as password_router
# from .endpoints.verification.router import router as verification_router
# from .endpoints.social.router import router as social_router
# from .endpoints.security.router import router as security_router
# from .endpoints.account.router import router as account_router

router = APIRouter()

# Include all the sub-routers
# You can add prefixes here if you want, e.g., prefix="/auth"
router.include_router(auth_router, prefix="/auth", tags=["Core Auth"])
# router.include_router(password_router, prefix="/password", tags=["Password Management"])
# router.include_router(verification_router, prefix="/verification", tags=["Email/Phone Verification"])
# router.include_router(social_router, prefix="/social_login", tags=["Social Login"])
# router.include_router(security_router, prefix="/security", tags=["Security & Device Management"])
# router.include_router(account_router, prefix="/account", tags=["Account Management"])
