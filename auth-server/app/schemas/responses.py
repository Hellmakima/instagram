"""
### File: app/schemas/responses.py
defines
- SuccessMessageResponse
- ErrorDetail
- APIErrorResponse
- InternalServerError

**Usage**

```python
from app.schemas.responses import SuccessMessageResponse

raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=APIErrorResponse(
        message="Bad Request",
        error=ErrorDetail(
            code="INVALID_CREDENTIALS",
            details="Invalid username, password, or account status."
        )
    ).model_dump()
)
```

"""

from fastapi import HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional


class SuccessMessageResponse(BaseModel):
    success: bool = True
    message: str = Field("Success", description="Message of the response")
    data: Optional[dict] = Field(default_factory=dict)


class ErrorDetail(BaseModel):
    code: str = Field(default="UNKNOWN_ERROR", description="Error code")
    details: str = Field(
        default="No details provided", description="Details of the error"
    )


class APIErrorResponse(BaseModel):
    success: bool = Field(default=False, description="Indicates failure")
    message: str = Field(default="Error", description="Message of the response")
    error: Optional[ErrorDetail] = None


class InternalServerError(HTTPException):
    def __init__(self, details: str = "An unexpected server error occurred."):
        error_response = APIErrorResponse(
            message="An unexpected server error occurred.",
            error=ErrorDetail(code="INTERNAL_SERVER_ERROR", details=details),
        )
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        )
