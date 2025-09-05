"""
Initial migration to populate the database with existing fund data.

This migration combines data from:
1. Hardcoded FUND_DATA in opcvm_simulator.py
2. JSON data in funds.json
3. Category-based defaults for tax rates and volatility
"""

import json
import os
import sys

# Add the parent directory to Python path so we can import our modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from sqlalchemy.orm import Session
from models import Fund

# Category-based defaults (from opcvm_simulator.py)
DEFAULT_TAX_BY_CATEGORY = {
    "Actions": 0.15,
    "Diversifié": 0.20,
    "Obligations": 0.20,
    "Taux": 0.20,
    "Monétaire": 0.20,
    "Trésorerie": 0.20,
}

DEFAULT_VOL_BY_CATEGORY = {
    "Actions": 0.20,
    "Diversifié": 0.12,
    "Obligations": 0.06,
    "Taux": 0.05,
    "Monétaire": 0.015,
    "Trésorerie": 0.02,
}

# Hardcoded performance data (from opcvm_simulator.py)
FUND_PERFORMANCE_DATA = {
    "ATTIJARI ACTIONS":            {"category": "Actions", "horizon_years": 5.0, "cum_return": 0.8782},
    "ATTIJARI AL MOUCHARAKA":      {"category": "Actions", "horizon_years": 5.0, "cum_return": 0.9080},
    "ATTIJARI DIVIDEND FUND":      {"category": "Actions", "horizon_years": 5.0, "cum_return": 0.3015},
    "ATTIJARI PATRIMOINE VALEURS": {"category": "Actions", "horizon_years": 5.0, "cum_return": 0.8183},
    "FCP ATTIJARI GOLD":           {"category": "Actions", "horizon_years": 5.0, "cum_return": 0.6279},
    "ATTIJARI DIVERSIFIE":         {"category": "Diversifié", "horizon_years": 4.0, "cum_return": 0.4583},
    "ATTIJARI PATRIMOINE DIVERSIFIE": {"category": "Diversifié", "horizon_years": 4.0, "cum_return": 0.5248},
    "WG OBLIGATIONS":              {"category": "Obligations", "horizon_years": 2.0, "cum_return": -0.2190},
    "ATTIJARI PATRIMOINE TAUX":    {"category": "Taux", "horizon_years": 2.0, "cum_return": 0.0980},
    "PATRIMOINE OBLIGATIONS":      {"category": "Obligations", "horizon_years": 2.0, "cum_return": 0.1613},
    "ATTIJARI MONETAIRE PLUS":     {"category": "Monétaire", "horizon_years": 0.5, "cum_return": 0.1139},
    "OBLIDYNAMIC":                 {"category": "Monétaire", "horizon_years": 0.5, "cum_return": 0.1232},
    "FCP CAP INSTITUTIONS":        {"category": "Monétaire", "horizon_years": 0.25, "cum_return": 0.1354},
    "ATTIJARI TRESORERIE":         {"category": "Trésorerie", "horizon_years": 1.0/12., "cum_return": 0.0991},
    "CAP MONETAIRE PREMIERE":      {"category": "Monétaire", "horizon_years": 1.0/12., "cum_return": 0.1252},
}

def load_json_funds_data():
    """Load fund metadata from the JSON file."""
    try:
        # Get the directory where this migration file is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to the server directory
        server_dir = os.path.dirname(current_dir)
        funds_file_path = os.path.join(server_dir, "funds.json")
        
        with open(funds_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Warning: funds.json not found at {funds_file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error reading funds.json: {e}")
        return {}

def migrate_funds_data(db: Session):
    """
    Migrate all fund data to the database.
    
    This function combines performance data from the hardcoded FUND_PERFORMANCE_DATA
    with metadata from the JSON file to create complete fund records.
    """
    # Load JSON metadata
    json_funds = load_json_funds_data()
    
    # Create funds from performance data
    for fund_name, perf_data in FUND_PERFORMANCE_DATA.items():
        # Get metadata from JSON if available
        metadata = json_funds.get(fund_name, {})
        
        # Get category-based defaults
        category = perf_data["category"]
        default_tax_rate = DEFAULT_TAX_BY_CATEGORY.get(category, 0.20)
        default_volatility = DEFAULT_VOL_BY_CATEGORY.get(category, 0.10)
        
        # Create fund record
        fund = Fund(
            name=fund_name,
            category=category,
            horizon_years=perf_data["horizon_years"],
            cumulative_return=perf_data["cum_return"],
            nav=metadata.get("nav"),
            risk_profile=metadata.get("riskProfile"),
            recommended_holding=metadata.get("recommendedHolding"),
            objective=metadata.get("objective"),
            strategy=metadata.get("strategy"),
            default_tax_rate=default_tax_rate,
            default_volatility=default_volatility
        )
        
        # Add to database
        db.add(fund)
        print(f"Added fund: {fund_name}")
    
    # Commit all changes
    db.commit()
    print(f"Successfully migrated {len(FUND_PERFORMANCE_DATA)} funds to database")

def run_migration(db: Session):
    """
    Run the initial migration.
    
    This function should be called to populate the database with initial fund data.
    """
    print("Starting initial fund data migration...")
    
    # Check if funds already exist
    existing_funds = db.query(Fund).count()
    if existing_funds > 0:
        print(f"Database already contains {existing_funds} funds. Skipping migration.")
        return
    
    # Run the migration
    migrate_funds_data(db)
    print("Migration completed successfully!")

if __name__ == "__main__":
    # This allows running the migration directly
    sys.path.append(parent_dir)  # Ensure parent directory is in path
    from database import SessionLocal
    
    db = SessionLocal()
    try:
        run_migration(db)
    finally:
        db.close()
