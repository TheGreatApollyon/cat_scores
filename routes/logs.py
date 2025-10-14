from flask import Blueprint, render_template
from models import ActivityLog
from utils.decorators import admin_required

logs_bp = Blueprint('logs', __name__, url_prefix='/manage/admin')

@logs_bp.route('/logs')
@admin_required
def view_logs():
    """Display activity logs in chronological order"""
    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).all()
    return render_template('admin/logs.html', logs=logs)
