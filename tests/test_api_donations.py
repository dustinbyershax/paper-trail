"""Tests for donation summary API endpoints.

Includes unfiltered and filtered donation summaries with SQL injection protection.
"""

import pytest
import json


class TestDonationSummary:
    """Test suite for /api/politician/<politician_id>/donations/summary endpoint."""

    def test_get_summary_with_valid_id(self, client):
        """Get donation summary returns list of industries and amounts."""
        response = client.get("/api/politician/1/donations/summary")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_summary_returns_expected_fields(self, client):
        """Each summary item includes industry and totalamount."""
        response = client.get("/api/politician/1/donations/summary")
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data) > 0:
            item = data[0]
            assert "industry" in item
            assert "totalamount" in item

    def test_summary_amounts_are_numeric(self, client):
        """Total amounts are returned as numeric values."""
        response = client.get("/api/politician/1/donations/summary")
        assert response.status_code == 200
        data = json.loads(response.data)

        for item in data:
            assert isinstance(item["totalamount"], (int, float))
            assert item["totalamount"] >= 0

    def test_summary_ordered_by_amount_desc(self, client):
        """Summary is ordered by total amount descending."""
        response = client.get("/api/politician/1/donations/summary")
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data) > 1:
            for i in range(len(data) - 1):
                assert data[i]["totalamount"] >= data[i + 1]["totalamount"]

    def test_summary_with_nonexistent_id(self, client):
        """Nonexistent politician ID returns empty list."""
        response = client.get("/api/politician/999999999/donations/summary")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_sql_injection_in_politician_id(self, client):
        """SQL injection in politician_id is blocked by Flask routing."""
        malicious_id = "1'; DROP TABLE donations; --"
        response = client.get(f"/api/politician/{malicious_id}/donations/summary")
        # Flask routing rejects non-integer IDs with 404
        assert response.status_code == 404


class TestFilteredDonationSummary:
    """Test suite for /api/politician/<politician_id>/donations/summary/filtered endpoint."""

    def test_filtered_summary_requires_topic(self, client):
        """Filtered summary requires topic parameter."""
        response = client.get("/api/politician/1/donations/summary/filtered")
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_filtered_summary_with_valid_topic(self, client):
        """Filtered summary with valid topic returns data."""
        valid_topics = ["Health", "Finance", "Technology", "Defense", "Energy"]

        for topic in valid_topics:
            response = client.get(
                f"/api/politician/1/donations/summary/filtered?topic={topic}"
            )
            assert response.status_code == 200
            data = json.loads(response.data)
            assert isinstance(data, list)

    def test_filtered_summary_with_invalid_topic(self, client):
        """Filtered summary with invalid topic returns empty list."""
        response = client.get(
            "/api/politician/1/donations/summary/filtered?topic=InvalidTopic"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_filtered_summary_returns_expected_fields(self, client):
        """Filtered summary items include industry and totalamount."""
        response = client.get(
            "/api/politician/1/donations/summary/filtered?topic=Health"
        )
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data) > 0:
            item = data[0]
            assert "industry" in item
            assert "totalamount" in item

    def test_filtered_summary_amounts_are_numeric(self, client):
        """Filtered summary amounts are numeric."""
        response = client.get(
            "/api/politician/1/donations/summary/filtered?topic=Health"
        )
        assert response.status_code == 200
        data = json.loads(response.data)

        for item in data:
            assert isinstance(item["totalamount"], (int, float))
            assert item["totalamount"] >= 0

    def test_filtered_summary_ordered_by_amount_desc(self, client):
        """Filtered summary is ordered by amount descending."""
        response = client.get(
            "/api/politician/1/donations/summary/filtered?topic=Health"
        )
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data) > 1:
            for i in range(len(data) - 1):
                assert data[i]["totalamount"] >= data[i + 1]["totalamount"]

    def test_filtered_summary_industries_match_topic(self, client):
        """Filtered summary returns only industries mapped to the topic."""
        topic_industry_map = {
            "Health": [
                "Health Professionals",
                "Pharmaceuticals",
                "Health Services",
                "Hospitals & Nursing Homes",
            ],
            "Finance": [
                "Real Estate",
                "Commercial Banks",
                "Securities & Investment",
                "Insurance",
                "Finance",
            ],
            "Technology": ["Telecom Services", "Internet", "Electronics"],
        }

        for topic, expected_industries in topic_industry_map.items():
            response = client.get(
                f"/api/politician/1/donations/summary/filtered?topic={topic}"
            )
            assert response.status_code == 200
            data = json.loads(response.data)

            for item in data:
                assert item["industry"] in expected_industries

    def test_sql_injection_in_politician_id_filtered(self, client):
        """SQL injection in politician_id for filtered endpoint is blocked by Flask routing."""
        malicious_id = "1'; DROP TABLE donations; --"
        response = client.get(
            f"/api/politician/{malicious_id}/donations/summary/filtered?topic=Health"
        )
        # Flask routing rejects non-integer IDs with 404
        assert response.status_code == 404

    def test_sql_injection_in_topic_parameter(self, client):
        """SQL injection in topic parameter is safely handled."""
        malicious_topic = "Health'; DROP TABLE donors; --"
        response = client.get(
            f"/api/politician/1/donations/summary/filtered?topic={malicious_topic}"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        # Should return empty list for unknown topic, not execute injection
        assert isinstance(data, list)

    def test_filtered_summary_with_special_characters(self, client):
        """Topic with special characters is handled safely."""
        special_topics = ["Health%", "Finance_", "Tech'OR'1'='1"]

        for topic in special_topics:
            response = client.get(
                f"/api/politician/1/donations/summary/filtered?topic={topic}"
            )
            assert response.status_code == 200
            data = json.loads(response.data)
            assert isinstance(data, list)

    def test_filtered_summary_with_empty_topic(self, client):
        """Empty topic parameter returns error."""
        response = client.get("/api/politician/1/donations/summary/filtered?topic=")
        assert response.status_code == 400

    def test_filtered_summary_case_sensitive_topic(self, client):
        """Topic matching is case-sensitive."""
        response_correct = client.get(
            "/api/politician/1/donations/summary/filtered?topic=Health"
        )
        response_lowercase = client.get(
            "/api/politician/1/donations/summary/filtered?topic=health"
        )

        assert response_correct.status_code == 200
        assert response_lowercase.status_code == 200

        data_correct = json.loads(response_correct.data)
        data_lowercase = json.loads(response_lowercase.data)

        # Lowercase should return empty since topics are case-sensitive
        assert isinstance(data_correct, list)
        assert data_lowercase == []

    def test_all_topic_mappings_exist(self, client):
        """All topics in TOPIC_INDUSTRY_MAP return results or empty list."""
        all_topics = [
            "Health",
            "Finance",
            "Technology",
            "Defense",
            "Energy",
            "Law",
            "Education",
            "Foreign Relations",
            "Government Operations",
        ]

        for topic in all_topics:
            response = client.get(
                f"/api/politician/1/donations/summary/filtered?topic={topic}"
            )
            assert response.status_code == 200
            data = json.loads(response.data)
            assert isinstance(data, list)
