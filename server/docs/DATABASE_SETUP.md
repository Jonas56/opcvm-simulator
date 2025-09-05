# Database Setup Guide for OPCVM Simulator

This guide explains how to set up and use the PostgreSQL database for the OPCVM Simulator application.

## Overview

The application has been migrated from hardcoded data and JSON files to a PostgreSQL database that stores:

- **Fund Performance Data**: Category, horizon years, cumulative returns
- **Fund Metadata**: NAV, risk profile, recommended holding period, objective, strategy
- **Category Defaults**: Tax rates and volatility by fund category

## Prerequisites

1. **PostgreSQL Database**: You need access to a PostgreSQL database
2. **Python Environment**: Make sure you have the required Python packages installed
3. **Environment Variables**: Set up your database connection string

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:

- `sqlalchemy>=2.0.0` - Database ORM
- `alembic>=1.13.0` - Database migrations
- `psycopg2-binary>=2.9.0` - PostgreSQL adapter
- `python-dotenv>=1.0.0` - Environment variable management

### 2. Set Up Environment Variables

Create a `.env` file in the `server/` directory:

```env
DATABASE_URL=postgresql://postgres:{password}@db.ujbaikdsmmszbjifugkl.jonas.co:5432/postgres
```

**Important**: Replace `{password}` with your actual database password.

### 3. Initialize the Database

Run the setup script to create tables and populate with initial data:

```bash
cd server
python setup_database.py
```

This script will:

- Create all necessary database tables
- Migrate all existing fund data from hardcoded sources and JSON files
- Verify the setup was successful

### 4. Verify the Setup

You can verify the database setup anytime:

```bash
python setup_database.py verify
```

## Database Schema

### Funds Table

| Column                | Type        | Description                               |
| --------------------- | ----------- | ----------------------------------------- |
| `id`                  | Integer     | Primary key                               |
| `name`                | String(255) | Fund name (unique)                        |
| `category`            | String(50)  | Fund category (Actions, Diversifié, etc.) |
| `horizon_years`       | Float       | Recommended investment horizon            |
| `cumulative_return`   | Float       | Historical cumulative return              |
| `nav`                 | Float       | Net Asset Value                           |
| `risk_profile`        | String(20)  | Risk level (low, medium, high)            |
| `recommended_holding` | String(20)  | Holding period (short, medium, long)      |
| `objective`           | Text        | Fund investment objective                 |
| `strategy`            | Text        | Fund investment strategy                  |
| `default_tax_rate`    | Float       | Default tax rate for category             |
| `default_volatility`  | Float       | Default volatility for category           |
| `created_at`          | DateTime    | Record creation timestamp                 |
| `updated_at`          | DateTime    | Record update timestamp                   |

## Running the Application

### Using the New Database Version

Start the server with database integration:

```bash
uvicorn server_db:app --reload --port 8000
```

### Using the Original Version (for comparison)

If you want to run the original version that uses JSON files:

```bash
uvicorn server:app --reload --port 8000
```

## API Endpoints

The new database version provides the same API endpoints as the original, plus additional ones:

### Core Endpoints

- `POST /deterministic` - Deterministic investment simulation
- `POST /mc-simulate` - Monte Carlo simulation
- `GET /funds` - Get all funds
- `GET /funds/{fund_name}` - Get specific fund

### New Endpoints

- `GET /funds/category/{category}` - Get funds by category
- `GET /categories` - Get all available categories
- `GET /health` - Health check

## Data Migration Details

The migration script (`migrations/001_initial_data.py`) combines data from:

1. **Hardcoded Performance Data** (from `opcvm_simulator.py`):

   - 15 funds with category, horizon years, and cumulative returns

2. **JSON Metadata** (from `funds.json`):

   - Fund metadata including NAV, risk profile, objective, strategy

3. **Category Defaults**:
   - Tax rates and volatility by fund category

## Troubleshooting

### Common Issues

1. **Database Connection Error**

   ```
   Error: DATABASE_URL environment variable is not set
   ```

   **Solution**: Make sure your `.env` file exists and contains the correct DATABASE_URL.

2. **Permission Denied**

   ```
   Error: permission denied for database
   ```

   **Solution**: Check your database credentials and permissions.

3. **Table Already Exists**

   ```
   Error: table "funds" already exists
   ```

   **Solution**: The migration is idempotent - it will skip if data already exists.

4. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'models'
   ```
   **Solution**: Make sure you're running scripts from the `server/` directory.

### Verification Commands

Check if the database is properly set up:

```bash
# Verify database setup
python setup_database.py verify

# Check fund count
python -c "
from database import SessionLocal
from models import Fund
db = SessionLocal()
print(f'Total funds: {db.query(Fund).count()}')
db.close()
"
```

## File Structure

```
server/
├── .env                          # Environment variables (create this)
├── requirements.txt              # Python dependencies
├── database.py                   # Database configuration
├── models.py                     # Database models
├── server_db.py                  # New FastAPI server (database version)
├── server.py                     # Original FastAPI server (JSON version)
├── opcvm_simulator_db.py         # New simulator (database version)
├── opcvm_simulator.py            # Original simulator (hardcoded version)
├── setup_database.py             # Database setup script
├── migrations/
│   ├── __init__.py
│   └── 001_initial_data.py       # Initial data migration
├── funds.json                    # Original JSON data (for reference)
└── DATABASE_SETUP.md             # This file
```

## Benefits of Database Migration

1. **Data Consistency**: All fund data is centralized in one place
2. **Scalability**: Easy to add new funds or update existing ones
3. **Performance**: Database queries are more efficient than file operations
4. **Flexibility**: Can easily add new fields or relationships
5. **Backup**: Database backups are more reliable than file backups
6. **Concurrency**: Multiple users can access data simultaneously

## Next Steps

After setting up the database:

1. **Test the API**: Use the new endpoints to verify everything works
2. **Update Client**: Modify your frontend to use the new database endpoints
3. **Add New Funds**: Use database management tools to add new funds
4. **Monitor Performance**: Check database performance and optimize if needed

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your database connection
3. Review the error messages carefully
4. Check that all dependencies are installed correctly
