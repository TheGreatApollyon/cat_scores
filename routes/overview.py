from flask import Blueprint, render_template
from models import Cluster
from utils.decorators import login_required

overview_bp = Blueprint('overview', __name__)

@overview_bp.route('/overview')
def public_overview():
    """Public display of cluster leaderboard with total points"""
    clusters = Cluster.query.all()
    
    # Calculate total points for each cluster and create leaderboard data
    leaderboard = []
    for cluster in clusters:
        total_points = cluster.get_total_points()
        leaderboard.append({
            'cluster': cluster,
            'total_points': total_points
        })
    
    # Sort by total points in descending order
    leaderboard.sort(key=lambda x: x['total_points'], reverse=True)
    
    return render_template('overview.html', leaderboard=leaderboard, public_view=True)

@overview_bp.route('/manage')
@login_required
def manage_overview():
    """Protected management view - redirects to events management"""
    return render_template('manage_dashboard.html')
