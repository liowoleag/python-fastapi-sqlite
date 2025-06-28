"""
Tests para endpoints de usuarios
"""
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """Test crear usuario"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "password": "TestPass123!",
        "confirm_password": "TestPass123!"
    }
    
    response = await client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data
    assert "hashed_password" not in data

@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: AsyncClient):
    """Test crear usuario con email duplicado"""
    user_data = {
        "email": "duplicate@example.com",
        "username": "user1",
        "first_name": "Test",
        "last_name": "User",
        "password": "TestPass123!",
        "confirm_password": "TestPass123!"
    }
    
    # Crear primer usuario
    response1 = await client.post("/api/v1/users/", json=user_data)
    assert response1.status_code == 201
    
    # Intentar crear segundo usuario con mismo email
    user_data["username"] = "user2"
    response2 = await client.post("/api/v1/users/", json=user_data)
    assert response2.status_code == 422

@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    """Test login de usuario"""
    # Crear usuario primero
    user_data = {
        "email": "login@example.com",
        "username": "loginuser",
        "first_name": "Login",
        "last_name": "User",
        "password": "LoginPass123!",
        "confirm_password": "LoginPass123!"
    }
    
    await client.post("/api/v1/users/", json=user_data)
    
    # Hacer login
    login_data = {
        "email": "login@example.com",
        "password": "LoginPass123!"
    }
    
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient):
    """Test obtener usuario actual"""
    # Crear y hacer login
    user_data = {
        "email": "current@example.com",
        "username": "currentuser",
        "first_name": "Current",
        "last_name": "User",
        "password": "CurrentPass123!",
        "confirm_password": "CurrentPass123!"
    }
    
    await client.post("/api/v1/users/", json=user_data)
    
    login_response = await client.post("/api/v1/auth/login", json={
        "email": "current@example.com",
        "password": "CurrentPass123!"
    })
    
    token = login_response.json()["access_token"]
    
    # Obtener usuario actual
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "current@example.com"
    assert data["username"] == "currentuser"
