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


class TestGetPolitician:
    """Test suite for /api/politician/<politician_id> endpoint."""

    def test_get_politician_with_valid_id(self, client):
        """Get politician returns politician data for valid ID."""
        # First search to get a valid politician ID
        search_response = client.get("/api/politicians/search?name=Biden")
        search_data = json.loads(search_response.data)

        if len(search_data) > 0:
            politician_id = search_data[0]['politicianid']
            response = client.get(f"/api/politician/{politician_id}")
            assert response.status_code == 200

            data = json.loads(response.data)
            assert isinstance(data, dict)

            # Verify all required fields are present
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
                assert field in data

    def test_get_politician_returns_correct_data(self, client):
        """Get politician returns the correct politician data."""
        # First search to get a specific politician
        search_response = client.get("/api/politicians/search?name=Biden")
        search_data = json.loads(search_response.data)

        if len(search_data) > 0:
            expected_politician = search_data[0]
            politician_id = expected_politician['politicianid']

            response = client.get(f"/api/politician/{politician_id}")
            assert response.status_code == 200

            data = json.loads(response.data)

            # Verify the data matches what we found in search
            assert data['politicianid'] == expected_politician['politicianid']
            assert data['firstname'] == expected_politician['firstname']
            assert data['lastname'] == expected_politician['lastname']
            assert data['party'] == expected_politician['party']
            assert data['state'] == expected_politician['state']
            assert data['role'] == expected_politician['role']
            assert data['isactive'] == expected_politician['isactive']

    def test_get_politician_with_nonexistent_id(self, client):
        """Get politician returns 404 for nonexistent politician ID."""
        response = client.get("/api/politician/999999999")
        assert response.status_code == 404

        data = json.loads(response.data)
        assert "error" in data
        assert data["error"] == "Politician not found"

    def test_get_politician_with_valid_numeric_id(self, client):
        """Get politician handles valid numeric IDs correctly."""
        response = client.get("/api/politician/999999")
        # Should return 404 if ID doesn't exist, not a 500 error
        assert response.status_code in [200, 404]

    def test_sql_injection_in_politician_id(self, client):
        """SQL injection attempt in politician ID is blocked by Flask routing."""
        malicious_inputs = [
            "'; DROP TABLE Politicians; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM Politicians --",
            "Biden'; UPDATE Politicians SET Party='Hacked' --",
        ]

        for malicious_input in malicious_inputs:
            response = client.get(f"/api/politician/{malicious_input}")
            # Flask routing should reject non-integer values with 404
            assert response.status_code == 404

    def test_get_politician_with_invalid_id_type(self, client):
        """Get politician with non-integer ID returns 404."""
        invalid_ids = ["invalid", "Test%", "Test_", "O'Brien", "Smith-Jones", "abc123"]

        for politician_id in invalid_ids:
            response = client.get(f"/api/politician/{politician_id}")
            # Flask routing rejects non-integer IDs with 404
            assert response.status_code == 404

    def test_get_politician_with_negative_id(self, client):
        """Get politician with negative ID is rejected by Flask routing."""
        response = client.get("/api/politician/-1")
        # Flask routing rejects negative IDs for <int:> converters
        assert response.status_code == 404

    def test_get_politician_consistency_with_search(self, client):
        """Get politician returns data consistent with search results."""
        # Search for multiple politicians
        search_response = client.get("/api/politicians/search?name=Jo")
        search_data = json.loads(search_response.data)

        if len(search_data) >= 2:
            # Get details for first two politicians
            for politician in search_data[:2]:
                politician_id = politician['politicianid']
                response = client.get(f"/api/politician/{politician_id}")
                assert response.status_code == 200

                data = json.loads(response.data)
                # Verify data is identical to search result
                assert data == politician
