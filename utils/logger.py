from models import ActivityLog, db
from flask import session
import json

def log_activity(action, details=None):
    """
    Create ActivityLog entry for user actions
    
    Args:
        action: String describing the action (e.g., 'create_event', 'edit_event', 'delete_event')
        details: Dictionary with additional information about the action
    """
    if 'user_id' not in session:
        return
    
    details_json = None
    if details:
        details_json = json.dumps(details)
    
    log_entry = ActivityLog(
        user_id=session['user_id'],
        action=action,
        details=details_json
    )
    
    db.session.add(log_entry)
    db.session.commit()
