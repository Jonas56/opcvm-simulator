# OPCVM Simulator Server

A FastAPI-based server for simulating OPCVM (Mutual Fund) investments with both deterministic and Monte Carlo approaches.

## 🏗️ Project Structure

```
server/
├── app/                          # Main application package
│   ├── main.py                   # FastAPI app entry point
│   ├── api/                      # API routes
│   │   ├── v1/                   # API version 1
│   │   │   ├── endpoints/        # Individual endpoint modules
│   │   │   │   ├── funds.py      # Fund-related endpoints
│   │   │   │   ├── simulation.py # Simulation endpoints
│   │   │   │   └── health.py     # Health check endpoints
│   │   │   └── api.py            # API router
│   │   └── deps.py               # Dependencies
│   ├── core/                     # Core configuration
│   │   ├── config.py             # Settings and configuration
│   │   └── database.py           # Database configuration
│   ├── models/                   # Database models
│   │   └── fund.py               # Fund model
│   ├── services/                 # Business logic
│   │   ├── fund_service.py       # Fund-related business logic
│   │   └── simulation_service.py # Simulation business logic
│   ├── schemas/                  # Pydantic models
│   │   ├── fund.py               # Fund schemas
│   │   └── simulation.py         # Simulation schemas
│   └── utils/                    # Utility functions
├── migrations/                   # Database migrations
├── tests/                        # Test files
├── data/                         # Static data files
├── scripts/                      # Utility scripts
├── docs/                         # Documentation
└── requirements.txt              # Python dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the `server/` directory:

```env
DATABASE_URL=postgresql://postgres:{password}@db.ujbaikdsmmszbjifugkl.jonas.co:5432/postgres
ENVIRONMENT=development
DEBUG=True
```

### 3. Initialize Database

```bash
python scripts/setup_database.py
```

### 4. Run the Server

```bash
# Using the new structure
python run.py

# Or using uvicorn directly
uvicorn app.main:app --reload --port 8000
```

## 📚 API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🔧 API Endpoints

### Funds

- `GET /api/v1/funds/` - Get all funds with pagination
- `GET /api/v1/funds/{fund_name}` - Get specific fund
- `GET /api/v1/funds/category/{category}` - Get funds by category
- `GET /api/v1/funds/categories/list` - Get all categories
- `POST /api/v1/funds/` - Create new fund
- `PUT /api/v1/funds/{fund_name}` - Update fund
- `DELETE /api/v1/funds/{fund_name}` - Delete fund

### Simulation

- `POST /api/v1/simulation/deterministic` - Deterministic simulation
- `POST /api/v1/simulation/monte-carlo` - Monte Carlo simulation

### Health

- `GET /api/v1/health/` - Basic health check
- `GET /api/v1/health/db` - Database health check

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api/

# Run with coverage
pytest --cov=app
```

## 🔄 Migration from Old Structure

The old files are still available for reference:

- `server.py` - Original FastAPI server
- `opcvm_simulator.py` - Original simulation logic
- `server_db.py` - Database version of original server

## 📖 Key Features

- **Modular Architecture**: Clean separation of concerns
- **Type Safety**: Full type hints and Pydantic validation
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **API Versioning**: Structured for future API versions
- **Comprehensive Testing**: Unit and integration tests
- **Documentation**: Auto-generated API documentation
- **Error Handling**: Proper HTTP status codes and error messages

## 🛠️ Development

### Adding New Endpoints

1. Create endpoint file in `app/api/v1/endpoints/`
2. Add router to `app/api/v1/api.py`
3. Add corresponding service in `app/services/`
4. Add schemas in `app/schemas/`

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## 📝 Environment Variables

| Variable       | Description                          | Default     |
| -------------- | ------------------------------------ | ----------- |
| `DATABASE_URL` | PostgreSQL connection string         | Required    |
| `ENVIRONMENT`  | Environment (development/production) | development |
| `DEBUG`        | Enable debug mode                    | True        |

## 🤝 Contributing

1. Follow the existing code structure
2. Add type hints to all functions
3. Include docstrings for all public methods
4. Write tests for new functionality
5. Update documentation as needed
