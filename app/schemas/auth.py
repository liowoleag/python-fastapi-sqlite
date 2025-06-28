"""
Authentication schemas
"""
from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    """Schema for login request"""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="Password")

class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request"""
    refresh_token: str = Field(..., description="Refresh token")

class TokenData(BaseModel):
    """Schema for token data"""
    user_id: int
    email: str
    username: str
