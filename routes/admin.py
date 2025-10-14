from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import User, db
from utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/manage/admin')

@admin_bp.route('/managers')
@admin_required
def managers():
    """Display list of all Event Manager accounts"""
    event_managers = User.query.filter_by(role='event_manager').all()
    return render_template('admin/managers.html', managers=event_managers)

@admin_bp.route('/managers/create', methods=['POST'])
@admin_required
def create_manager():
    """Create new Event Manager account"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        flash('Username and password are required', 'error')
        return redirect(url_for('admin.managers'))
    
    # Check for duplicate username
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Username already exists', 'error')
        return redirect(url_for('admin.managers'))
    
    # Create new Event Manager
    new_manager = User(username=username, role='event_manager')
    new_manager.set_password(password)
    
    db.session.add(new_manager)
    db.session.commit()
    
    flash(f'Event Manager "{username}" created successfully', 'success')
    return redirect(url_for('admin.managers'))

@admin_bp.route('/managers/<int:id>/edit', methods=['POST'])
@admin_required
def edit_manager(id):
    """Update Event Manager account"""
    manager = User.query.get_or_404(id)
    
    if manager.role != 'event_manager':
        flash('Cannot edit non-Event Manager accounts', 'error')
        return redirect(url_for('admin.managers'))
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username:
        flash('Username is required', 'error')
        return redirect(url_for('admin.managers'))
    
    # Check for duplicate username (excluding current user)
    existing_user = User.query.filter(User.username == username, User.id != id).first()
    if existing_user:
        flash('Username already exists', 'error')
        return redirect(url_for('admin.managers'))
    
    manager.username = username
    if password:  # Only update password if provided
        manager.set_password(password)
    
    db.session.commit()
    
    flash(f'Event Manager "{username}" updated successfully', 'success')
    return redirect(url_for('admin.managers'))

@admin_bp.route('/managers/<int:id>/delete', methods=['POST'])
@admin_required
def delete_manager(id):
    """Delete Event Manager account"""
    manager = User.query.get_or_404(id)
    
    if manager.role != 'event_manager':
        flash('Cannot delete non-Event Manager accounts', 'error')
        return redirect(url_for('admin.managers'))
    
    username = manager.username
    db.session.delete(manager)
    db.session.commit()
    
    flash(f'Event Manager "{username}" deleted successfully', 'success')
    return redirect(url_for('admin.managers'))
