"""
### File: app/api/api_v1/router.py

Combines all the routers from api folder making it easier to import
"""

from fastapi import APIRouter

from app.api.api_v1.endpoints.auth.router import router as auth_router
# from app.api.api_v1.endpoints.password.router import router as password_router
# from app.api.api_v1.endpoints.verification.router import router as verification_router
# from app.api.api_v1.endpoints.social.router import router as social_router
# from app.api.api_v1.endpoints.security.router import router as security_router
# from app.api.api_v1.endpoints.account.router import router as account_router

router = APIRouter()

router.include_router(auth_router, prefix="/resource", tags=["Resource Management"])
# router.include_router(password_router, prefix="/password", tags=["Password Management"])
# router.include_router(verification_router, prefix="/verification", tags=["Email/Phone Verification"])
# router.include_router(social_router, prefix="/social_login", tags=["Social Login"])
# router.include_router(security_router, prefix="/security", tags=["Security & Device Management"])
# router.include_router(account_router, prefix="/account", tags=["Account Management"])
