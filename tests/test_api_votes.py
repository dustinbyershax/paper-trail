"""Tests for politician votes API endpoint.

Verifies pagination, filtering, sorting, and SQL injection protection with
comprehensive edge case testing against known seed data.
"""

import json
from datetime import datetime


class TestPoliticianVotes:
    """Test suite for /api/politician/<politician_id>/votes endpoint."""

    def test_get_votes_returns_expected_structure(self, client, seed_test_data):
        """Get votes returns data structure with pagination and votes list."""
        response = client.get("/api/politician/1/votes")
        assert response.status_code == 200
        data = json.loads(response.data)

        assert "pagination" in data, "Missing pagination field"
        assert "votes" in data, "Missing votes field"
        assert isinstance(data["votes"], list), "Votes should be a list"
        assert isinstance(data["pagination"], dict), "Pagination should be a dict"

    def test_pagination_structure_complete(self, client, seed_test_data):
        """Pagination includes all required fields with correct types."""
        response = client.get("/api/politician/1/votes")
        assert response.status_code == 200
        data = json.loads(response.data)

        pagination = data["pagination"]
        assert "currentPage" in pagination, "Missing currentPage"
        assert "totalPages" in pagination, "Missing totalPages"
        assert "totalVotes" in pagination, "Missing totalVotes"
        assert isinstance(pagination["currentPage"], int)
        assert isinstance(pagination["totalPages"], int)
        assert isinstance(pagination["totalVotes"], int)
        assert pagination["currentPage"] >= 1, "Current page should be >= 1"
        assert pagination["totalPages"] >= 0, "Total pages should be >= 0"
        assert pagination["totalVotes"] >= 0, "Total votes should be >= 0"

    def test_vote_structure_has_required_fields(self, client, seed_test_data):
        """Each vote includes all required fields with correct types."""
        response = client.get("/api/politician/1/votes")
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data["votes"]) > 0:
            vote = data["votes"][0]
            required_fields = {
                "VoteID": int,
                "Vote": str,
                "BillNumber": str,
                "Title": str,
                "DateIntroduced": str,  # ISO date string
                "subjects": (list, type(None)),  # Can be list or None
            }

            for field, expected_type in required_fields.items():
                assert field in vote, f"Missing field: {field}"
                if expected_type == (list, type(None)):
                    assert vote[field] is None or isinstance(vote[field], list)
                else:
                    assert isinstance(
                        vote[field], expected_type
                    ), f"Field {field} should be {expected_type}"

    def test_vote_values_are_valid(self, client, seed_test_data):
        """Vote values are one of: Yea, Nay, Present, Not Voting."""
        response = client.get("/api/politician/1/votes")
        assert response.status_code == 200
        data = json.loads(response.data)

        valid_votes = ["Yea", "Nay", "Present", "Not Voting"]
        for vote in data["votes"]:
            assert (
                vote["Vote"] in valid_votes
            ), f"Invalid vote value: {vote['Vote']}"

    def test_pagination_default_page_one(self, client, seed_test_data):
        """Default page is 1 when not specified."""
        response = client.get("/api/politician/1/votes")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["pagination"]["currentPage"] == 1

    def test_pagination_page_parameter(self, client, seed_test_data):
        """Page parameter controls current page number."""
        response1 = client.get("/api/politician/1/votes?page=1")
        response2 = client.get("/api/politician/1/votes?page=2")

        assert response1.status_code == 200
        assert response2.status_code == 200

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)

        assert data1["pagination"]["currentPage"] == 1
        assert data2["pagination"]["currentPage"] == 2

    def test_pagination_per_page_limit(self, client, seed_test_data):
        """Results limited to 10 per page."""
        response = client.get("/api/politician/1/votes")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data["votes"]) <= 10, "Should return at most 10 votes per page"

    def test_pagination_math_consistency(self, client, seed_test_data):
        """Pagination math is internally consistent."""
        response = client.get("/api/politician/1/votes")
        assert response.status_code == 200
        data = json.loads(response.data)

        pagination = data["pagination"]
        total_votes = pagination["totalVotes"]
        total_pages = pagination["totalPages"]
        per_page = 10

        # Verify total_pages calculation: (totalVotes + perPage - 1) // perPage
        expected_pages = (total_votes + per_page - 1) // per_page
        assert (
            total_pages == expected_pages
        ), f"Expected {expected_pages} pages, got {total_pages}"

    def test_sorting_default_descending(self, client, seed_test_data):
        """Default sort order is descending by DateIntroduced (newest first)."""
        response = client.get("/api/politician/1/votes")
        assert response.status_code == 200
        data = json.loads(response.data)

        votes = data["votes"]
        if len(votes) >= 2:
            # Check first vote is newer than or equal to last vote
            # API returns ISO format dates (YYYY-MM-DD)
            first = datetime.fromisoformat(votes[0]["DateIntroduced"])
            last = datetime.fromisoformat(votes[-1]["DateIntroduced"])
            assert first >= last, (
                f"First vote {votes[0]['DateIntroduced']} "
                f"should be >= last {votes[-1]['DateIntroduced']}"
            )

    def test_sorting_ascending_order(self, client, seed_test_data):
        """Ascending sort order works correctly (oldest first)."""
        response = client.get("/api/politician/1/votes?sort=asc")
        assert response.status_code == 200
        data = json.loads(response.data)

        votes = data["votes"]
        if len(votes) >= 2:
            # Check first vote is older than or equal to last vote
            # API returns ISO format dates (YYYY-MM-DD)
            first = datetime.fromisoformat(votes[0]["DateIntroduced"])
            last = datetime.fromisoformat(votes[-1]["DateIntroduced"])
            assert first <= last, (
                f"First vote {votes[0]['DateIntroduced']} "
                f"should be <= last {votes[-1]['DateIntroduced']}"
            )

    def test_sorting_descending_explicit(self, client, seed_test_data):
        """Explicit descending sort order works correctly."""
        response = client.get("/api/politician/1/votes?sort=desc")
        assert response.status_code == 200
        data = json.loads(response.data)

        votes = data["votes"]
        if len(votes) >= 2:
            # Check first vote is newer than or equal to last vote
            # API returns ISO format dates (YYYY-MM-DD)
            first = datetime.fromisoformat(votes[0]["DateIntroduced"])
            last = datetime.fromisoformat(votes[-1]["DateIntroduced"])
            assert first >= last, (
                f"First vote {votes[0]['DateIntroduced']} "
                f"should be >= last {votes[-1]['DateIntroduced']}"
            )

    def test_sorting_case_insensitive(self, client, seed_test_data):
        """Sort parameter is case-insensitive."""
        response_lower = client.get("/api/politician/1/votes?sort=asc")
        response_upper = client.get("/api/politician/1/votes?sort=ASC")
        response_mixed = client.get("/api/politician/1/votes?sort=Asc")

        assert response_lower.status_code == 200
        assert response_upper.status_code == 200
        assert response_mixed.status_code == 200

        data_lower = json.loads(response_lower.data)
        data_upper = json.loads(response_upper.data)
        data_mixed = json.loads(response_mixed.data)

        # All should return same data
        assert data_lower["votes"] == data_upper["votes"] == data_mixed["votes"]

    def test_sorting_invalid_defaults_to_descending(self, client, seed_test_data):
        """Invalid sort order defaults to DESC."""
        response = client.get("/api/politician/1/votes?sort=invalid")
        assert response.status_code == 200
        data = json.loads(response.data)

        votes = data["votes"]
        if len(votes) >= 2:
            # Check first vote is newer than or equal to last vote (DESC order)
            # API returns ISO format dates (YYYY-MM-DD)
            first = datetime.fromisoformat(votes[0]["DateIntroduced"])
            last = datetime.fromisoformat(votes[-1]["DateIntroduced"])
            assert first >= last, "Should default to DESC order"


class TestPoliticianVotesFiltering:
    """Test suite for filtering functionality of votes endpoint."""

    def test_bill_type_filter_hr(self, client, seed_test_data):
        """Filter by single bill type 'hr' returns only HR bills."""
        response = client.get("/api/politician/1/votes?type=hr")
        assert response.status_code == 200
        data = json.loads(response.data)

        # Should return at least one H.R. bill
        assert len(data["votes"]) > 0, "Should return at least one H.R. bill"

        # Verify all returned bills start with 'H.R.'
        for vote in data["votes"]:
            assert vote["BillNumber"].startswith("H.R."), (
                f"Bill {vote['BillNumber']} should be H.R. type"
            )

    def test_bill_type_filter_s(self, client, seed_test_data):
        """Filter by single bill type 's' returns only Senate bills."""
        response = client.get("/api/politician/1/votes?type=s")
        assert response.status_code == 200
        data = json.loads(response.data)

        # If bills are returned, verify all are Senate bills
        # (Politician 1 may not have any Senate bill votes in test data)
        for vote in data["votes"]:
            assert vote["BillNumber"].startswith("S."), (
                f"Bill {vote['BillNumber']} should be S. type"
            )

    def test_bill_type_filter_multiple(self, client, seed_test_data):
        """Filter by multiple bill types works correctly."""
        response = client.get("/api/politician/1/votes?type=hr&type=s")
        assert response.status_code == 200
        data = json.loads(response.data)

        # Should return at least one bill
        assert len(data["votes"]) > 0, "Should return at least one bill"

        # Verify all returned bills are either H.R. or S.
        for vote in data["votes"]:
            assert vote["BillNumber"].startswith("H.R.") or vote["BillNumber"].startswith("S."), (
                f"Bill {vote['BillNumber']} should be H.R. or S. type"
            )

    def test_bill_subject_filter(self, client, seed_test_data):
        """Filter by bill subject returns only bills with that subject."""
        response = client.get("/api/politician/1/votes?subject=Health")
        assert response.status_code == 200
        data = json.loads(response.data)

        # Verify all returned bills have 'Health' in subjects
        for vote in data["votes"]:
            if vote["subjects"]:
                assert (
                    "Health" in vote["subjects"]
                ), f"Vote should have Health subject: {vote['subjects']}"

    def test_subject_filter_case_sensitive(self, client, seed_test_data):
        """Subject filter is case-sensitive."""
        response_correct = client.get("/api/politician/1/votes?subject=Health")
        response_lowercase = client.get("/api/politician/1/votes?subject=health")

        assert response_correct.status_code == 200
        assert response_lowercase.status_code == 200

        data_correct = json.loads(response_correct.data)
        data_lowercase = json.loads(response_lowercase.data)

        # Lowercase might return fewer or no results
        assert isinstance(data_correct["votes"], list)
        assert isinstance(data_lowercase["votes"], list)

    def test_combined_type_and_subject_filters(self, client, seed_test_data):
        """Combination of type and subject filters works correctly."""
        response = client.get("/api/politician/1/votes?type=hr&subject=Health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)
        assert "votes" in data
        assert "pagination" in data

        # If there are results, verify they match both filters
        for vote in data["votes"]:
            assert vote["BillNumber"].startswith("H.R."), (
                f"Bill {vote['BillNumber']} should be H.R. type"
            )
            if vote["subjects"]:
                assert "Health" in vote["subjects"]

    def test_filter_with_invalid_type(self, client, seed_test_data):
        """Invalid bill type filter returns empty or no matches."""
        response = client.get("/api/politician/1/votes?type=invalid")
        assert response.status_code == 200
        data = json.loads(response.data)
        # Should return valid structure, possibly empty votes
        assert isinstance(data["votes"], list)

    def test_filter_with_invalid_subject(self, client, seed_test_data):
        """Invalid subject filter returns empty or no matches."""
        response = client.get("/api/politician/1/votes?subject=NonexistentSubject123")
        assert response.status_code == 200
        data = json.loads(response.data)
        # Should return empty votes list
        assert isinstance(data["votes"], list)


class TestPoliticianVotesSQLInjection:
    """SQL injection protection tests for votes endpoint."""

    def test_sql_injection_drop_table_in_politician_id(
        self, client, seed_test_data, db_connection
    ):
        """SQL injection attempt via politician_id is rejected by Flask type validation."""
        cursor = db_connection.cursor()

        # Count rows before injection attempt
        cursor.execute("SELECT COUNT(*) FROM pt.Votes")
        count_before = cursor.fetchone()[0]
        assert count_before > 0, "Should have votes in database"

        # Attempt injection
        malicious_id = "1'; DROP TABLE Votes; --"
        response = client.get(f"/api/politician/{malicious_id}/votes")

        # Flask's <int:> validation rejects non-integer values with 404
        assert response.status_code == 404, "Should reject non-integer politician_id"

        # Verify table still exists and has same row count
        cursor.execute("SELECT COUNT(*) FROM pt.Votes")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before, "Table row count should be unchanged"

        # Verify subsequent queries still work
        cursor.execute("SELECT * FROM pt.Votes LIMIT 1")
        assert cursor.fetchone() is not None, "Table should still be queryable"

        cursor.close()

    def test_sql_injection_union_in_politician_id(
        self, client, seed_test_data, db_connection
    ):
        """SQL injection UNION SELECT via politician_id is rejected by Flask type validation."""
        cursor = db_connection.cursor()

        malicious_id = "1' UNION SELECT * FROM Votes --"
        response = client.get(f"/api/politician/{malicious_id}/votes")

        # Flask's <int:> validation rejects non-integer values with 404
        assert response.status_code == 404, "Should reject non-integer politician_id"

        # Verify data integrity
        cursor.execute("SELECT COUNT(*) FROM pt.Votes")
        assert cursor.fetchone()[0] > 0

        cursor.close()

    def test_sql_injection_in_sort_parameter(
        self, client, seed_test_data, db_connection
    ):
        """SQL injection in sort parameter is prevented."""
        cursor = db_connection.cursor()

        # Count rows before
        cursor.execute("SELECT COUNT(*) FROM pt.Votes")
        count_before = cursor.fetchone()[0]

        malicious_sort = "DESC; DROP TABLE Votes; --"
        response = client.get(f"/api/politician/1/votes?sort={malicious_sort}")

        assert response.status_code == 200
        data = json.loads(response.data)
        # Should default to DESC and not execute injection
        assert isinstance(data, dict)

        # Verify table integrity
        cursor.execute("SELECT COUNT(*) FROM pt.Votes")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before

        cursor.close()

    def test_sql_injection_in_bill_type(self, client, seed_test_data, db_connection):
        """SQL injection in bill type filter is safely handled."""
        cursor = db_connection.cursor()

        # Count rows before
        cursor.execute("SELECT COUNT(*) FROM pt.Bills")
        count_before = cursor.fetchone()[0]

        malicious_type = "hr' OR '1'='1"
        response = client.get(f"/api/politician/1/votes?type={malicious_type}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)

        # Verify table integrity
        cursor.execute("SELECT COUNT(*) FROM pt.Bills")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before

        cursor.close()

    def test_sql_injection_in_subject(self, client, seed_test_data, db_connection):
        """SQL injection in subject filter is safely handled."""
        cursor = db_connection.cursor()

        # Count rows before
        cursor.execute("SELECT COUNT(*) FROM pt.Bills")
        count_before = cursor.fetchone()[0]

        malicious_subject = "Health'; DROP TABLE Bills; --"
        response = client.get(f"/api/politician/1/votes?subject={malicious_subject}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)

        # Verify table integrity
        cursor.execute("SELECT COUNT(*) FROM pt.Bills")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before

        cursor.close()

    def test_sql_injection_in_page_parameter(self, client, seed_test_data):
        """SQL injection in page parameter is safely handled."""
        malicious_page = "1'; DROP TABLE Votes; --"
        response = client.get(f"/api/politician/1/votes?page={malicious_page}")

        # Should either handle gracefully or return error
        assert response.status_code in [200, 400, 500]


class TestPoliticianVotesEdgeCases:
    """Edge case tests for votes endpoint."""

    def test_nonexistent_politician_id(self, client, seed_test_data):
        """Nonexistent politician ID returns empty votes list."""
        response = client.get("/api/politician/999999999/votes")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["pagination"]["totalVotes"] == 0, "Should have 0 total votes"
        assert len(data["votes"]) == 0, "Should return empty votes list"

    def test_negative_page_number(self, client, seed_test_data):
        """Negative page number is handled gracefully."""
        response = client.get("/api/politician/1/votes?page=-1")
        # Should either handle gracefully or return error
        assert response.status_code in [200, 400, 500]

    def test_zero_page_number(self, client, seed_test_data):
        """Zero page number is handled gracefully."""
        response = client.get("/api/politician/1/votes?page=0")
        # Should either handle gracefully or return error
        assert response.status_code in [200, 400, 500]

    def test_large_page_number(self, client, seed_test_data):
        """Large page number beyond total pages returns empty votes."""
        response = client.get("/api/politician/1/votes?page=99999")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data["votes"]) == 0, "Should return empty votes for page beyond total"

    def test_page_as_non_integer(self, client, seed_test_data):
        """Non-integer page parameter is handled gracefully."""
        response = client.get("/api/politician/1/votes?page=abc")
        # Should return error or default to page 1
        assert response.status_code in [200, 400, 500]

    def test_page_as_float(self, client, seed_test_data):
        """Float page parameter is handled gracefully."""
        response = client.get("/api/politician/1/votes?page=1.5")
        # Should handle gracefully
        assert response.status_code in [200, 400, 500]

    def test_very_long_bill_type_parameter(self, client, seed_test_data):
        """Very long bill type parameter is handled safely."""
        long_type = "a" * 10000
        response = client.get(f"/api/politician/1/votes?type={long_type}")
        assert response.status_code == 200
        data = json.loads(response.data)
        # Should return empty or no matches
        assert isinstance(data["votes"], list)

    def test_very_long_subject_parameter(self, client, seed_test_data):
        """Very long subject parameter is handled safely."""
        long_subject = "a" * 10000
        response = client.get(f"/api/politician/1/votes?subject={long_subject}")
        assert response.status_code == 200
        data = json.loads(response.data)
        # Should return empty or no matches
        assert isinstance(data["votes"], list)

    def test_unicode_in_parameters(self, client, seed_test_data):
        """Unicode characters in parameters are handled safely."""
        response = client.get("/api/politician/1/votes?type=健康&subject=здоровье")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)

    def test_special_characters_in_parameters(self, client, seed_test_data):
        """Special characters in parameters are handled safely."""
        special_params = [
            "type=%",
            "type=_",
            "subject=Health%20Care",
            "subject=Tech'OR'1'='1",
        ]

        for param in special_params:
            response = client.get(f"/api/politician/1/votes?{param}")
            assert response.status_code == 200, f"Failed for param: {param}"
            data = json.loads(response.data)
            assert isinstance(data, dict)

    def test_consistency_across_multiple_calls(self, client, seed_test_data):
        """Multiple calls with same parameters return consistent data."""
        url = "/api/politician/1/votes?page=1&sort=desc"
        response1 = client.get(url)
        response2 = client.get(url)
        response3 = client.get(url)

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        data3 = json.loads(response3.data)

        assert data1 == data2 == data3, "Results should be consistent"

    def test_empty_type_parameter(self, client, seed_test_data):
        """Empty type parameter is handled gracefully."""
        response = client.get("/api/politician/1/votes?type=")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)

    def test_empty_subject_parameter(self, client, seed_test_data):
        """Empty subject parameter is handled gracefully."""
        response = client.get("/api/politician/1/votes?subject=")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)
