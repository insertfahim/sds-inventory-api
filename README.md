# SDS Chemical Inventory & Reporting System

A complete FastAPI backend project for managing Safety Data Sheet (SDS) Chemical Inventory with hybrid database access patterns using SQLAlchemy ORM and asyncpg.

## 🚀 Features

- **Hybrid Database Access**: Uses both SQLAlchemy ORM and asyncpg for optimal performance
- **Complete CRUD Operations**: Full Create, Read, Update, Delete operations for chemicals
- **Inventory Logging**: Track all chemical inventory changes with timestamps
- **Docker Support**: Complete containerization with PostgreSQL database
- **Automatic Migrations**: Alembic integration with automatic database setup
- **Environment Configuration**: Support for both local and Azure database configurations
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## 📋 Prerequisites

- Python 3.13+
- Docker and Docker Compose
- Git

## 🛠️ Setup Instructions

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chemical-inventory-system
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your database configuration
   ```

5. **Run the application**
   ```bash
   # Using Docker (Recommended)
   ./run.sh
   
   # Or manually with Docker Compose
   docker-compose up --build
   ```

### Environment Configuration

The system supports two environment configurations:

#### Local Development (.env)
```env
DATABASE_URL=postgresql://postgres:password@db:5432/chemical_inventory
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=chemical_inventory
ENVIRONMENT=local
```

#### Azure Production (.env)
```env
AZURE_DATABASE_URL=postgresql://username:password@server.postgres.database.azure.com:5432/database_name
ENVIRONMENT=azure
```

## 🐳 Docker Setup

### Quick Start
```bash
# Build and start all services
./run.sh

# Or manually
docker-compose up --build -d
```

### Services
- **API**: FastAPI application on port 8000
- **Database**: PostgreSQL 15 on port 5432

### Access Points
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### Chemical Management

#### Create Chemical
```http
POST /chemicals/
Content-Type: application/json

{
  "name": "Sodium Chloride",
  "cas_number": "7647-14-5",
  "quantity": 100.0,
  "unit": "kg"
}
```

#### Get All Chemicals
```http
GET /chemicals/
```

#### Get Chemical by ID
```http
GET /chemicals/{id}
```

#### Update Chemical
```http
PUT /chemicals/{id}
Content-Type: application/json

{
  "name": "Updated Name",
  "quantity": 150.0
}
```

#### Delete Chemical
```http
DELETE /chemicals/{id}
```

### Inventory Logging

#### Create Inventory Log
```http
POST /chemicals/{id}/log
Content-Type: application/json

{
  "action_type": "add",
  "quantity": 25.0
}
```

#### Get Chemical Logs
```http
GET /chemicals/{id}/logs
```

#### Get All Inventory Logs
```http
GET /inventory-logs/
```

#### Get Inventory Log by ID
```http
GET /inventory-logs/{log_id}
```

### Action Types
- `add`: Add quantity to inventory
- `remove`: Remove quantity from inventory
- `update`: Update inventory quantity

## 🗄️ Database Schema

### Chemicals Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String | Chemical name |
| cas_number | String | Chemical Abstract Service number |
| quantity | Float | Current quantity |
| unit | String | Unit of measurement (kg, L, g, etc.) |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### Inventory Logs Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| chemical_id | Integer | Foreign key to chemicals table |
| action_type | String | Type of action (add, remove, update) |
| quantity | Float | Quantity involved in the action |
| timestamp | DateTime | Action timestamp |

## 🔧 Technical Implementation

### Hybrid Database Access

The system implements a hybrid approach to database access:

- **SQLAlchemy ORM**: Used for complex operations, relationships, and CRUD operations
- **asyncpg**: Used for direct SQL queries where performance is critical

#### ORM Usage Examples
```python
# Create chemical (ORM)
db_chemical = Chemical(name="Sodium Chloride", cas_number="7647-14-5", quantity=100.0, unit="kg")
db.add(db_chemical)
await db.commit()

# Get all chemicals (ORM)
result = await db.execute(select(Chemical))
chemicals = result.scalars().all()
```

#### AsyncPG Usage Examples
```python
# Get chemical by ID (asyncpg)
conn = await get_asyncpg_connection()
query = "SELECT * FROM chemicals WHERE id = $1"
row = await conn.fetchrow(query, chemical_id)
```

### Database Migrations

Alembic is configured for automatic database migrations:

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🧪 Testing

### Manual Testing

1. **Start the application**
   ```bash
   ./run.sh
   ```

2. **Test endpoints using curl**
   ```bash
   # Create a chemical
   curl -X POST "http://localhost:8000/chemicals/" \
        -H "Content-Type: application/json" \
        -d '{"name": "Sodium Chloride", "cas_number": "7647-14-5", "quantity": 100.0, "unit": "kg"}'

   # Get all chemicals
   curl -X GET "http://localhost:8000/chemicals/"

   # Create inventory log
   curl -X POST "http://localhost:8000/chemicals/1/log" \
        -H "Content-Type: application/json" \
        -d '{"action_type": "add", "quantity": 25.0}'
   ```

3. **Use the interactive API documentation**
   - Visit http://localhost:8000/docs
   - Test endpoints directly in the browser

### Automated Testing

```bash
# Run tests (when implemented)
pytest tests/
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps
   
   # Check database logs
   docker-compose logs db
   ```

2. **Port Already in Use**
   ```bash
   # Stop existing services
   docker-compose down
   
   # Or change ports in docker-compose.yml
   ```

3. **Migration Errors**
   ```bash
   # Reset database
   docker-compose down -v
   docker-compose up --build
   ```

### Logs and Debugging

```bash
# View API logs
docker-compose logs api

# View database logs
docker-compose logs db

# Follow logs in real-time
docker-compose logs -f api
```

## 📊 Performance Considerations

- **Hybrid Access Pattern**: Uses ORM for complex operations and asyncpg for performance-critical queries
- **Connection Pooling**: SQLAlchemy connection pooling for efficient database connections
- **Async Operations**: All database operations are asynchronous for better concurrency
- **Indexing**: Primary keys and foreign keys are automatically indexed

## 🔒 Security Features

- **Input Validation**: Pydantic models validate all input data
- **SQL Injection Protection**: Parameterized queries prevent SQL injection
- **Environment Variables**: Sensitive data stored in environment variables
- **Database Isolation**: Each request uses isolated database connections

## 📈 Monitoring and Health Checks

- **Health Endpoint**: `/health` for application status
- **Database Health**: Automatic database connection verification
- **Migration Status**: Alembic tracks database schema version

## 🚀 Deployment

### Production Deployment

1. **Update environment variables**
   ```env
   ENVIRONMENT=azure
   AZURE_DATABASE_URL=your_azure_connection_string
   ```

2. **Build production image**
   ```bash
   docker build -t chemical-inventory-api .
   ```

3. **Deploy to your platform**
   - Azure Container Instances
   - AWS ECS
   - Google Cloud Run
   - Kubernetes

### Environment Variables for Production

```env
ENVIRONMENT=azure
AZURE_DATABASE_URL=postgresql://username:password@server.postgres.database.azure.com:5432/database_name
API_HOST=0.0.0.0
API_PORT=8000
```

## 📝 Development Guidelines

### Code Structure
```
app/
├── models/          # SQLAlchemy models
├── schemas/         # Pydantic schemas
├── api/endpoints/   # API route handlers
├── database/        # Database configuration
└── config/          # Application settings
```

### Adding New Features

1. **Create/Update Models**: Add new fields to SQLAlchemy models
2. **Update Schemas**: Add corresponding Pydantic schemas
3. **Create Endpoints**: Implement API endpoints with hybrid database access
4. **Create Migration**: Generate Alembic migration for database changes
5. **Update Tests**: Add tests for new functionality

### Code Style

- Follow PEP 8 guidelines
- Use type hints throughout
- Document all functions and classes
- Use meaningful variable and function names

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation at `/docs`

---

**Built with ❤️ using FastAPI, SQLAlchemy, and PostgreSQL**