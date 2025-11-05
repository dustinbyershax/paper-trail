"""Tests for donor search and donation API endpoints.

Includes SQL injection protection validation and data integrity tests.
"""

import pytest
import json


class TestDonorsSearch:
    """Test suite for /api/donors/search endpoint."""

    def test_search_requires_minimum_length(self, client):
        """Search returns empty list for queries less than 3 characters."""
        response = client.get("/api/donors/search?name=ab")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_single_char_returns_empty(self, client):
        """Search returns empty list for single character."""
        response = client.get("/api/donors/search?name=a")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_accepts_valid_length(self, client):
        """Search accepts queries of 3 or more characters."""
        response = client.get("/api/donors/search?name=John")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_search_returns_donor_fields(self, client):
        """Search returns donors with expected lowercase fields."""
        response = client.get("/api/donors/search?name=Smith")
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data) > 0:
            donor = data[0]
            required_fields = ["donorid", "name", "donortype", "employer", "state"]
            for field in required_fields:
                assert field in donor

    def test_search_is_case_insensitive(self, client):
        """Search matches regardless of case."""
        response_lower = client.get("/api/donors/search?name=smith")
        response_upper = client.get("/api/donors/search?name=SMITH")
        response_mixed = client.get("/api/donors/search?name=Smith")

        assert response_lower.status_code == 200
        assert response_upper.status_code == 200
        assert response_mixed.status_code == 200

        data_lower = json.loads(response_lower.data)
        data_upper = json.loads(response_upper.data)
        data_mixed = json.loads(response_mixed.data)

        assert len(data_lower) == len(data_upper) == len(data_mixed)

    def test_sql_injection_single_quote(self, client):
        """SQL injection attempt with single quote is safely handled."""
        malicious_input = "'; DROP TABLE Donors; --"
        response = client.get(f"/api/donors/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_sql_injection_union_select(self, client):
        """SQL injection UNION SELECT attempt is safely handled."""
        malicious_input = (
            "' UNION SELECT DonorID,Name,DonorType,Employer,State FROM Donors --"
        )
        response = client.get(f"/api/donors/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_sql_injection_or_condition(self, client):
        """SQL injection OR 1=1 attempt is safely handled."""
        malicious_input = "' OR '1'='1"
        response = client.get(f"/api/donors/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_sql_injection_comment_injection(self, client):
        """SQL injection comment injection attempt is safely handled."""
        malicious_input = "Smith' --"
        response = client.get(f"/api/donors/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_search_with_empty_query_parameter(self, client):
        """Search with empty query parameter returns empty list."""
        response = client.get("/api/donors/search?name=")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_without_query_parameter(self, client):
        """Search without query parameter returns empty list."""
        response = client.get("/api/donors/search")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_with_special_characters(self, client):
        """Search handles special characters without errors."""
        special_chars = ["O'Brien Corp", "Smith-Jones LLC", "Test%", "Test_"]

        for name in special_chars:
            response = client.get(f"/api/donors/search?name={name}")
            assert response.status_code == 200
            data = json.loads(response.data)
            assert isinstance(data, list)

    def test_search_partial_match(self, client):
        """Search returns partial matches using ILIKE."""
        response = client.get("/api/donors/search?name=Corp")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

        # If results exist, verify they contain 'Corp' in the name
        if len(data) > 0:
            for donor in data:
                assert "corp" in donor["name"].lower()


class TestGetDonor:
    """Test suite for /api/donor/<donor_id> endpoint."""

    def test_get_donor_with_valid_id(self, client):
        """Get donor returns donor data for valid ID."""
        # First search to get a valid donor ID
        search_response = client.get("/api/donors/search?name=Corp")
        search_data = json.loads(search_response.data)

        if len(search_data) > 0:
            donor_id = search_data[0]['donorid']
            response = client.get(f"/api/donor/{donor_id}")
            assert response.status_code == 200

            data = json.loads(response.data)
            assert isinstance(data, dict)

            # Verify all required fields are present
            required_fields = ["donorid", "name", "donortype", "employer", "state"]
            for field in required_fields:
                assert field in data

    def test_get_donor_returns_correct_data(self, client):
        """Get donor returns the correct donor data."""
        # First search to get a specific donor
        search_response = client.get("/api/donors/search?name=Corp")
        search_data = json.loads(search_response.data)

        if len(search_data) > 0:
            expected_donor = search_data[0]
            donor_id = expected_donor['donorid']

            response = client.get(f"/api/donor/{donor_id}")
            assert response.status_code == 200

            data = json.loads(response.data)

            # Verify the data matches what we found in search
            assert data['donorid'] == expected_donor['donorid']
            assert data['name'] == expected_donor['name']
            assert data['donortype'] == expected_donor['donortype']
            assert data['employer'] == expected_donor['employer']
            assert data['state'] == expected_donor['state']

    def test_get_donor_with_nonexistent_id(self, client):
        """Get donor returns 404 for nonexistent donor ID."""
        response = client.get("/api/donor/999999999")
        assert response.status_code == 404

        data = json.loads(response.data)
        assert "error" in data
        assert data["error"] == "Donor not found"

    def test_get_donor_with_invalid_id_type(self, client):
        """Get donor with non-integer ID returns 404."""
        response = client.get("/api/donor/invalid")
        assert response.status_code == 404

    def test_sql_injection_in_donor_id(self, client):
        """SQL injection attempt in donor ID is blocked by Flask routing."""
        malicious_inputs = [
            "1'; DROP TABLE Donors; --",
            "1 OR 1=1",
            "1 UNION SELECT * FROM Donors",
            "'; DELETE FROM Donors WHERE '1'='1",
        ]

        for malicious_input in malicious_inputs:
            response = client.get(f"/api/donor/{malicious_input}")
            # Flask routing should reject non-integer values with 404
            assert response.status_code == 404

    def test_get_donor_with_zero_id(self, client):
        """Get donor with zero ID returns 404 or data."""
        response = client.get("/api/donor/0")
        # Should return 404 if ID 0 doesn't exist
        assert response.status_code in [200, 404]

        if response.status_code == 404:
            data = json.loads(response.data)
            assert "error" in data

    def test_get_donor_with_negative_id(self, client):
        """Get donor with negative ID is rejected by Flask routing."""
        response = client.get("/api/donor/-1")
        # Flask routing rejects negative IDs for <int:> converters
        assert response.status_code == 404

    def test_get_donor_consistency_with_search(self, client):
        """Get donor returns data consistent with search results."""
        # Search for multiple donors
        search_response = client.get("/api/donors/search?name=LLC")
        search_data = json.loads(search_response.data)

        if len(search_data) >= 2:
            # Get details for first two donors
            for donor in search_data[:2]:
                donor_id = donor['donorid']
                response = client.get(f"/api/donor/{donor_id}")
                assert response.status_code == 200

                data = json.loads(response.data)
                # Verify data is identical to search result
                assert data == donor


class TestDonorDonations:
    """Test suite for /api/donor/<donor_id>/donations endpoint."""

    def test_get_donations_with_valid_id(self, client):
        """Get donations returns list for valid donor ID."""
        response = client.get("/api/donor/1/donations")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_get_donations_returns_expected_fields(self, client):
        """Donations include amount, date, and politician information."""
        response = client.get("/api/donor/1/donations")
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data) > 0:
            donation = data[0]
            required_fields = [
                "amount",
                "date",
                "firstname",
                "lastname",
                "party",
                "state",
            ]
            for field in required_fields:
                assert field in donation

    def test_get_donations_amount_is_numeric(self, client):
        """Donation amounts are returned as numeric values."""
        response = client.get("/api/donor/1/donations")
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data) > 0:
            for donation in data:
                assert isinstance(donation["amount"], (int, float))
                assert donation["amount"] >= 0

    def test_get_donations_with_nonexistent_id(self, client):
        """Get donations for nonexistent donor returns empty list or error."""
        response = client.get("/api/donor/999999999/donations")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_get_donations_with_invalid_id_type(self, client):
        """Get donations with non-integer ID returns 404."""
        response = client.get("/api/donor/invalid/donations")
        assert response.status_code == 404

    def test_sql_injection_in_donor_id_url(self, client):
        """SQL injection attempt in donor ID URL parameter is blocked by Flask routing."""
        malicious_inputs = [
            "1'; DROP TABLE Donations; --",
            "1 OR 1=1",
            "1 UNION SELECT * FROM Donors",
        ]

        for malicious_input in malicious_inputs:
            response = client.get(f"/api/donor/{malicious_input}/donations")
            # Flask routing should reject non-integer values with 404
            assert response.status_code == 404

    def test_get_donations_with_zero_id(self, client):
        """Get donations with zero ID returns data or empty list."""
        response = client.get("/api/donor/0/donations")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_get_donations_with_negative_id(self, client):
        """Get donations with negative ID is rejected by Flask routing."""
        response = client.get("/api/donor/-1/donations")
        # Flask routing rejects negative IDs for <int:> converters
        assert response.status_code == 404
