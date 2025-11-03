"""Tests for bills API endpoints.

Tests the bill subjects endpoint for data integrity and error handling.
"""

import pytest
import json


class TestBillSubjects:
    """Test suite for /api/bills/subjects endpoint."""

    def test_get_subjects_returns_list(self, client):
        """Get bill subjects returns a list."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_subjects_are_strings(self, client):
        """All subjects are strings."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)

        for subject in data:
            assert isinstance(subject, str)
            assert len(subject) > 0

    def test_subjects_are_unique(self, client):
        """All subjects are unique (no duplicates)."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)

        # Convert to set and compare length
        assert len(data) == len(set(data))

    def test_subjects_are_sorted(self, client):
        """Subjects are returned in alphabetical order."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data) > 1:
            # Check if list is sorted
            assert data == sorted(data)

    def test_subjects_no_null_values(self, client):
        """No null or empty subjects in the list."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)

        for subject in data:
            assert subject is not None
            assert subject != ""

    def test_subjects_endpoint_no_parameters(self, client):
        """Subjects endpoint does not require parameters."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200

    def test_subjects_endpoint_ignores_parameters(self, client):
        """Subjects endpoint ignores query parameters."""
        response1 = client.get("/api/bills/subjects")
        response2 = client.get("/api/bills/subjects?foo=bar")

        assert response1.status_code == 200
        assert response2.status_code == 200

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)

        # Should return same data regardless of parameters
        assert data1 == data2

    def test_subjects_sql_injection_in_query_string(self, client):
        """SQL injection attempts in query string are safely ignored."""
        malicious_params = [
            "?subject='; DROP TABLE Bills; --",
            "?param=' OR '1'='1",
            "?foo=1' UNION SELECT * FROM Bills --",
        ]

        for param in malicious_params:
            response = client.get(f"/api/bills/subjects{param}")
            assert response.status_code == 200
            data = json.loads(response.data)
            assert isinstance(data, list)

    def test_subjects_consistency_across_calls(self, client):
        """Multiple calls return consistent data."""
        response1 = client.get("/api/bills/subjects")
        response2 = client.get("/api/bills/subjects")

        assert response1.status_code == 200
        assert response2.status_code == 200

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)

        # Should return identical data
        assert data1 == data2

    def test_subjects_endpoint_returns_list(self, client):
        """Subjects endpoint returns a list (may be empty if no data)."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)

        # Should always return a list
        assert isinstance(data, list)

        # If data exists, verify it's properly structured
        for subject in data:
            assert isinstance(subject, str)
            assert len(subject) > 0
