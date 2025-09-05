#!/usr/bin/env python3
"""
Database setup script for OPCVM Simulator.

This script:
1. Initializes the database tables
2. Runs the migration to populate with initial fund data
3. Verifies the setup was successful
"""

import sys
import os

# Add the current directory to Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import init_db, SessionLocal
from migrations.initial_data import run_migration
from models import Fund

def setup_database():
    """
    Complete database setup process.
    
    This function:
    1. Creates all database tables
    2. Populates the database with initial fund data
    3. Verifies the setup was successful
    """
    print("🚀 Starting OPCVM Simulator database setup...")
    
    try:
        # Step 1: Initialize database tables
        print("📋 Creating database tables...")
        init_db()
        print("✅ Database tables created successfully")
        
        # Step 2: Run migration to populate data
        print("📊 Populating database with fund data...")
        db = SessionLocal()
        try:
            run_migration(db)
            print("✅ Fund data migration completed")
            
            # Step 3: Verify setup
            print("🔍 Verifying database setup...")
            fund_count = db.query(Fund).count()
            print(f"✅ Database contains {fund_count} funds")
            
            # Show some sample data
            print("\n📈 Sample funds in database:")
            sample_funds = db.query(Fund).limit(3).all()
            for fund in sample_funds:
                print(f"  - {fund.name} ({fund.category})")
            
            print(f"\n🎉 Database setup completed successfully!")
            print(f"   Total funds: {fund_count}")
            print(f"   Categories: {[cat[0] for cat in db.query(Fund.category).distinct().all()]}")
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Database setup failed: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure your DATABASE_URL is set correctly in .env file")
        print("2. Ensure the PostgreSQL database is running and accessible")
        print("3. Check that all required packages are installed")
        print("4. Verify database permissions")
        sys.exit(1)

def verify_database():
    """
    Verify that the database is properly set up and contains data.
    """
    print("🔍 Verifying database setup...")
    
    try:
        db = SessionLocal()
        try:
            fund_count = db.query(Fund).count()
            if fund_count == 0:
                print("❌ Database is empty. Run setup_database() first.")
                return False
            
            print(f"✅ Database verification successful")
            print(f"   Found {fund_count} funds")
            return True
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Database verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        verify_database()
    else:
        setup_database()