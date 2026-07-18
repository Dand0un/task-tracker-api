"""
Pydantic schema(s) for the /health endpoint.
Keeping response schemas in this module (rather than inline in the
route) keeps the API layer thin and makes schemas reusable/testable.
"""
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response body returned by GET /health."""

    status: str = Field(..., description="Simple indicator that the API is running.")
    timestamp: str = Field(..., description="Current server time in ISO 8601 format.")