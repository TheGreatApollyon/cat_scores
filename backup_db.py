#!/usr/bin/env python3
"""
Database Backup Script for Event Scoring System

This script creates a timestamped backup of the SQLite database.
"""

import os
import shutil
from datetime import datetime

def backup_database():
    """Create a backup of the SQLite database with timestamp"""
    
    # Database paths
    db_path = 'instance/event_scoring.db'
    backup_dir = 'instance/backups'
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"❌ Error: Database file not found at {db_path}")
        return False
    
    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'event_scoring_backup_{timestamp}.db'
    backup_path = os.path.join(backup_dir, backup_filename)
    
    try:
        # Copy database file
        shutil.copy2(db_path, backup_path)
        
        # Get file size
        file_size = os.path.getsize(backup_path)
        file_size_kb = file_size / 1024
        
        print(f"✓ Database backup created successfully!")
        print(f"  Location: {backup_path}")
        print(f"  Size: {file_size_kb:.2f} KB")
        print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # List all backups
        backups = sorted([f for f in os.listdir(backup_dir) if f.endswith('.db')])
        print(f"\n📁 Total backups: {len(backups)}")
        
        if len(backups) > 5:
            print(f"⚠️  You have {len(backups)} backups. Consider cleaning up old backups.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating backup: {str(e)}")
        return False

def list_backups():
    """List all available backups"""
    backup_dir = 'instance/backups'
    
    if not os.path.exists(backup_dir):
        print("No backups found.")
        return
    
    backups = sorted([f for f in os.listdir(backup_dir) if f.endswith('.db')])
    
    if not backups:
        print("No backups found.")
        return
    
    print(f"\n📁 Available backups ({len(backups)}):\n")
    for backup in backups:
        backup_path = os.path.join(backup_dir, backup)
        file_size = os.path.getsize(backup_path) / 1024
        mod_time = datetime.fromtimestamp(os.path.getmtime(backup_path))
        print(f"  • {backup}")
        print(f"    Size: {file_size:.2f} KB")
        print(f"    Created: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

def restore_backup(backup_filename):
    """Restore database from a backup"""
    db_path = 'instance/event_scoring.db'
    backup_path = os.path.join('instance/backups', backup_filename)
    
    if not os.path.exists(backup_path):
        print(f"❌ Error: Backup file not found: {backup_filename}")
        return False
    
    # Create a backup of current database before restoring
    if os.path.exists(db_path):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_backup = f'instance/event_scoring_before_restore_{timestamp}.db'
        shutil.copy2(db_path, temp_backup)
        print(f"✓ Current database backed up to: {temp_backup}")
    
    try:
        shutil.copy2(backup_path, db_path)
        print(f"✓ Database restored successfully from: {backup_filename}")
        return True
    except Exception as e:
        print(f"❌ Error restoring backup: {str(e)}")
        return False

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'list':
            list_backups()
        elif command == 'restore' and len(sys.argv) > 2:
            backup_filename = sys.argv[2]
            restore_backup(backup_filename)
        else:
            print("Usage:")
            print("  python backup_db.py           - Create a new backup")
            print("  python backup_db.py list      - List all backups")
            print("  python backup_db.py restore <filename> - Restore from backup")
    else:
        backup_database()
