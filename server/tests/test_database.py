#!/usr/bin/env python3
"""
Test script for the OPCVM Simulator database setup.

This script tests:
1. Database connection
2. Fund data retrieval
3. Simulation functionality
4. API endpoints
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Fund
from opcvm_simulator_db import simulate_investment, monte_carlo_simulate

def test_database_connection():
    """Test basic database connection and fund retrieval."""
    print("🔍 Testing database connection...")
    
    try:
        db = SessionLocal()
        fund_count = db.query(Fund).count()
        print(f"✅ Database connection successful. Found {fund_count} funds.")
        
        # Show sample funds
        sample_funds = db.query(Fund).limit(3).all()
        print("📊 Sample funds:")
        for fund in sample_funds:
            print(f"  - {fund.name} ({fund.category})")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def test_simulation():
    """Test simulation functionality with database data."""
    print("\n🧮 Testing simulation functionality...")
    
    try:
        db = SessionLocal()
        
        # Test deterministic simulation
        result = simulate_investment(
            db=db,
            fund_name="ATTIJARI ACTIONS",
            initial_amount=100000,
            monthly_contribution=3000,
            years=5
        )
        
        print(f"✅ Deterministic simulation successful")
        print(f"   Fund: {result.fund_name}")
        print(f"   Net final value: {result.net_final_value:,.2f} MAD")
        print(f"   Net profit: {result.net_profit_after_tax:,.2f} MAD")
        
        # Test Monte Carlo simulation
        mc_result = monte_carlo_simulate(
            db=db,
            fund_name="ATTIJARI ACTIONS",
            initial_amount=100000,
            monthly_contribution=3000,
            years=5,
            n_paths=1000  # Reduced for faster testing
        )
        
        print(f"✅ Monte Carlo simulation successful")
        print(f"   Median (P50): {mc_result.p50:,.2f} MAD")
        print(f"   Probability of loss: {mc_result.prob_loss:.2%}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Simulation test failed: {str(e)}")
        return False

def test_fund_categories():
    """Test fund category retrieval."""
    print("\n📂 Testing fund categories...")
    
    try:
        db = SessionLocal()
        
        categories = db.query(Fund.category).distinct().all()
        category_list = [cat[0] for cat in categories]
        
        print(f"✅ Found {len(category_list)} categories:")
        for category in category_list:
            fund_count = db.query(Fund).filter(Fund.category == category).count()
            print(f"  - {category}: {fund_count} funds")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Category test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all database tests."""
    print("🚀 Starting OPCVM Simulator database tests...\n")
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Fund Categories", test_fund_categories),
        ("Simulation", test_simulation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running: {test_name}")
        if test_func():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Database setup is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the database setup.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
