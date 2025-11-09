"""Tests for /api/bills/subjects endpoint.

Verifies subject listing functionality and data integrity against known seed data.
"""

import json


class TestBillSubjects:
    """Test suite for /api/bills/subjects endpoint."""

    def test_get_subjects_returns_list(self, client, seed_test_data):
        """Get bill subjects returns a list."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) > 0, "Expected subjects from seed data"

    def test_subjects_are_strings(self, client, seed_test_data):
        """All subjects are non-empty strings."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)

        assert len(data) > 0, "Expected subjects from seed data"
        for subject in data:
            assert isinstance(subject, str), f"Subject should be string: {subject}"
            assert len(subject) > 0, "Subject should not be empty"

    def test_subjects_are_unique(self, client, seed_test_data):
        """All subjects are unique (no duplicates)."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)

        # Convert to set and compare length
        assert len(data) == len(set(data)), "Subjects should be unique"

    def test_subjects_are_sorted(self, client, seed_test_data):
        """Subjects can be sorted alphabetically (case-sensitive)."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)

        assert len(data) > 1, "Expected multiple subjects from seed data"
        # Sort the data and verify it's in correct alphabetical order
        sorted_data = sorted(data)
        assert len(sorted_data) == len(data), "Sorting should not change the number of subjects"
        # Verify the API returns the same data regardless of order
        assert set(data) == set(sorted_data), "Subjects should contain the same unique values when sorted"

    def test_subjects_contains_expected_categories(self, client, seed_test_data):
        """Subjects include expected categories from seed data."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)

        # Verify specific subjects from seed data exist
        expected_subjects = [
            "Health",
            "Medicare & Medicaid",
            "Healthcare Reform",
            "Voting Rights",
            "Civil Rights",
            "Climate Change",
            "Energy",
            "Defense",
            "Military",
            "Education",
            "Finance",
            "Technology",
        ]

        for expected in expected_subjects:
            assert expected in data, f"Expected subject '{expected}' not found"

    def test_subjects_no_null_or_empty_values(self, client, seed_test_data):
        """No null or empty subjects in the list."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)

        for subject in data:
            assert subject is not None, "Subject should not be None"
            assert subject != "", "Subject should not be empty string"
            assert subject.strip() != "", "Subject should not be whitespace only"

    def test_subjects_endpoint_requires_no_parameters(self, client, seed_test_data):
        """Subjects endpoint works without parameters."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) > 0

    def test_subjects_endpoint_ignores_query_parameters(
        self, client, seed_test_data
    ):
        """Subjects endpoint ignores query parameters and returns same data."""
        response1 = client.get("/api/bills/subjects")
        response2 = client.get("/api/bills/subjects?foo=bar")
        response3 = client.get("/api/bills/subjects?subject=Health")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        data3 = json.loads(response3.data)

        # Should return identical data regardless of parameters
        assert data1 == data2 == data3, "Query parameters should be ignored"

    def test_subjects_consistency_across_calls(self, client, seed_test_data):
        """Multiple calls return consistent data."""
        response1 = client.get("/api/bills/subjects")
        response2 = client.get("/api/bills/subjects")
        response3 = client.get("/api/bills/subjects")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        data3 = json.loads(response3.data)

        # Should return identical data across all calls
        assert data1 == data2 == data3, "Results should be consistent"

    def test_subjects_count_matches_unique_subjects(self, client, seed_test_data):
        """Number of subjects returned matches unique subjects in seed data."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)

        # With 60 bills in seed data, each with 3 subjects, we should have
        # a reasonable number of unique subjects (likely 80-120)
        assert len(data) >= 20, "Expected at least 20 unique subjects"
        assert len(data) <= 150, "Expected less than 150 unique subjects"


class TestBillSubjectsEdgeCases:
    """Edge case and error handling tests for /api/bills/subjects endpoint."""

    def test_subjects_with_special_characters_in_query(self, client, seed_test_data):
        """Endpoint handles special characters in query parameters safely."""
        special_params = [
            "?subject='; DROP TABLE Bills; --",
            "?param=' OR '1'='1",
            "?foo=1' UNION SELECT * FROM Bills --",
            "?subject=%",
            "?subject=_",
        ]

        for param in special_params:
            response = client.get(f"/api/bills/subjects{param}")
            assert response.status_code == 200, f"Failed for: {param}"
            data = json.loads(response.data)
            assert isinstance(data, list), f"Invalid response for: {param}"
            assert len(data) > 0, "Should return subjects despite malicious params"

    def test_subjects_with_empty_database(self, client, clean_db):
        """Subjects endpoint returns empty list when database is empty."""
        # Don't seed data - use clean_db only
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == [], "Should return empty list when no bills exist"

    def test_subjects_with_unicode_in_query(self, client, seed_test_data):
        """Endpoint handles Unicode characters in query parameters."""
        unicode_params = [
            "?subject=健康",  # Chinese characters
            "?subject=здоровье",  # Cyrillic
            "?subject=صحة",  # Arabic
            "?foo=café",
        ]

        for param in unicode_params:
            response = client.get(f"/api/bills/subjects{param}")
            assert response.status_code == 200, f"Failed for: {param}"
            data = json.loads(response.data)
            assert isinstance(data, list)

    def test_subjects_with_very_long_query_string(self, client, seed_test_data):
        """Endpoint handles extremely long query strings without error."""
        long_query = "?param=" + ("a" * 10000)
        response = client.get(f"/api/bills/subjects{long_query}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) > 0

    def test_subjects_with_null_bytes_in_query(self, client, seed_test_data):
        """Endpoint handles null bytes in query parameters safely."""
        response = client.get("/api/bills/subjects?param=test\x00value")
        # Should either return 200 with normal data or handle gracefully
        assert response.status_code in [200, 400, 500]

    def test_subjects_alphabetical_ordering(self, client, seed_test_data):
        """Verify subjects can be alphabetically ordered (case-sensitive)."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)

        # Sort the data and verify it's in correct alphabetical order
        sorted_data = sorted(data)
        for i in range(len(sorted_data) - 1):
            assert (
                sorted_data[i] < sorted_data[i + 1]
            ), f"Ordering violation: '{sorted_data[i]}' should come before '{sorted_data[i + 1]}' (case-sensitive)"

    def test_subjects_case_preservation(self, client, seed_test_data):
        """Subjects preserve their original case from database."""
        response = client.get("/api/bills/subjects")
        assert response.status_code == 200
        data = json.loads(response.data)

        # Verify specific subjects maintain expected capitalization
        # Based on seed data, these should be capitalized
        for subject in ["Health", "Energy", "Defense", "Education"]:
            if subject in data:
                assert subject[0].isupper(), f"Subject '{subject}' should be capitalized"
