# 🚀 User Management Microservice

Professional user management microservice built with **FastAPI** and **SQLite**, following best practices for development and clean architecture.

## ✨ Features

- 🔥 **Async FastAPI**: Fully asynchronous REST API with high performance
- 🗄️ **SQLite Database**: Lightweight and efficient database, perfect for development
- 📚 **Auto Documentation**: Swagger UI and ReDoc automatically integrated
- ✅ **Robust Validations**: Using Pydantic for complete data validation
- 🔐 **JWT Authentication**: Complete system with access and refresh tokens
- 🏗️ **Clean Architecture**: Clear separation of concerns (Repository, Service, Router)
- 🛡️ **Error Handling**: Robust custom exception system
- 🧪 **Complete Testing**: Automated test suite with pytest
- 🐳 **Docker Ready**: Complete containerization ready for production
- 📊 **Structured Logging**: Detailed logging system for debugging
- 📄 **Pagination**: Endpoints with automatic pagination and search

## 🏗️ Project Architecture

```text
app/
├── core/           # Core configuration and utilities
│   ├── config.py          # Configuration with Pydantic Settings
│   ├── database.py        # SQLAlchemy async configuration
│   ├── security.py        # JWT, hashing, authentication
│   ├── exceptions.py      # Custom exceptions
│   └── logging_config.py  # Logging configuration
├── models/         # Database models (SQLAlchemy)
│   └── user.py           # User model with timestamps
├── schemas/        # Validation schemas (Pydantic)
│   ├── user.py           # User schemas
│   └── auth.py           # Authentication schemas
├── repositories/   # Data access layer
│   └── user_repository.py # CRUD operations for users
├── services/       # Business logic layer
│   ├── user_service.py   # User services
│   └── auth_service.py   # Authentication services
├── routers/        # API endpoints
│   ├── users.py          # User endpoints
│   ├── auth.py           # Authentication endpoints
│   ├── health.py         # Health checks
│   └── dependencies.py   # Shared dependencies
└── tests/          # Automated tests
    ├── test_users.py     # User tests
    └── test_auth.py      # Authentication tests
```
## 🛠️ Technologies Used

- **FastAPI**: Modern, high-performance web framework
- **SQLite**: Lightweight database with no configuration needed
- **SQLAlchemy**: Async ORM for database management
- **Pydantic**: Data validation and serialization
- **JWT (Jose)**: Token-based authentication
- **Bcrypt**: Secure password hashing
- **Docker**: Containerization and deployment
- **Pytest**: Testing framework
- **Uvicorn**: High-performance ASGI server

## 🚀 Installation and Setup

### Option 1: With Docker (Recommended)

#### Prerequisites
- Docker and Docker Compose installed
- Git to clone the repository

#### Installation Steps

1. **Clone the repository**
\`\`\`bash
git clone <repository-url>
cd user-management-microservice
\`\`\`

2. **Configure environment variables**
\`\`\`bash
# Copy example file
cp .env.example .env

# Edit configurations if needed
nano .env
\`\`\`

3. **Build and run with Docker**
\`\`\`bash
# Build the image
docker compose build

# Run in background
docker compose up -d

# View logs in real-time
docker compose logs -f user-api
\`\`\`

4. **Verify it works**
\`\`\`bash
# Health check
curl http://localhost:8000/api/v1/health

# Root endpoint
curl http://localhost:8000/

# Debug info
curl http://localhost:8000/debug
\`\`\`

### Option 2: Local Development

#### Prerequisites
- Python 3.11+
- pip (Python package manager)

#### Installation Steps

1. **Create virtual environment**
\`\`\`bash
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
\`\`\`

2. **Install dependencies**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Configure environment variables**
\`\`\`bash
cp .env.example .env
# Edit .env according to your needs
\`\`\`

4. **Run the application**
\`\`\`bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

## 🧪 Installation Verification

### 1. Create Admin User
\`\`\`bash
# With Docker
docker compose exec user-api python scripts/create_admin.py

# Local development
python scripts/create_admin.py
\`\`\`

### 2. Verify Database
\`\`\`bash
# With Docker
docker compose exec user-api python scripts/check_db.py

# Local development
python scripts/check_db.py
\`\`\`

### 3. Run Tests
\`\`\`bash
# With Docker
docker compose exec user-api pytest -v

# Local development
pytest -v
\`\`\`

## 📚 API Usage

### 📖 Interactive API Documentation

Once the application is running, you can access the interactive API documentation:

#### **🎯 Swagger UI (Recommended)**
**URL**: **http://localhost:8000/docs**

- ✅ **Interactive testing** - Test all endpoints directly from the browser
- ✅ **Authentication support** - Built-in authorization with JWT tokens
- ✅ **Request/Response examples** - See exactly what to send and expect
- ✅ **Schema validation** - Real-time validation of your requests

#### **📚 ReDoc (Alternative Documentation)**
**URL**: **http://localhost:8000/redoc**

- ✅ **Clean, readable format** - Better for reading and understanding
- ✅ **Detailed schemas** - Complete data model documentation
- ✅ **Export capabilities** - Easy to share with team members

#### **🔧 OpenAPI Specification**
**URL**: **http://localhost:8000/openapi.json**

- ✅ **Machine-readable format** - For API client generation
- ✅ **Integration ready** - Import into Postman, Insomnia, etc.

### 🚀 Quick Start with Swagger UI

1. **Start the application**:
   \`\`\`bash
   docker compose up -d
   \`\`\`

2. **Open Swagger UI**: http://localhost:8000/docs

3. **Create a user**:
   - Expand `POST /api/v1/users/`
   - Click "Try it out"
   - Fill in the example data
   - Click "Execute"

4. **Login to get token**:
   - Expand `POST /api/v1/auth/login`
   - Use the email/password from step 3
   - Copy the `access_token` from response

5. **Authorize for protected endpoints**:
   - Click the 🔒 **"Authorize"** button at the top
   - Enter: `Bearer your_access_token_here`
   - Click "Authorize"

6. **Test protected endpoints**:
   - Now you can test `/api/v1/users/me` and other protected routes!

### Main Endpoints

#### 🔐 Authentication
\`\`\`bash
# Login
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "MyPassword123!"
}

# Refresh token
POST /api/v1/auth/refresh
{
  "refresh_token": "your_refresh_token"
}

# Logout
POST /api/v1/auth/logout
\`\`\`

#### 👥 User Management
\`\`\`bash
# Create user
POST /api/v1/users/
{
  "email": "new@example.com",
  "username": "newuser",
  "first_name": "First",
  "last_name": "Last",
  "password": "Password123!",
  "confirm_password": "Password123!"
}

# Get current profile (requires authentication)
GET /api/v1/users/me
Authorization: Bearer your_access_token

# List users (paginated)
GET /api/v1/users/?page=1&size=10&search=text
Authorization: Bearer your_access_token

# Update profile
PUT /api/v1/users/me
Authorization: Bearer your_access_token
{
  "first_name": "New Name",
  "bio": "New biography"
}

# Change password
POST /api/v1/users/me/change-password
Authorization: Bearer your_access_token
{
  "current_password": "CurrentPassword123!",
  "new_password": "NewPassword456!",
  "confirm_password": "NewPassword456!"
}
\`\`\`

#### 🏥 Health Checks
\`\`\`bash
# Basic health check
GET /api/v1/health

# Detailed health check
GET /api/v1/health/detailed
\`\`\`

## 🧪 Practical Examples

### Complete Test Script

\`\`\`bash
# Create and run complete test script
cat > test_api_complete.sh << 'EOF'
#!/bin/bash

echo "🚀 Testing complete API..."

# 1. Health check
echo "1️⃣ Health check..."
curl -s http://localhost:8000/api/v1/health | jq .

# 2. Create user
echo -e "\n2️⃣ Creating user..."
USER_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "password": "TestPass123!",
    "confirm_password": "TestPass123!",
    "phone": "+1234567890",
    "bio": "Test user"
  }')
echo $USER_RESPONSE | jq .

# 3. Login
echo -e "\n3️⃣ Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }')
echo $LOGIN_RESPONSE | jq .

# Extract token
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')

# 4. Get profile
echo -e "\n4️⃣ Getting profile..."
curl -s -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer $TOKEN" | jq .

# 5. List users
echo -e "\n5️⃣ Listing users..."
curl -s -X GET "http://localhost:8000/api/v1/users/?page=1&size=10" \
  -H "Authorization: Bearer $TOKEN" | jq .

echo -e "\n✅ Tests completed!"
EOF

chmod +x test_api_complete.sh
./test_api_complete.sh
\`\`\`

### Using curl step by step

\`\`\`bash
# 1. Create user
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "user123",
    "first_name": "John",
    "last_name": "Doe",
    "password": "MyPassword123!",
    "confirm_password": "MyPassword123!"
  }'

# 2. Login and save token
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "MyPassword123!"
  }')

TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')

# 3. Use token for protected endpoints
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer $TOKEN"
\`\`\`

## 🗄️ SQLite Database

### Features
- **Single file**: `users.db` in root directory
- **Serverless**: No additional installation required
- **ACID compliant**: Safe transactions
- **Perfect for development**: Easy to backup and migrate

### Useful Commands

\`\`\`bash
# Access database (with Docker)
docker compose exec user-api sqlite3 users.db

# View tables
.tables

# View users structure
.schema users

# View all users
SELECT * FROM users;

# Count users
SELECT COUNT(*) FROM users;

# Exit
.quit
\`\`\`

### Migration to PostgreSQL (Production)

To migrate to PostgreSQL in production:

1. **Change DATABASE_URL** in `.env`:
\`\`\`bash
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
\`\`\`

2. **Use docker-compose.full.yml**:
\`\`\`bash
docker compose -f docker-compose.full.yml up -d
\`\`\`

3. **Install PostgreSQL driver**:
\`\`\`bash
pip install asyncpg
\`\`\`

## 🧪 Testing

### Run Tests

\`\`\`bash
# All tests
docker compose exec user-api pytest -v

# Tests with coverage
docker compose exec user-api pytest --cov=app --cov-report=html

# Specific tests
docker compose exec user-api pytest tests/test_users.py -v
docker compose exec user-api pytest tests/test_auth.py -v

# Specific test
docker compose exec user-api pytest tests/test_users.py::test_create_user -v
\`\`\`

### Test Structure

- `tests/test_users.py`: Tests for user endpoints
- `tests/test_auth.py`: Tests for authentication
- `tests/conftest.py`: Pytest configuration and fixtures

## 🔧 Useful Commands

### Docker

\`\`\`bash
# Build image
make docker-build
# or
docker compose build

# Run application
make docker-run
# or
docker compose up -d

# View logs
make docker-logs
# or
docker compose logs -f user-api

# Stop services
make docker-stop
# or
docker compose down

# Restart services
docker compose restart
\`\`\`

### Makefile Commands

El proyecto incluye un `Makefile` con comandos útiles para desarrollo:

\`\`\`bash
# Ver todos los comandos disponibles
make help

# Comandos de desarrollo
make install          # Instalar dependencias
make dev              # Ejecutar en modo desarrollo
make format           # Formatear código con black
make lint             # Verificar código con flake8

# Comandos de testing
make test             # Ejecutar tests
make test-cov         # Ejecutar tests con coverage

# Comandos de Docker (SQLite)
make docker-build     # Construir imagen Docker
make docker-run       # Ejecutar con Docker Compose
make docker-stop      # Detener contenedores
make docker-logs      # Ver logs
make docker-restart   # Reiniciar servicios
make docker-rebuild   # Reconstruir y reiniciar

# Comandos de Docker (PostgreSQL completo)
make docker-full-run  # Ejecutar con PostgreSQL + Redis + Adminer
make docker-full-stop # Detener configuración completa
make docker-full-logs # Ver logs de configuración completa

# Comandos de aplicación
make create-admin     # Crear usuario administrador
make check-db         # Verificar estado de base de datos
make sqlite-shell     # Abrir shell de SQLite
make sqlite-backup    # Crear backup de SQLite

# Comandos de utilidad
make clean            # Limpiar archivos temporales (__pycache__, etc.)
make shell            # Acceder al shell del contenedor
make health           # Verificar salud de la aplicación
make quick-test       # Test rápido de la API
\`\`\`

### Ejemplos de uso del Makefile

\`\`\`bash
# Flujo típico de desarrollo
make docker-build     # Construir imagen
make docker-run       # Iniciar aplicación
make create-admin     # Crear usuario admin
make health           # Verificar que funciona
make test             # Ejecutar tests

# Desarrollo local
make install          # Instalar dependencias
make dev              # Ejecutar en desarrollo
make format           # Formatear código antes de commit

# Mantenimiento
make clean            # Limpiar archivos temporales
make sqlite-backup    # Hacer backup antes de cambios
make check-db         # Verificar estado de BD
\`\`\`

### Database

\`\`\`bash
# Create admin user
make create-admin
# or
docker compose exec user-api python scripts/create_admin.py

# Check database
make check-db
# or
docker compose exec user-api python scripts/check_db.py

# SQLite shell
make sqlite-shell
# or
docker compose exec user-api sqlite3 users.db

# SQLite backup
docker compose exec user-api cp users.db users_backup_$(date +%Y%m%d_%H%M%S).db
\`\`\`

### Development

\`\`\`bash
# Format code
make format
# or
black app/ tests/ main.py

# Check code
make lint
# or
flake8 app/ tests/ main.py

# Run in development
make dev
# or
uvicorn main:app --reload
\`\`\`

## 🔒 Security

### Implemented Security Features

- ✅ **Hashed passwords** with bcrypt (automatic salt)
- ✅ **JWT tokens** with configurable expiration
- ✅ **Refresh tokens** for secure renewal
- ✅ **Robust input validation** with Pydantic
- ✅ **Secure error handling** without sensitive information exposure
- ✅ **CORS configured** for access control
- ✅ **Trusted host middleware**
- ✅ **Password validation** (uppercase, lowercase, number, length)

### Security Configuration

\`\`\`bash
# Important variables in .env
SECRET_KEY=your-super-secret-production-key-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
\`\`\`

### Best Practices

1. **Change SECRET_KEY** in production
2. **Use HTTPS** in production
3. **Configure specific ALLOWED_HOSTS**
4. **Implement rate limiting** for public endpoints
5. **Monitor security logs**
6. **Update dependencies** regularly

## 🚀 Production Deployment

### Production Environment Variables

\`\`\`bash
# .env for production
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-super-secret-production-key-very-long-and-random
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/users_db
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
LOG_LEVEL=WARNING
\`\`\`

### Docker in Production

\`\`\`bash
# Use complete configuration with PostgreSQL
docker compose -f docker-compose.full.yml up -d

# Or build optimized image
docker build -t user-management-api:latest .
docker run -d -p 8000:8000 --env-file .env.production user-management-api:latest
\`\`\`

### Production Checklist

- [ ] Change SECRET_KEY to a secure one
- [ ] Configure PostgreSQL database
- [ ] Configure HTTPS/SSL
- [ ] Configure specific ALLOWED_HOSTS
- [ ] Implement rate limiting
- [ ] Configure monitoring and logging
- [ ] Configure automatic backups
- [ ] Implement CI/CD pipeline
- [ ] Configure health checks
- [ ] Document APIs for the team

## 🐛 Troubleshooting

### Common Issues

#### 1. Database connection error
\`\`\`bash
# Check if file exists
ls -la users.db

# Recreate database
docker compose exec user-api python scripts/force_create_db.py

# View detailed logs
docker compose logs user-api
\`\`\`

#### 2. Permission error
\`\`\`bash
# Check directory permissions
docker compose exec user-api ls -la /app/

# Recreate container
docker compose down
docker compose build --no-cache
docker compose up -d
\`\`\`

#### 3. Invalid token
\`\`\`bash
# Check if token has expired
# Login again to get fresh token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
\`\`\`

#### 4. Test errors
\`\`\`bash
# Clear pytest cache
docker compose exec user-api rm -rf .pytest_cache

# Run tests with more verbosity
docker compose exec user-api pytest -v -s
\`\`\`

### Logs and Debugging

\`\`\`bash
# View logs in real-time
docker compose logs -f user-api

# View specific logs
docker compose logs user-api | grep ERROR

# Access container for debugging
docker compose exec user-api bash

# Check application status
curl http://localhost:8000/debug
\`\`\`

## 📈 Future Improvements

### Planned Features

- [ ] **Role system** (Admin, User, Moderator)
- [ ] **Email verification** for new users
- [ ] **Password reset** via email
- [ ] **Rate limiting** for security
- [ ] **Monitoring and metrics** with Prometheus
- [ ] **Cache with Redis** for better performance
- [ ] **Push notifications**
- [ ] **API versioning** for compatibility
- [ ] **Extended documentation** with examples
- [ ] **CI/CD pipeline** with GitHub Actions

### Future Integrations

- [ ] **OAuth2** (Google, GitHub, Facebook)
- [ ] **Email sending** (SendGrid, AWS SES)
- [ ] **File storage** (AWS S3, Cloudinary)
- [ ] **Centralized logging** (ELK Stack)
- [ ] **Monitoring** (Grafana, DataDog)

## 🤝 Contributing

### How to Contribute

1. **Fork** the project
2. **Create branch** feature (`git checkout -b feature/new-feature`)
3. **Commit** changes (`git commit -am 'Add new feature'`)
4. **Push** to branch (`git push origin feature/new-feature`)
5. **Create Pull Request**

### Code Standards

- Use **Black** for formatting
- Follow **PEP 8** for style
- **Document** functions and classes
- **Write tests** for new functionality
- **Update README** if necessary

### Commit Structure

\`\`\`
type(scope): brief description

More detailed description if necessary

- Specific change 1
- Specific change 2
\`\`\`

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 📄 License

This project is under the **MIT License**. See `LICENSE` file for more details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/user-management-microservice/issues)
- **Documentation**: http://localhost:8000/docs
- **Email**: your-email@example.com

---

## 🎉 Ready to Use!

With this README you have all the information needed to:

✅ **Install** and configure the microservice  
✅ **Run** in development and production  
✅ **Test** all functionality  
✅ **Deploy** securely  
✅ **Maintain** and extend the code  
✅ **Contribute** to the project  

**Built with ❤️ using FastAPI, SQLite and development best practices.**

---

### 🚀 Quick Start con Makefile

\`\`\`bash
# Clone y start en 3 comandos con Makefile
git clone <repository-url>
cd user-management-microservice
make docker-run

# Crear usuario admin
make create-admin

# Verificar que funciona
make health

# Ver documentación
open http://localhost:8000/docs
\`\`\`

Your microservice is now running! 🎉

## 📖 Quick Reference

### 🌐 Important URLs
- **Application**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health
- **Debug Info**: http://localhost:8000/debug

### 🔑 Default Admin Credentials
After running `docker compose exec user-api python scripts/create_admin.py`:
- **Email**: admin@example.com
- **Password**: Admin123!

### 📋 Essential Commands (con Makefile)
\`\`\`bash
# Iniciar aplicación
make docker-run

# Ver logs
make docker-logs

# Crear usuario admin
make create-admin

# Ejecutar tests
make test

# Acceder a base de datos
make sqlite-shell

# Detener aplicación
make docker-stop

# Ver todos los comandos disponibles
make help
\`\`\`

### 🧪 Test User Creation
\`\`\`bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "password": "TestPass123!",
    "confirm_password": "TestPass123!"
  }'
