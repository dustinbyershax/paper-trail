"""Tests for politician search API endpoints.

Includes SQL injection protection validation and edge case testing.
"""

import pytest
import json


class TestPoliticiansSearch:
    """Test suite for /api/politicians/search endpoint."""

    def test_search_requires_minimum_length(self, client):
        """Search returns empty list for queries less than 2 characters."""
        response = client.get("/api/politicians/search?name=a")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_accepts_valid_length(self, client):
        """Search accepts queries of 2 or more characters."""
        response = client.get("/api/politicians/search?name=Jo")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_search_returns_politician_fields(self, client):
        """Search returns politicians with expected fields."""
        response = client.get("/api/politicians/search?name=Biden")
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data) > 0:
            politician = data[0]
            required_fields = [
                "politicianid",
                "firstname",
                "lastname",
                "party",
                "state",
                "role",
                "isactive",
            ]
            for field in required_fields:
                assert field in politician

    def test_search_is_case_insensitive(self, client):
        """Search matches regardless of case."""
        response_lower = client.get("/api/politicians/search?name=biden")
        response_upper = client.get("/api/politicians/search?name=BIDEN")
        response_mixed = client.get("/api/politicians/search?name=Biden")

        assert response_lower.status_code == 200
        assert response_upper.status_code == 200
        assert response_mixed.status_code == 200

        data_lower = json.loads(response_lower.data)
        data_upper = json.loads(response_upper.data)
        data_mixed = json.loads(response_mixed.data)

        assert len(data_lower) == len(data_upper) == len(data_mixed)

    def test_search_with_special_characters(self, client):
        """Search handles special characters without errors."""
        special_chars = ["O'Brien", "Smith-Jones", "Test%", "Test_"]

        for name in special_chars:
            response = client.get(f"/api/politicians/search?name={name}")
            assert response.status_code == 200
            data = json.loads(response.data)
            assert isinstance(data, list)

    def test_sql_injection_single_quote(self, client):
        """SQL injection attempt with single quote is safely handled."""
        malicious_input = "'; DROP TABLE Politicians; --"
        response = client.get(f"/api/politicians/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_sql_injection_union_select(self, client):
        """SQL injection UNION SELECT attempt is safely handled."""
        malicious_input = "' UNION SELECT * FROM Politicians --"
        response = client.get(f"/api/politicians/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_sql_injection_or_condition(self, client):
        """SQL injection OR 1=1 attempt is safely handled."""
        malicious_input = "' OR '1'='1"
        response = client.get(f"/api/politicians/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_sql_injection_comment_injection(self, client):
        """SQL injection comment injection attempt is safely handled."""
        malicious_input = "Biden' --"
        response = client.get(f"/api/politicians/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_sql_injection_semicolon_command(self, client):
        """SQL injection with semicolon command injection is safely handled."""
        malicious_input = "Biden'; UPDATE Politicians SET Party='Hacked' WHERE '1'='1"
        response = client.get(f"/api/politicians/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_search_with_empty_query_parameter(self, client):
        """Search with empty query parameter returns empty list."""
        response = client.get("/api/politicians/search?name=")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_without_query_parameter(self, client):
        """Search without query parameter returns empty list."""
        response = client.get("/api/politicians/search")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_with_spaces(self, client):
        """Search handles names with spaces correctly."""
        response = client.get("/api/politicians/search?name=Joe Biden")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_search_partial_match(self, client):
        """Search returns partial matches using ILIKE."""
        response = client.get("/api/politicians/search?name=John")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

        # If results exist, verify they contain 'John' in first or last name
        if len(data) > 0:
            for politician in data:
                full_name = f"{politician['firstname']} {politician['lastname']}"
                assert "john" in full_name.lower()
