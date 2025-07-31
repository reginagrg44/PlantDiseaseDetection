#!/usr/bin/env python3
"""
Setup script for Plant Disease Detection History Feature
Run this script to initialize the database and verify everything is working.
"""

import sqlite3
import os
from datetime import datetime

def setup_history_database():
    """Initialize the history database"""
    print("🔄 Setting up prediction history database...")
    
    try:
        # Import the database class
        from history_database import HistoryDatabase
        
        # Initialize database
        db = HistoryDatabase()
        print("✅ History database initialized successfully!")
        
        # Test database connection
        conn = sqlite3.connect('prediction_history.db')
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prediction_history';")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ Prediction history table created successfully!")
            
            # Check table structure
            cursor.execute("PRAGMA table_info(prediction_history);")
            columns = cursor.fetchall()
            print(f"📊 Table has {len(columns)} columns:")
            for col in columns:
                print(f"   - {col[1]} ({col[2]})")
        
        conn.close()
        
        return True
        
    except ImportError:
        print("❌ Error: history_database.py not found!")
        print("   Make sure you have copied the history_database.py file to your project folder.")
        return False
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        return False

def test_database_operations():
    """Test basic database operations"""
    print("\n🧪 Testing database operations...")
    
    try:
        from history_database import HistoryDatabase
        
        db = HistoryDatabase()
        
        # Test adding a record
        test_username = "test_user"
        test_record = {
            'username': test_username,
            'image_name': 'test_image.jpg',
            'prediction_type': 'Disease Detection',
            'predicted_disease': 'Tomato___Early_blight',
            'confidence_score': 95.5,
            'is_leaf': True,
            'cure_info': 'Test cure information'
        }
        
        db.add_prediction_record(**test_record)
        print("✅ Test record added successfully!")
        
        # Test retrieving records
        records = db.get_user_history(test_username)
        if records:
            print(f"✅ Retrieved {len(records)} record(s) for test user!")
        
        # Test statistics
        stats = db.get_history_stats(test_username)
        if stats:
            print(f"✅ Statistics generated: {stats[0]} total predictions")
        
        # Clean up test data
        db.delete_user_history(test_username)
        print("✅ Test data cleaned up!")
        
        print("🎉 All database operations working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing database: {str(e)}")
        return False

def check_file_requirements():
    """Check if all required files are present"""
    print("\n📁 Checking required files...")
    
    required_files = [
        'history_database.py',
        'history_view.py'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        print("   Please make sure all files are in your project directory.")
        return False
    else:
        print("\n🎉 All required files present!")
        return True

def show_integration_summary():
    """Show integration steps summary"""
    print("\n" + "="*60)
    print("📋 INTEGRATION SUMMARY")
    print("="*60)
    print("""
To integrate the history feature into your main application:

1. Add this import to your main file:
   from history_view import view_history_page, save_prediction_to_history

2. Add "View History" to your navigation menu

3. Add the history page handler in your app() function

4. Modify your Disease Prediction section to save predictions

See 'integration_instructions.md' for detailed steps!

🚀 Your history feature is ready to use!
""")

def main():
    """Main setup function"""
    print("🌱 Plant Disease Detection - History Feature Setup")
    print("="*55)
    
    # Check files
    if not check_file_requirements():
        return
    
    # Setup database
    if not setup_history_database():
        return
    
    # Test operations
    if not test_database_operations():
        return
    
    # Show summary
    show_integration_summary()

if __name__ == "__main__":
    main()