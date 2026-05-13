"""
SC Chatbot E2E Test Configuration

Pytest fixtures and conftest for Playwright testing.
"""

import pytest
from playwright.sync_api import sync_playwright
import sys
import os

# Add backend path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'backend'))


@pytest.fixture(scope="session")
def browser():
    """Browser fixture for E2E tests."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # Set True for CI environments
            slow_mo=500,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-gpu',
                '--no-sandbox',
            ],
        )
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Page fixture for E2E tests."""
    page = browser.new_page()
    page.goto('/')
    yield page
    # page.close()


@pytest.fixture
def backend_server():
    """FastAPI backend server fixture."""
    from src.backend.main import app
    from fastapi.testclient import TestClient
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    yield client
    client.close()


@pytest.fixture
def api_client(backend_server):
    """API client fixture."""
    return backend_server


@pytest.fixture
def tenant1(api_client):
    """Test tenant 1."""
    data = api_client.post(
        '/auth/register',
        json={
            'tenant_key': 'test-tenant-1',
            'tenant_name': 'Test Tenant 1',
            'email': 'admin@test.com',
            'password': 'password123',
        },
    )
    assert data.status_code == 200


@pytest.fixture
def tenant2(api_client):
    """Test tenant 2."""
    data = api_client.post(
        '/auth/register',
        json={
            'tenant_key': 'test-tenant-2',
            'tenant_name': 'Test Tenant 2',
            'email': 'admin2@test.com',
            'password': 'password123',
        },
    )
    assert data.status_code == 200


@pytest.fixture
def tenant3(api_client):
    """Test tenant 3."""
    data = api_client.post(
        '/auth/register',
        json={
            'tenant_key': 'test-tenant-3',
            'tenant_name': 'Test Tenant 3',
            'email': 'admin3@test.com',
            'password': 'password123',
        },
    )
    assert data.status_code == 200


@pytest.fixture(scope="session")
def test_data():
    """Test data setup."""
    return {
        'tenant1': 'test-tenant-1',
        'tenant2': 'test-tenant-2',
        'tenant3': 'test-tenant-3',
    }


@pytest.fixture
def cleanup():
    """Cleanup fixture."""
    yield
    # Cleanup code here
    print("Cleanup complete")


def pytest_configure(config):
    """Pytest configuration."""
    config.addinivalue_line(
        "markers", "POC: mark test as POC phase (months 1-3)"
    )
    config.addinivalue_line(
        "markers", "MVP: mark test as MVP phase (months 4-9)"
    )
    config.addinivalue_line(
        "markers", "PRODUCTION: mark test as Production phase (months 10-21)"
    )