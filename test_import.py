#!/usr/bin/env python3
"""
Test script to verify the app can be imported correctly
"""

try:
    print("Testing imports...")
    
    # Test importing from app.py
    from app import app, application
    print("✅ Successfully imported 'app' from app.py")
    print("✅ Successfully imported 'application' from app.py")
    print(f"   App type: {type(app)}")
    
    # Test importing from main.py
    from main import app as main_app, application as main_application
    print("✅ Successfully imported 'app' from main.py")
    print("✅ Successfully imported 'application' from main.py")
    print(f"   Main app type: {type(main_app)}")
    
    print("\n🎉 All imports successful! The server should work now.")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()