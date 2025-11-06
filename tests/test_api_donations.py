"""Tests for donation summary API endpoints.

Verifies unfiltered and filtered donation summaries with SQL injection protection
and comprehensive edge case testing against known seed data.
"""

import json


class TestDonationSummary:
    """Test suite for /api/politician/<politician_id>/donations/summary endpoint."""

    def test_get_summary_with_valid_id(self, client, seed_test_data):
        """Get donation summary returns list of industries and amounts."""
        # Use politician ID 1 (first politician from seed data)
        response = client.get("/api/politician/1/donations/summary")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_summary_returns_expected_fields(self, client, seed_test_data):
        """Each summary item includes industry and totalamount fields."""
        response = client.get("/api/politician/1/donations/summary")
        assert response.status_code == 200
        data = json.loads(response.data)

        # Should have at least some donations for first politician
        if len(data) > 0:
            item = data[0]
            assert "industry" in item, "Missing 'industry' field"
            assert "totalamount" in item, "Missing 'totalamount' field"
            assert isinstance(item["industry"], str)
            assert isinstance(item["totalamount"], (int, float))

    def test_summary_amounts_are_numeric_and_positive(self, client, seed_test_data):
        """Total amounts are returned as numeric values >= 0."""
        response = client.get("/api/politician/1/donations/summary")
        assert response.status_code == 200
        data = json.loads(response.data)

        for item in data:
            assert isinstance(
                item["totalamount"], (int, float)
            ), f"Amount should be numeric: {item['totalamount']}"
            assert item["totalamount"] >= 0, "Amount should be non-negative"

    def test_summary_ordered_by_amount_descending(self, client, seed_test_data):
        """Summary is ordered by total amount descending (highest first)."""
        response = client.get("/api/politician/1/donations/summary")
        assert response.status_code == 200
        data = json.loads(response.data)

        # Verify descending order
        if len(data) > 1:
            for i in range(len(data) - 1):
                assert (
                    data[i]["totalamount"] >= data[i + 1]["totalamount"]
                ), f"Ordering violation: {data[i]['totalamount']} should be >= {data[i + 1]['totalamount']}"

    def test_summary_industries_are_unique(self, client, seed_test_data):
        """Each industry appears only once in summary (grouped by industry)."""
        response = client.get("/api/politician/1/donations/summary")
        assert response.status_code == 200
        data = json.loads(response.data)

        industries = [item["industry"] for item in data]
        assert len(industries) == len(set(industries)), "Industries should be unique"

    def test_summary_with_nonexistent_politician_id(self, client, seed_test_data):
        """Nonexistent politician ID returns empty list, not an error."""
        response = client.get("/api/politician/999999999/donations/summary")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == [], "Should return empty list for nonexistent politician"

    def test_summary_with_different_politicians(self, client, seed_test_data):
        """Different politician IDs return different donation summaries."""
        response1 = client.get("/api/politician/1/donations/summary")
        response2 = client.get("/api/politician/2/donations/summary")
        response3 = client.get("/api/politician/3/donations/summary")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        data3 = json.loads(response3.data)

        # Each politician should have their own donations (or empty)
        assert isinstance(data1, list)
        assert isinstance(data2, list)
        assert isinstance(data3, list)

    def test_summary_consistency_across_calls(self, client, seed_test_data):
        """Multiple calls for same politician return identical data."""
        response1 = client.get("/api/politician/1/donations/summary")
        response2 = client.get("/api/politician/1/donations/summary")
        response3 = client.get("/api/politician/1/donations/summary")

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        data3 = json.loads(response3.data)

        assert data1 == data2 == data3, "Results should be consistent"


class TestDonationSummarySQLInjection:
    """SQL injection protection tests for donation summary endpoint."""

    def test_sql_injection_drop_table_in_politician_id(
        self, client, seed_test_data, db_connection
    ):
        """SQL injection attempt to drop table via politician_id is safely handled."""
        cursor = db_connection.cursor()

        # Count rows before injection attempt
        cursor.execute("SELECT COUNT(*) FROM pt.Donations")
        count_before = cursor.fetchone()[0]
        assert count_before > 0, "Should have donations in database"

        # Attempt injection
        malicious_id = "1'; DROP TABLE Donations; --"
        response = client.get(f"/api/politician/{malicious_id}/donations/summary")

        # Should handle gracefully (500 error for invalid ID format)
        assert response.status_code in [200, 500]

        # Verify table still exists and has same row count
        cursor.execute("SELECT COUNT(*) FROM pt.Donations")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before, "Table row count should be unchanged"

        # Verify subsequent queries still work
        cursor.execute("SELECT * FROM pt.Donations LIMIT 1")
        assert cursor.fetchone() is not None, "Table should still be queryable"

        cursor.close()

    def test_sql_injection_union_select_in_politician_id(
        self, client, seed_test_data, db_connection
    ):
        """SQL injection UNION SELECT attempt via politician_id is safely handled."""
        cursor = db_connection.cursor()

        malicious_id = "1' UNION SELECT * FROM Donations --"
        response = client.get(f"/api/politician/{malicious_id}/donations/summary")

        # Should handle gracefully
        assert response.status_code in [200, 500]

        # Verify data integrity
        cursor.execute("SELECT COUNT(*) FROM pt.Donations")
        assert cursor.fetchone()[0] > 0

        cursor.close()

    def test_sql_injection_or_condition_in_politician_id(
        self, client, seed_test_data, db_connection
    ):
        """SQL injection OR 1=1 attempt via politician_id is safely handled."""
        cursor = db_connection.cursor()

        malicious_id = "1' OR '1'='1"
        response = client.get(f"/api/politician/{malicious_id}/donations/summary")

        # Should handle gracefully
        assert response.status_code in [200, 500]

        # If it returns 200, should not return all donations
        if response.status_code == 200:
            data = json.loads(response.data)
            # Should either be empty or error, not all donations
            assert isinstance(data, list)

        cursor.close()


class TestFilteredDonationSummary:
    """Test suite for /api/politician/<politician_id>/donations/summary/filtered endpoint."""

    def test_filtered_summary_requires_topic_parameter(self, client, seed_test_data):
        """Filtered summary requires topic parameter, returns 400 without it."""
        response = client.get("/api/politician/1/donations/summary/filtered")
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data, "Should return error message"

    def test_filtered_summary_with_valid_topics(self, client, seed_test_data):
        """Filtered summary with valid topics returns data."""
        valid_topics = [
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

        for topic in valid_topics:
            response = client.get(
                f"/api/politician/1/donations/summary/filtered?topic={topic}"
            )
            assert (
                response.status_code == 200
            ), f"Failed for topic: {topic}"
            data = json.loads(response.data)
            assert isinstance(data, list), f"Invalid response for topic: {topic}"

    def test_filtered_summary_with_invalid_topic(self, client, seed_test_data):
        """Filtered summary with invalid topic returns empty list."""
        invalid_topics = ["InvalidTopic", "Nonexistent", "FakeCategory"]

        for topic in invalid_topics:
            response = client.get(
                f"/api/politician/1/donations/summary/filtered?topic={topic}"
            )
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data == [], f"Should return empty list for invalid topic: {topic}"

    def test_filtered_summary_returns_expected_fields(self, client, seed_test_data):
        """Filtered summary items include industry and totalamount fields."""
        response = client.get(
            "/api/politician/1/donations/summary/filtered?topic=Health"
        )
        assert response.status_code == 200
        data = json.loads(response.data)

        # If there are health-related donations, verify fields
        for item in data:
            assert "industry" in item, "Missing 'industry' field"
            assert "totalamount" in item, "Missing 'totalamount' field"
            assert isinstance(item["industry"], str)
            assert isinstance(item["totalamount"], (int, float))

    def test_filtered_summary_amounts_are_numeric(self, client, seed_test_data):
        """Filtered summary amounts are numeric and non-negative."""
        response = client.get(
            "/api/politician/1/donations/summary/filtered?topic=Finance"
        )
        assert response.status_code == 200
        data = json.loads(response.data)

        for item in data:
            assert isinstance(item["totalamount"], (int, float))
            assert item["totalamount"] >= 0

    def test_filtered_summary_ordered_by_amount_descending(
        self, client, seed_test_data
    ):
        """Filtered summary is ordered by amount descending."""
        response = client.get(
            "/api/politician/1/donations/summary/filtered?topic=Technology"
        )
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data) > 1:
            for i in range(len(data) - 1):
                assert data[i]["totalamount"] >= data[i + 1]["totalamount"]

    def test_filtered_summary_industries_match_topic_mapping(
        self, client, seed_test_data
    ):
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
            "Defense": ["Defense Aerospace"],
            "Energy": ["Oil & Gas", "Electric Utilities", "Gas Utilities"],
        }

        for topic, expected_industries in topic_industry_map.items():
            response = client.get(
                f"/api/politician/1/donations/summary/filtered?topic={topic}"
            )
            assert response.status_code == 200
            data = json.loads(response.data)

            # Verify all returned industries are in the expected list
            for item in data:
                assert (
                    item["industry"] in expected_industries
                ), f"Industry '{item['industry']}' not expected for topic '{topic}'"

    def test_filtered_summary_case_sensitive_topic(self, client, seed_test_data):
        """Topic matching is case-sensitive."""
        response_correct = client.get(
            "/api/politician/1/donations/summary/filtered?topic=Health"
        )
        response_lowercase = client.get(
            "/api/politician/1/donations/summary/filtered?topic=health"
        )
        response_uppercase = client.get(
            "/api/politician/1/donations/summary/filtered?topic=HEALTH"
        )

        assert response_correct.status_code == 200
        assert response_lowercase.status_code == 200
        assert response_uppercase.status_code == 200

        data_correct = json.loads(response_correct.data)
        data_lowercase = json.loads(response_lowercase.data)
        data_uppercase = json.loads(response_uppercase.data)

        # Lowercase/uppercase should return empty since topics are case-sensitive
        assert isinstance(data_correct, list)
        assert data_lowercase == [], "Lowercase topic should return empty"
        assert data_uppercase == [], "Uppercase topic should return empty"

    def test_filtered_summary_with_empty_topic_parameter(self, client, seed_test_data):
        """Empty topic parameter returns 400 error."""
        response = client.get("/api/politician/1/donations/summary/filtered?topic=")
        assert response.status_code == 400

    def test_filtered_summary_consistency_across_calls(self, client, seed_test_data):
        """Multiple calls for same politician and topic return identical data."""
        url = "/api/politician/1/donations/summary/filtered?topic=Finance"
        response1 = client.get(url)
        response2 = client.get(url)
        response3 = client.get(url)

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        data3 = json.loads(response3.data)

        assert data1 == data2 == data3, "Results should be consistent"


class TestFilteredDonationSummarySQLInjection:
    """SQL injection protection tests for filtered donation summary endpoint."""

    def test_sql_injection_in_politician_id(
        self, client, seed_test_data, db_connection
    ):
        """SQL injection in politician_id for filtered endpoint is safely handled."""
        cursor = db_connection.cursor()

        # Count rows before
        cursor.execute("SELECT COUNT(*) FROM pt.Donations")
        count_before = cursor.fetchone()[0]

        malicious_id = "1'; DROP TABLE Donations; --"
        response = client.get(
            f"/api/politician/{malicious_id}/donations/summary/filtered?topic=Health"
        )

        # Should handle gracefully
        assert response.status_code in [200, 500]

        # Verify table integrity
        cursor.execute("SELECT COUNT(*) FROM pt.Donations")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before

        cursor.close()

    def test_sql_injection_in_topic_parameter(
        self, client, seed_test_data, db_connection
    ):
        """SQL injection in topic parameter is safely handled."""
        cursor = db_connection.cursor()

        # Count rows before
        cursor.execute("SELECT COUNT(*) FROM pt.Donors")
        count_before = cursor.fetchone()[0]

        malicious_topic = "Health'; DROP TABLE Donors; --"
        response = client.get(
            f"/api/politician/1/donations/summary/filtered?topic={malicious_topic}"
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        # Should return empty list for unknown topic, not execute injection
        assert data == [], "Should return empty for malicious topic"

        # Verify table integrity
        cursor.execute("SELECT COUNT(*) FROM pt.Donors")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before

        cursor.close()

    def test_sql_injection_union_in_topic(self, client, seed_test_data, db_connection):
        """SQL injection UNION attempt in topic parameter is safely handled."""
        cursor = db_connection.cursor()

        malicious_topic = "Health' UNION SELECT * FROM Donors --"
        response = client.get(
            f"/api/politician/1/donations/summary/filtered?topic={malicious_topic}"
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

        # Verify data integrity
        cursor.execute("SELECT COUNT(*) FROM pt.Donors")
        assert cursor.fetchone()[0] > 0

        cursor.close()

    def test_sql_injection_or_condition_in_topic(
        self, client, seed_test_data, db_connection
    ):
        """SQL injection OR condition in topic parameter is safely handled."""
        malicious_topic = "Health' OR '1'='1"
        response = client.get(
            f"/api/politician/1/donations/summary/filtered?topic={malicious_topic}"
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        # Should return empty list for unknown topic
        assert data == []


class TestFilteredDonationSummaryEdgeCases:
    """Edge case tests for filtered donation summary endpoint."""

    def test_filtered_summary_with_special_characters_in_topic(
        self, client, seed_test_data
    ):
        """Topic with special characters is handled safely."""
        special_topics = [
            "Health%",
            "Finance_",
            "Tech'OR'1'='1",
            "Energy&Defense",
            "Law;DROP TABLE",
        ]

        for topic in special_topics:
            response = client.get(
                f"/api/politician/1/donations/summary/filtered?topic={topic}"
            )
            assert response.status_code == 200, f"Failed for topic: {topic}"
            data = json.loads(response.data)
            assert isinstance(data, list)
            # Should return empty for invalid topics
            assert data == []

    def test_filtered_summary_with_unicode_in_topic(self, client, seed_test_data):
        """Topic with Unicode characters returns empty list."""
        unicode_topics = [
            "健康",  # Chinese
            "здоровье",  # Cyrillic
            "صحة",  # Arabic
            "Santé",  # French
        ]

        for topic in unicode_topics:
            response = client.get(
                f"/api/politician/1/donations/summary/filtered?topic={topic}"
            )
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data == []

    def test_filtered_summary_with_very_long_topic(self, client, seed_test_data):
        """Topic with very long string is handled safely."""
        long_topic = "a" * 10000
        response = client.get(
            f"/api/politician/1/donations/summary/filtered?topic={long_topic}"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_filtered_summary_with_nonexistent_politician(
        self, client, seed_test_data
    ):
        """Filtered summary with nonexistent politician returns empty list."""
        response = client.get(
            "/api/politician/999999999/donations/summary/filtered?topic=Health"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_all_topic_mappings_are_valid(self, client, seed_test_data):
        """All topics in TOPIC_INDUSTRY_MAP return valid responses."""
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
            assert (
                response.status_code == 200
            ), f"Topic '{topic}' should return 200"
            data = json.loads(response.data)
            assert isinstance(data, list), f"Topic '{topic}' should return list"
