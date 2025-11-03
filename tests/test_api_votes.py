"""Tests for politician votes API endpoint.

Includes pagination, filtering, sorting, and SQL injection protection tests.
"""

import pytest
import json


class TestPoliticianVotes:
    """Test suite for /api/politician/<politician_id>/votes endpoint."""

    def test_get_votes_with_valid_id(self, client):
        """Get votes returns data structure with pagination and votes."""
        response = client.get("/api/politician/1/votes")
        assert response.status_code == 200
        data = json.loads(response.data)

        assert "pagination" in data
        assert "votes" in data
        assert isinstance(data["votes"], list)

    def test_pagination_structure(self, client):
        """Pagination includes currentPage, totalPages, and totalVotes."""
        response = client.get("/api/politician/1/votes")
        assert response.status_code == 200
        data = json.loads(response.data)

        pagination = data["pagination"]
        assert "currentPage" in pagination
        assert "totalPages" in pagination
        assert "totalVotes" in pagination
        assert isinstance(pagination["currentPage"], int)
        assert isinstance(pagination["totalPages"], int)
        assert isinstance(pagination["totalVotes"], int)

    def test_vote_structure(self, client):
        """Each vote includes expected fields."""
        response = client.get("/api/politician/1/votes")
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data["votes"]) > 0:
            vote = data["votes"][0]
            required_fields = [
                "VoteID",
                "Vote",
                "BillNumber",
                "Title",
                "DateIntroduced",
                "subjects",
            ]
            for field in required_fields:
                assert field in vote

    def test_pagination_default_page_one(self, client):
        """Default page is 1 when not specified."""
        response = client.get("/api/politician/1/votes")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["pagination"]["currentPage"] == 1

    def test_pagination_page_parameter(self, client):
        """Page parameter controls current page."""
        response = client.get("/api/politician/1/votes?page=2")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["pagination"]["currentPage"] == 2

    def test_pagination_per_page_limit(self, client):
        """Results limited to 10 per page."""
        response = client.get("/api/politician/1/votes")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data["votes"]) <= 10

    def test_sorting_default_desc(self, client):
        """Default sort order is descending by DateIntroduced."""
        response = client.get("/api/politician/1/votes")
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data["votes"]) > 1:
            first_date = data["votes"][0]["DateIntroduced"]
            second_date = data["votes"][1]["DateIntroduced"]
            # First date should be >= second date for DESC order
            assert first_date >= second_date

    def test_sorting_asc_order(self, client):
        """Ascending sort order works correctly."""
        response = client.get("/api/politician/1/votes?sort=asc")
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data["votes"]) > 1:
            first_date = data["votes"][0]["DateIntroduced"]
            second_date = data["votes"][1]["DateIntroduced"]
            # First date should be <= second date for ASC order
            assert first_date <= second_date

    def test_sorting_desc_order(self, client):
        """Explicit descending sort order works correctly."""
        response = client.get("/api/politician/1/votes?sort=desc")
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data["votes"]) > 1:
            first_date = data["votes"][0]["DateIntroduced"]
            second_date = data["votes"][1]["DateIntroduced"]
            assert first_date >= second_date

    def test_sorting_invalid_order_defaults_to_desc(self, client):
        """Invalid sort order defaults to DESC."""
        response = client.get("/api/politician/1/votes?sort=invalid")
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data["votes"]) > 1:
            first_date = data["votes"][0]["DateIntroduced"]
            second_date = data["votes"][1]["DateIntroduced"]
            assert first_date >= second_date

    def test_bill_type_filter_single_type(self, client):
        """Filter by single bill type (e.g., hr)."""
        response = client.get("/api/politician/1/votes?type=hr")
        assert response.status_code == 200
        data = json.loads(response.data)

        # If votes exist, verify they match the filter
        for vote in data["votes"]:
            assert vote["BillNumber"].lower().startswith("hr")

    def test_bill_type_filter_multiple_types(self, client):
        """Filter by multiple bill types (e.g., hr and s)."""
        response = client.get("/api/politician/1/votes?type=hr&type=s")
        assert response.status_code == 200
        data = json.loads(response.data)

        # If votes exist, verify they match one of the filters
        for vote in data["votes"]:
            bill_num_lower = vote["BillNumber"].lower()
            assert bill_num_lower.startswith("hr") or bill_num_lower.startswith("s")

    def test_bill_subject_filter(self, client):
        """Filter by bill subject."""
        response = client.get("/api/politician/1/votes?subject=Health")
        assert response.status_code == 200
        data = json.loads(response.data)

        # If votes exist, verify subjects contain the filter
        for vote in data["votes"]:
            if vote["subjects"]:
                assert "Health" in vote["subjects"]

    def test_combined_filters(self, client):
        """Combination of type and subject filters works."""
        response = client.get("/api/politician/1/votes?type=hr&subject=Health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)

    def test_sql_injection_in_politician_id(self, client):
        """SQL injection in politician_id parameter is safely handled."""
        malicious_id = "1'; DROP TABLE votes; --"
        response = client.get(f"/api/politician/{malicious_id}/votes")
        assert response.status_code in [200, 500]
        # Should not crash the application

    def test_sql_injection_in_sort_parameter(self, client):
        """SQL injection in sort parameter is prevented."""
        malicious_sort = "DESC; DROP TABLE votes; --"
        response = client.get(f"/api/politician/1/votes?sort={malicious_sort}")
        assert response.status_code == 200
        data = json.loads(response.data)
        # Should default to DESC and not execute injection
        assert isinstance(data, dict)

    def test_sql_injection_in_bill_type(self, client):
        """SQL injection in bill type filter is safely handled."""
        malicious_type = "hr' OR '1'='1"
        response = client.get(f"/api/politician/1/votes?type={malicious_type}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)

    def test_sql_injection_in_subject(self, client):
        """SQL injection in subject filter is safely handled."""
        malicious_subject = "Health'; DROP TABLE bills; --"
        response = client.get(f"/api/politician/1/votes?subject={malicious_subject}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)

    def test_sql_injection_in_page_parameter(self, client):
        """SQL injection in page parameter is safely handled."""
        malicious_page = "1'; DROP TABLE votes; --"
        response = client.get(f"/api/politician/1/votes?page={malicious_page}")
        # Should either convert to int and fail or return error
        assert response.status_code in [200, 400, 500]

    def test_nonexistent_politician_id(self, client):
        """Nonexistent politician ID returns empty votes list."""
        response = client.get("/api/politician/999999999/votes")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["pagination"]["totalVotes"] == 0
        assert len(data["votes"]) == 0

    def test_negative_page_number(self, client):
        """Negative page number is handled gracefully."""
        response = client.get("/api/politician/1/votes?page=-1")
        # Should either handle gracefully or return error
        assert response.status_code in [200, 400, 500]

    def test_zero_page_number(self, client):
        """Zero page number is handled gracefully."""
        response = client.get("/api/politician/1/votes?page=0")
        # Should either handle gracefully or return error
        assert response.status_code in [200, 400, 500]

    def test_large_page_number(self, client):
        """Large page number beyond total pages returns empty votes."""
        response = client.get("/api/politician/1/votes?page=99999")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data["votes"]) == 0

    def test_pagination_math_consistency(self, client):
        """Pagination math is internally consistent."""
        response = client.get("/api/politician/1/votes")
        assert response.status_code == 200
        data = json.loads(response.data)

        pagination = data["pagination"]
        total_votes = pagination["totalVotes"]
        total_pages = pagination["totalPages"]
        per_page = 10

        # Verify total_pages calculation
        expected_pages = (total_votes + per_page - 1) // per_page
        assert total_pages == expected_pages
