"""
Tests para autenticación
"""
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login con credenciales inválidas"""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "WrongPassword123!"
    }
    
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401
    
    data = response.json()
    assert data["error"] == "UNAUTHORIZED"

@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient):
    """Test renovar token"""
    # Crear usuario y hacer login
    user_data = {
        "email": "refresh@example.com",
        "username": "refreshuser",
        "first_name": "Refresh",
        "last_name": "User",
        "password": "RefreshPass123!",
        "confirm_password": "RefreshPass123!"
    }
    
    await client.post("/api/v1/users/", json=user_data)
    
    login_response = await client.post("/api/v1/auth/login", json={
        "email": "refresh@example.com",
        "password": "RefreshPass123!"
    })
    
    refresh_token = login_response.json()["refresh_token"]
    
    # Renovar token
    response = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.asyncio
async def test_protected_endpoint_without_token(client: AsyncClient):
    """Test endpoint protegido sin token"""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 403
