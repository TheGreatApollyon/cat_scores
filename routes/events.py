from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Event, Participant, Cluster, db
from utils.decorators import login_required
from utils.logger import log_activity

events_bp = Blueprint('events', __name__, url_prefix='/manage/events')

@events_bp.route('/')
@login_required
def list_events():
    """Display list of all events"""
    events = Event.query.order_by(Event.created_at.desc()).all()
    return render_template('events/list.html', events=events)

@events_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    """Create new event with participants"""
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        
        if not event_name:
            flash('Event name is required', 'error')
            return redirect(url_for('events.create_event'))
        
        # Create event
        event = Event(name=event_name, created_by=session['user_id'])
        db.session.add(event)
        db.session.flush()  # Get event ID
        
        # Process participants
        participant_count = 0
        cluster_ids = request.form.getlist('cluster_id[]')
        participant_names = request.form.getlist('participant_name[]')
        positions = request.form.getlist('position[]')
        points_list = request.form.getlist('points[]')
        
        for i in range(len(cluster_ids)):
            if cluster_ids[i] and participant_names[i]:
                try:
                    participant = Participant(
                        event_id=event.id,
                        cluster_id=int(cluster_ids[i]),
                        name=participant_names[i],
                        position=int(positions[i]),
                        points=int(points_list[i])
                    )
                    db.session.add(participant)
                    participant_count += 1
                except (ValueError, IndexError) as e:
                    flash(f'Invalid participant data: {str(e)}', 'error')
                    db.session.rollback()
                    return redirect(url_for('events.create_event'))
        
        if participant_count == 0:
            flash('At least one participant is required', 'error')
            db.session.rollback()
            return redirect(url_for('events.create_event'))
        
        db.session.commit()
        
        # Log activity
        log_activity('create_event', {
            'event_name': event_name,
            'event_id': event.id,
            'participant_count': participant_count
        })
        
        flash(f'Event "{event_name}" created successfully', 'success')
        return redirect(url_for('events.list_events'))
    
    # GET request - display form
    clusters = Cluster.query.order_by(Cluster.name).all()
    return render_template('events/create.html', clusters=clusters)

@events_bp.route('/<int:id>')
@login_required
def view_event(id):
    """View single event details"""
    event = Event.query.get_or_404(id)
    participants_by_cluster = event.get_participants_by_cluster()
    return render_template('events/view.html', event=event, participants_by_cluster=participants_by_cluster)

@events_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    """Edit existing event"""
    event = Event.query.get_or_404(id)
    
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        
        if not event_name:
            flash('Event name is required', 'error')
            return redirect(url_for('events.edit_event', id=id))
        
        old_name = event.name
        event.name = event_name
        
        # Delete existing participants
        Participant.query.filter_by(event_id=event.id).delete()
        
        # Add updated participants
        participant_count = 0
        cluster_ids = request.form.getlist('cluster_id[]')
        participant_names = request.form.getlist('participant_name[]')
        positions = request.form.getlist('position[]')
        points_list = request.form.getlist('points[]')
        
        for i in range(len(cluster_ids)):
            if cluster_ids[i] and participant_names[i]:
                try:
                    participant = Participant(
                        event_id=event.id,
                        cluster_id=int(cluster_ids[i]),
                        name=participant_names[i],
                        position=int(positions[i]),
                        points=int(points_list[i])
                    )
                    db.session.add(participant)
                    participant_count += 1
                except (ValueError, IndexError) as e:
                    flash(f'Invalid participant data: {str(e)}', 'error')
                    db.session.rollback()
                    return redirect(url_for('events.edit_event', id=id))
        
        if participant_count == 0:
            flash('At least one participant is required', 'error')
            db.session.rollback()
            return redirect(url_for('events.edit_event', id=id))
        
        db.session.commit()
        
        # Log activity
        log_activity('edit_event', {
            'event_name': event_name,
            'event_id': event.id,
            'old_name': old_name,
            'participant_count': participant_count
        })
        
        flash(f'Event "{event_name}" updated successfully', 'success')
        return redirect(url_for('events.view_event', id=id))
    
    # GET request - display form
    clusters = Cluster.query.order_by(Cluster.name).all()
    return render_template('events/edit.html', event=event, clusters=clusters)

@events_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_event(id):
    """Delete event"""
    event = Event.query.get_or_404(id)
    event_name = event.name
    
    db.session.delete(event)
    db.session.commit()
    
    # Log activity
    log_activity('delete_event', {
        'event_name': event_name,
        'event_id': id
    })
    
    flash(f'Event "{event_name}" deleted successfully', 'success')
    return redirect(url_for('events.list_events'))
