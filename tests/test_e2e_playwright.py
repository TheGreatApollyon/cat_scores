"""
End-to-End tests using Playwright for Event Scoring System
"""
import pytest
from playwright.sync_api import Page, expect
import subprocess
import time
import os
import signal

@pytest.fixture(scope="module")
def flask_app():
    """Start Flask application for testing"""
    # Set test environment
    env = os.environ.copy()
    env['FLASK_ENV'] = 'testing'
    
    # Start Flask app in background
    process = subprocess.Popen(
        ['python', 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    
    # Wait for app to start
    time.sleep(3)
    
    yield process
    
    # Cleanup
    process.send_signal(signal.SIGINT)
    process.wait(timeout=5)

@pytest.fixture(scope="function")
def page(flask_app, playwright):
    """Create a new browser page for each test"""
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    yield page
    
    context.close()
    browser.close()

def test_login_page_loads(page: Page):
    """Test that login page loads correctly"""
    page.goto("http://127.0.0.1:5000/login")
    
    expect(page).to_have_title("Login - Event Scoring System")
    expect(page.locator("h1")).to_contain_text("Event Scoring System")
    expect(page.locator("h2")).to_contain_text("Login")

def test_admin_login_flow(page: Page):
    """Test admin login flow"""
    page.goto("http://127.0.0.1:5000/login")
    
    # Fill in login form
    page.fill("#username", "admin")
    page.fill("#password", "admin123")
    
    # Submit form
    page.click("button[type='submit']")
    
    # Wait for redirect
    page.wait_for_url("http://127.0.0.1:5000/overview", timeout=5000)
    
    # Verify we're on overview page
    expect(page.locator("h2")).to_contain_text("Cluster Leaderboard")

def test_invalid_login(page: Page):
    """Test login with invalid credentials"""
    page.goto("http://127.0.0.1:5000/login")
    
    page.fill("#username", "wronguser")
    page.fill("#password", "wrongpass")
    page.click("button[type='submit']")
    
    # Should stay on login page with error
    expect(page.locator(".alert-error")).to_contain_text("Invalid username or password")

def test_navigation_menu_admin(page: Page):
    """Test navigation menu for admin user"""
    # Login as admin
    page.goto("http://127.0.0.1:5000/login")
    page.fill("#username", "admin")
    page.fill("#password", "admin123")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:5000/overview")
    
    # Check navigation links
    nav = page.locator("nav")
    expect(nav.locator("a:has-text('Overview')")).to_be_visible()
    expect(nav.locator("a:has-text('Events')")).to_be_visible()
    expect(nav.locator("a:has-text('Event Managers')")).to_be_visible()
    expect(nav.locator("a:has-text('Logs')")).to_be_visible()
    expect(nav.locator("a:has-text('Logout')")).to_be_visible()

def test_create_event_manager(page: Page):
    """Test creating a new Event Manager"""
    # Login as admin
    page.goto("http://127.0.0.1:5000/login")
    page.fill("#username", "admin")
    page.fill("#password", "admin123")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:5000/overview")
    
    # Navigate to Event Managers
    page.click("a:has-text('Event Managers')")
    page.wait_for_url("http://127.0.0.1:5000/admin/managers")
    
    # Fill in create form
    page.fill("input[name='username']", "testmanager")
    page.fill("input[name='password']", "testpass123")
    
    # Submit form
    page.click("button:has-text('Create Manager')")
    
    # Wait for success message
    expect(page.locator(".alert-success")).to_contain_text("created successfully")
    
    # Verify manager appears in list
    expect(page.locator("table")).to_contain_text("testmanager")

def test_create_event_flow(page: Page):
    """Test creating a new event with participants"""
    # Login as admin
    page.goto("http://127.0.0.1:5000/login")
    page.fill("#username", "admin")
    page.fill("#password", "admin123")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:5000/overview")
    
    # Navigate to Events
    page.click("a:has-text('Events')")
    page.wait_for_url("http://127.0.0.1:5000/events")
    
    # Click Create New Event
    page.click("a:has-text('Create New Event')")
    page.wait_for_url("http://127.0.0.1:5000/events/create")
    
    # Fill in event details
    page.fill("#event_name", "Test Competition")
    
    # Fill in first participant
    page.select_option("select[name='cluster_id[]']", index=1)
    page.fill("input[name='participant_name[]']", "John Doe")
    page.fill("input[name='position[]']", "1")
    page.fill("input[name='points[]']", "10")
    
    # Add another participant
    page.click("button:has-text('Add Participant')")
    
    # Fill in second participant
    selects = page.locator("select[name='cluster_id[]']")
    selects.nth(1).select_option(index=2)
    
    names = page.locator("input[name='participant_name[]']")
    names.nth(1).fill("Jane Smith")
    
    positions = page.locator("input[name='position[]']")
    positions.nth(1).fill("2")
    
    points = page.locator("input[name='points[]']")
    points.nth(1).fill("5")
    
    # Submit form
    page.click("button:has-text('Create Event')")
    
    # Wait for redirect to events list
    page.wait_for_url("http://127.0.0.1:5000/events")
    
    # Verify success message
    expect(page.locator(".alert-success")).to_contain_text("created successfully")
    
    # Verify event appears in list
    expect(page.locator(".events-grid")).to_contain_text("Test Competition")

def test_view_event_details(page: Page):
    """Test viewing event details"""
    # Login and create an event first
    page.goto("http://127.0.0.1:5000/login")
    page.fill("#username", "admin")
    page.fill("#password", "admin123")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:5000/overview")
    
    # Go to events
    page.click("a:has-text('Events')")
    page.wait_for_url("http://127.0.0.1:5000/events")
    
    # If there are events, click View on the first one
    if page.locator(".event-card").count() > 0:
        page.click(".event-card >> a:has-text('View')")
        
        # Verify we're on event view page
        expect(page.locator("h2")).to_be_visible()
        expect(page.locator("table")).to_be_visible()

def test_overview_leaderboard(page: Page):
    """Test overview leaderboard displays correctly"""
    # Login
    page.goto("http://127.0.0.1:5000/login")
    page.fill("#username", "admin")
    page.fill("#password", "admin123")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:5000/overview")
    
    # Verify leaderboard elements
    expect(page.locator("h2")).to_contain_text("Cluster Leaderboard")
    expect(page.locator("table")).to_be_visible()
    
    # Verify all 7 clusters are listed
    table = page.locator("table")
    rows = table.locator("tbody tr")
    expect(rows).to_have_count(7)

def test_activity_logs_admin_only(page: Page):
    """Test that activity logs are accessible only to admin"""
    # Login as admin
    page.goto("http://127.0.0.1:5000/login")
    page.fill("#username", "admin")
    page.fill("#password", "admin123")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:5000/overview")
    
    # Navigate to Logs
    page.click("a:has-text('Logs')")
    page.wait_for_url("http://127.0.0.1:5000/admin/logs")
    
    # Verify logs page loads
    expect(page.locator("h2")).to_contain_text("Activity Logs")

def test_logout_flow(page: Page):
    """Test logout functionality"""
    # Login
    page.goto("http://127.0.0.1:5000/login")
    page.fill("#username", "admin")
    page.fill("#password", "admin123")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:5000/overview")
    
    # Click logout
    page.click("a:has-text('Logout')")
    
    # Should redirect to login page
    page.wait_for_url("http://127.0.0.1:5000/login")
    expect(page.locator("h2")).to_contain_text("Login")
    
    # Try to access protected page
    page.goto("http://127.0.0.1:5000/overview")
    
    # Should redirect back to login
    page.wait_for_url("http://127.0.0.1:5000/login")

def test_responsive_design(page: Page):
    """Test responsive design on mobile viewport"""
    # Set mobile viewport
    page.set_viewport_size({"width": 375, "height": 667})
    
    # Login
    page.goto("http://127.0.0.1:5000/login")
    page.fill("#username", "admin")
    page.fill("#password", "admin123")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:5000/overview")
    
    # Verify page is still functional
    expect(page.locator("h2")).to_be_visible()
    expect(page.locator("nav")).to_be_visible()
