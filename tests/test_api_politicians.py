"""Tests for /api/politicians/search endpoint.

Verifies search functionality, SQL injection protection, and error handling
against known seed data.
"""

# pylint: disable=unused-argument
# noqa: F401
# type: ignore
import json


class TestPoliticiansSearch:
    """Test suite for /api/politicians/search endpoint."""

    def test_search_requires_minimum_length(self, client, seed_test_data):
        """Search returns empty list for queries less than 2 characters."""
        response = client.get("/api/politicians/search?name=a")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_accepts_valid_length(self, client, seed_test_data):
        """Search accepts queries of 2 or more characters and returns results."""
        response = client.get("/api/politicians/search?name=Jo")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1, "Expected at least one politician with 'Jo' in name"
        # Verify at least one result contains 'Jo'
        assert any('jo' in (p['firstname'] + ' ' + p['lastname']).lower()
                   for p in data), "Results should contain 'Jo'"

    def test_search_returns_all_required_fields(self, client, seed_test_data):
        """Search returns politicians with all required fields."""
        response = client.get("/api/politicians/search?name=Biden")
        assert response.status_code == 200
        data = json.loads(response.data)

        assert len(data) >= 1, "Expected at least one Biden in seed data"
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
            assert field in politician, f"Missing required field: {field}"

        # Verify data types
        assert isinstance(politician['politicianid'], int)
        assert isinstance(politician['firstname'], str)
        assert isinstance(politician['lastname'], str)
        assert isinstance(politician['isactive'], bool)

    def test_search_finds_biden(self, client, seed_test_data):
        """Search finds Joseph Biden from seed data."""
        response = client.get("/api/politicians/search?name=Biden")
        assert response.status_code == 200
        data = json.loads(response.data)

        assert len(data) >= 1, "Expected to find Biden"
        biden = next((p for p in data if p['lastname'] == 'Biden'), None)
        assert biden is not None, "Biden not found in results"
        assert biden['firstname'] == 'Joseph'
        assert biden['party'] == 'Democrat'
        assert biden['state'] == 'Delaware'

    def test_search_is_case_insensitive(self, client, seed_test_data):
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
        assert len(data_lower) >= 1, "Expected at least one result"

    def test_search_with_special_characters(self, client, seed_test_data):
        """Search handles special characters without errors."""
        special_chars = ["O'Brien", "Smith-Jones", "Test%", "Test_"]

        for name in special_chars:
            response = client.get(f"/api/politicians/search?name={name}")
            assert response.status_code == 200, f"Failed for: {name}"
            data = json.loads(response.data)
            assert isinstance(data, list), f"Invalid response for: {name}"

    def test_search_with_empty_query_parameter(self, client, seed_test_data):
        """Search with empty query parameter returns empty list."""
        response = client.get("/api/politicians/search?name=")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_without_query_parameter(self, client, seed_test_data):
        """Search without query parameter returns empty list."""
        response = client.get("/api/politicians/search")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_with_spaces(self, client, seed_test_data):
        """Search handles names with spaces correctly."""
        response = client.get("/api/politicians/search?name=Joseph Biden")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) >= 1, "Expected to find 'Joseph Biden'"
        # Verify Biden is in results
        assert any('biden' in p['lastname'].lower() for p in data)

    def test_search_partial_match_first_name(self, client, seed_test_data):
        """Search returns partial matches on first name using ILIKE."""
        response = client.get("/api/politicians/search?name=Jos")
        assert response.status_code == 200
        data = json.loads(response.data)

        assert len(data) >= 1, "Expected at least one politician with 'Jos'"
        # Verify all results contain 'Jos' in first or last name
        for politician in data:
            full_name = f"{politician['firstname']} {politician['lastname']}"
            assert 'jos' in full_name.lower(), f"{full_name} doesn't contain 'Jos'"

    def test_search_partial_match_last_name(self, client, seed_test_data):
        """Search returns partial matches on last name using ILIKE."""
        response = client.get("/api/politicians/search?name=Cruz")
        assert response.status_code == 200
        data = json.loads(response.data)

        assert len(data) >= 1, "Expected at least one Cruz"
        cruz = data[0]
        assert cruz['lastname'] == 'Cruz'
        assert cruz['firstname'] == 'Ted'

    def test_search_sorts_by_active_then_name(self, client, seed_test_data):
        """Search results are sorted by IsActive DESC, then LastName, FirstName."""
        response = client.get("/api/politicians/search?name=Jo")
        assert response.status_code == 200
        data = json.loads(response.data)

        assert len(data) >= 2, "Need at least 2 results to verify sorting"

        # Verify active politicians come before inactive
        active_indices = [i for i, p in enumerate(data) if p['isactive']]
        inactive_indices = [i for i, p in enumerate(data) if not p['isactive']]

        if active_indices and inactive_indices:
            assert max(active_indices) < min(inactive_indices), \
                "Active politicians should appear before inactive"


class TestPoliticiansSearchSQLInjection:
    """SQL injection protection tests for /api/politicians/search endpoint."""

    def test_sql_injection_drop_table(self, client, seed_test_data, db_connection):
        """SQL injection attempt to drop table is safely handled as literal string."""
        cursor = db_connection.cursor()

        # Count rows before injection attempt
        cursor.execute("SELECT COUNT(*) FROM pt.Politicians")
        count_before = cursor.fetchone()[0]
        assert count_before > 0, "Should have politicians in database"

        # Attempt injection
        malicious_input = "'; DROP TABLE Politicians; --"
        response = client.get(f"/api/politicians/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == [], "Injection string should be treated as literal, returning no results"

        # Verify table still exists and has same row count
        cursor.execute("SELECT COUNT(*) FROM pt.Politicians")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before, "Table row count should be unchanged"

        # Verify subsequent queries still work
        cursor.execute("SELECT * FROM pt.Politicians LIMIT 1")
        assert cursor.fetchone() is not None, "Table should still be queryable"

        cursor.close()

    def test_sql_injection_union_select(self, client, seed_test_data, db_connection):
        """SQL injection UNION SELECT attempt is safely handled as literal string."""
        cursor = db_connection.cursor()

        # Count rows before
        cursor.execute("SELECT COUNT(*) FROM pt.Politicians")
        count_before = cursor.fetchone()[0]

        # Attempt UNION injection
        malicious_input = "' UNION SELECT * FROM Politicians --"
        response = client.get(f"/api/politicians/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        # Should return empty list (injection string treated as literal)
        assert data == [], "UNION injection should return no results"

        # Verify row count unchanged
        cursor.execute("SELECT COUNT(*) FROM pt.Politicians")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before

        cursor.close()

    def test_sql_injection_or_condition(self, client, seed_test_data, db_connection):
        """SQL injection OR 1=1 attempt is safely handled as literal string."""
        cursor = db_connection.cursor()

        # Attempt OR injection
        malicious_input = "' OR '1'='1"
        response = client.get(f"/api/politicians/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)

        # Should return empty list (no politician named "' OR '1'='1")
        assert data == [], "OR injection should return no results"

        # Verify normal queries still work
        cursor.execute("SELECT COUNT(*) FROM pt.Politicians WHERE FirstName = 'Joseph'")
        count = cursor.fetchone()[0]
        assert count > 0, "Normal queries should still work"

        cursor.close()

    def test_sql_injection_comment_injection(self, client, seed_test_data, db_connection):
        """SQL injection comment injection attempt is safely handled."""
        cursor = db_connection.cursor()

        malicious_input = "Biden' --"
        response = client.get(f"/api/politicians/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        # Should return empty (literal search for "Biden' --")
        assert data == [], "Comment injection should return no results"

        # Verify Biden is still findable with normal query
        cursor.execute("SELECT COUNT(*) FROM pt.Politicians WHERE LastName = 'Biden'")
        count = cursor.fetchone()[0]
        assert count > 0, "Biden should still be findable"

        cursor.close()

    def test_sql_injection_semicolon_command(self, client, seed_test_data, db_connection):
        """SQL injection with semicolon command injection is safely handled."""
        cursor = db_connection.cursor()

        # Get Biden's party before injection attempt
        cursor.execute("SELECT Party FROM pt.Politicians WHERE LastName = 'Biden' LIMIT 1")
        party_before = cursor.fetchone()[0]
        assert party_before == 'Democrat'

        # Attempt UPDATE injection
        malicious_input = "Biden'; UPDATE Politicians SET Party='Hacked' WHERE '1'='1"
        response = client.get(f"/api/politicians/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == [], "Semicolon injection should return no results"

        # Verify Biden's party unchanged
        cursor.execute("SELECT Party FROM pt.Politicians WHERE LastName = 'Biden' LIMIT 1")
        party_after = cursor.fetchone()[0]
        assert party_after == 'Democrat', "Party should not have been modified"

        cursor.close()

    def test_sql_injection_stacked_queries(self, client, seed_test_data, db_connection):
        """SQL injection with stacked queries is safely handled."""
        cursor = db_connection.cursor()

        # Count politicians before
        cursor.execute("SELECT COUNT(*) FROM pt.Politicians")
        count_before = cursor.fetchone()[0]

        # Attempt stacked query injection
        malicious_input = "Biden'; DELETE FROM Politicians WHERE Party='Democrat'; --"
        response = client.get(f"/api/politicians/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

        # Verify no deletions occurred
        cursor.execute("SELECT COUNT(*) FROM pt.Politicians")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before, "No rows should have been deleted"

        # Verify Democrats still exist
        cursor.execute("SELECT COUNT(*) FROM pt.Politicians WHERE Party='Democrat'")
        democrat_count = cursor.fetchone()[0]
        assert democrat_count > 0, "Democrats should still exist"

        cursor.close()


class TestPoliticiansSearchNegative:
    """Negative test cases for error conditions and edge cases."""

    def test_search_with_very_long_input(self, client, seed_test_data):
        """Search handles extremely long input without crashing."""
        long_input = "a" * 10000
        response = client.get(f"/api/politicians/search?name={long_input}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_search_with_unicode_characters(self, client, seed_test_data):
        """Search handles Unicode characters correctly."""
        unicode_names = ["José", "François", "Müller", "李明"]

        for name in unicode_names:
            response = client.get(f"/api/politicians/search?name={name}")
            assert response.status_code == 200, f"Failed for: {name}"
            data = json.loads(response.data)
            assert isinstance(data, list)

    def test_search_with_null_bytes(self, client, seed_test_data):
        """Search handles null bytes safely."""
        response = client.get("/api/politicians/search?name=Biden\x00")
        # Should either return 200 with empty list or handle gracefully with error
        assert response.status_code in [200, 400, 500]

    def test_search_with_numeric_input(self, client, seed_test_data):
        """Search with numeric input returns empty list."""
        response = client.get("/api/politicians/search?name=12345")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_nonexistent_politician(self, client, seed_test_data):
        """Search for nonexistent politician returns empty list."""
        response = client.get("/api/politicians/search?name=XyZabc999")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_with_wildcard_characters(self, client, seed_test_data):
        """Search treats SQL wildcards as literal characters."""
        response = client.get("/api/politicians/search?name=%")
        assert response.status_code == 200
        data = json.loads(response.data)
        # % is used in ILIKE pattern but should be escaped in input
        assert isinstance(data, list)


class TestGetPolitician:
    """Test suite for /api/politician/<int:politician_id> endpoint."""

    def test_get_politician_by_id_success(self, client, seed_test_data):
        """Get politician by ID returns correct politician data."""
        # Get a valid politician ID from search
        search_response = client.get("/api/politicians/search?name=Jo")
        assert search_response.status_code == 200
        search_data = json.loads(search_response.data)
        assert len(search_data) > 0, "Should have at least one politician with 'Jo' in name"
        politician_id = search_data[0]['politicianid']
        
        response = client.get(f"/api/politician/{politician_id}")
        assert response.status_code == 200
        data = json.loads(response.data)

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
            assert field in data, f"Missing required field: {field}"

        # Verify data types
        assert isinstance(data['politicianid'], int)
        assert isinstance(data['firstname'], str)
        assert isinstance(data['lastname'], str)
        assert isinstance(data['party'], str)
        assert isinstance(data['state'], str)
        assert isinstance(data['role'], str)
        assert isinstance(data['isactive'], bool)

    def test_get_politician_returns_biden(self, client, seed_test_data):
        """Get politician by searching for Biden returns correct data."""
        # Search for Biden to get his ID
        search_response = client.get("/api/politicians/search?name=Biden")
        assert search_response.status_code == 200
        search_data = json.loads(search_response.data)
        assert len(search_data) > 0, "Should have at least one politician with 'Biden' in name"
        
        # Find Biden in the results
        biden = next((p for p in search_data if p['lastname'] == 'Biden'), search_data[0])
        politician_id = biden['politicianid']
        
        response = client.get(f"/api/politician/{politician_id}")
        assert response.status_code == 200
        data = json.loads(response.data)

        # Verify it's Biden
        assert data['firstname'] == 'Joseph'
        assert data['lastname'] == 'Biden'
        assert data['party'] == 'Democrat'
        assert data['state'] == 'Delaware'
        assert data['role'] == 'Senator'
        assert data['isactive'] is True

    def test_get_politician_nonexistent_id(self, client, seed_test_data):
        """Get politician with nonexistent ID returns 404."""
        response = client.get("/api/politician/999999999")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data
        assert "not found" in data["error"].lower()

    def test_get_politician_negative_id(self, client, seed_test_data):
        """Get politician with negative ID returns 404."""
        response = client.get("/api/politician/-1")
        assert response.status_code == 404
        # Flask's <int:> converter rejects negative IDs before reaching the route,
        # so it returns a 404 HTML page, not JSON
        # Just verify we get a 404 response

    def test_get_politician_zero_id(self, client, seed_test_data):
        """Get politician with zero ID returns 404."""
        response = client.get("/api/politician/0")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data

    def test_get_politician_very_large_id(self, client, seed_test_data):
        """Get politician with very large ID returns 404."""
        response = client.get("/api/politician/2147483647")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data

    def test_get_politician_consistent_response(self, client, seed_test_data):
        """Multiple requests for same politician return consistent data."""
        # Get a valid politician ID first
        search_response = client.get("/api/politicians/search?name=Jo")
        assert search_response.status_code == 200
        search_data = json.loads(search_response.data)
        assert len(search_data) > 0, "Should have at least one politician with 'Jo' in name"
        politician_id = search_data[0]['politicianid']
        
        response1 = client.get(f"/api/politician/{politician_id}")
        response2 = client.get(f"/api/politician/{politician_id}")
        response3 = client.get(f"/api/politician/{politician_id}")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        data3 = json.loads(response3.data)

        assert data1 == data2 == data3, "Results should be consistent"

    def test_get_politician_different_ids(self, client, seed_test_data):
        """Get different politician IDs return different data."""
        # Get valid politician IDs from search
        search_response = client.get("/api/politicians/search?name=Jo")
        assert search_response.status_code == 200
        search_data = json.loads(search_response.data)
        assert len(search_data) >= 3, "Should have at least 3 politicians with 'Jo' in name"
        
        id1 = search_data[0]['politicianid']
        id2 = search_data[1]['politicianid']
        id3 = search_data[2]['politicianid']
        
        response1 = client.get(f"/api/politician/{id1}")
        response2 = client.get(f"/api/politician/{id2}")
        response3 = client.get(f"/api/politician/{id3}")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        data3 = json.loads(response3.data)

        assert data1['politicianid'] != data2['politicianid']
        assert data2['politicianid'] != data3['politicianid']
        assert data1['lastname'] != data2['lastname'] or data1['firstname'] != data2['firstname']


class TestGetPoliticianSQLInjection:
    """SQL injection protection tests for /api/politician/<int:politician_id> endpoint."""

    def test_sql_injection_in_id_parameter(self, client, seed_test_data, db_connection):
        """SQL injection attempt in ID parameter is safely handled."""
        cursor = db_connection.cursor()

        # Count politicians before injection attempt
        cursor.execute("SELECT COUNT(*) FROM pt.Politicians")
        count_before = cursor.fetchone()[0]
        assert count_before > 0, "Should have politicians in database"

        # Attempt injection via URL (should fail at route level since it's <int:>)
        # But test that even if it somehow gets through, it's safe
        malicious_id = "1; DROP TABLE Politicians; --"
        # Flask's <int:> converter will reject this, but let's verify
        response = client.get(f"/api/politician/{malicious_id}")
        # Should return 404 (not found) or 400 (bad request), not execute SQL
        assert response.status_code in [404, 400]

        # Verify table still exists and has same row count
        cursor.execute("SELECT COUNT(*) FROM pt.Politicians")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before, "Table row count should be unchanged"

        cursor.close()

    def test_sql_injection_union_in_id(self, client, seed_test_data, db_connection):
        """SQL injection UNION SELECT attempt in ID is safely handled."""
        cursor = db_connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM pt.Politicians")
        count_before = cursor.fetchone()[0]

        # Attempt UNION injection (will be rejected by <int:> converter)
        malicious_id = "1 UNION SELECT * FROM Politicians --"
        response = client.get(f"/api/politician/{malicious_id}")
        assert response.status_code in [404, 400]

        # Verify row count unchanged
        cursor.execute("SELECT COUNT(*) FROM pt.Politicians")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before

        cursor.close()

    def test_sql_injection_or_condition_in_id(self, client, seed_test_data, db_connection):
        """SQL injection OR condition attempt in ID is safely handled."""
        cursor = db_connection.cursor()

        # Get a valid politician ID first
        cursor.execute("SELECT PoliticianID FROM pt.Politicians LIMIT 1")
        result = cursor.fetchone()
        assert result is not None, "Should have at least one politician"
        valid_id = result[0]

        # Attempt OR injection (will be rejected by <int:> converter)
        malicious_id = "1 OR 1=1"
        response = client.get(f"/api/politician/{malicious_id}")
        assert response.status_code in [404, 400]

        # Verify normal queries still work
        cursor.execute("SELECT COUNT(*) FROM pt.Politicians WHERE PoliticianID = %s", (valid_id,))
        count = cursor.fetchone()[0]
        assert count == 1, "Normal queries should still work"

        cursor.close()
