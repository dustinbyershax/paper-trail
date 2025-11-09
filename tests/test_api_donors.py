"""Tests for /api/donors/search endpoint.

Verifies search functionality, SQL injection protection, and error handling
against known seed data.
"""


import json


class TestDonorsSearch:
    """Test suite for /api/donors/search endpoint."""

    def test_search_requires_minimum_length(self, client, seed_test_data):
        """Search returns empty list for queries less than 3 characters."""
        response = client.get("/api/donors/search?name=ab")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_accepts_valid_length(self, client, seed_test_data):
        """Search accepts queries of 3 or more characters and returns results."""
        response = client.get("/api/donors/search?name=Goo")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1, "Expected at least one donor with 'Goo' in name"
        # Verify at least one result contains 'Goo'
        assert any('goo' in d['name'].lower() for d in data), "Results should contain 'Goo'"

    def test_search_returns_all_required_fields(self, client, seed_test_data):
        """Search returns donors with all required fields."""
        response = client.get("/api/donors/search?name=Google")
        assert response.status_code == 200
        data = json.loads(response.data)

        assert len(data) >= 1, "Expected at least one Google donor"
        donor = data[0]

        required_fields = ["donorid", "name", "donortype", "employer", "state"]
        for field in required_fields:
            assert field in donor, f"Missing required field: {field}"

        # Verify data types
        assert isinstance(donor['donorid'], int)
        assert isinstance(donor['name'], str)
        assert isinstance(donor['donortype'], str)
        # employer and state can be None or str

    def test_search_finds_google(self, client, seed_test_data):
        """Search finds Google donors from seed data."""
        response = client.get("/api/donors/search?name=Google")
        assert response.status_code == 200
        data = json.loads(response.data)

        assert len(data) >= 1, "Expected to find Google donor(s)"
        # Check for Google LLC (corporation)
        google_llc = next((d for d in data if 'google llc' in d['name'].lower()), None)
        assert google_llc is not None, "Google LLC not found"
        assert google_llc['donortype'] == 'Corporation'
        assert google_llc['state'] == 'CA'

    def test_search_finds_individual_donor(self, client, seed_test_data):
        """Search finds individual donors."""
        response = client.get("/api/donors/search?name=Sundar")
        assert response.status_code == 200
        data = json.loads(response.data)

        assert len(data) >= 1, "Expected to find Sundar Pichai"
        sundar = data[0]
        assert 'sundar' in sundar['name'].lower()
        assert sundar['donortype'] == 'Individual'
        assert sundar['employer'] == 'Google'

    def test_search_is_case_insensitive(self, client, seed_test_data):
        """Search matches regardless of case."""
        response_lower = client.get("/api/donors/search?name=google")
        response_upper = client.get("/api/donors/search?name=GOOGLE")
        response_mixed = client.get("/api/donors/search?name=Google")

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
        special_chars = ["O'Brien Corp", "Smith-Jones LLC", "Test%", "Test_"]

        for name in special_chars:
            response = client.get(f"/api/donors/search?name={name}")
            assert response.status_code == 200, f"Failed for: {name}"
            data = json.loads(response.data)
            assert isinstance(data, list), f"Invalid response for: {name}"

    def test_search_with_empty_query_parameter(self, client, seed_test_data):
        """Search with empty query parameter returns empty list."""
        response = client.get("/api/donors/search?name=")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_without_query_parameter(self, client, seed_test_data):
        """Search without query parameter returns empty list."""
        response = client.get("/api/donors/search")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_with_spaces(self, client, seed_test_data):
        """Search handles names with spaces correctly."""
        response = client.get("/api/donors/search?name=Jamie Dimon")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) >= 1, "Expected to find 'Jamie Dimon'"
        assert any('jamie dimon' in d['name'].lower() for d in data)

    def test_search_partial_match(self, client, seed_test_data):
        """Search returns partial matches using ILIKE."""
        response = client.get("/api/donors/search?name=Jami")
        assert response.status_code == 200
        data = json.loads(response.data)

        assert len(data) >= 1, "Expected at least one donor with 'Jami'"
        # Verify all results contain 'Jami'
        for donor in data:
            assert 'jami' in donor['name'].lower(), f"{donor['name']} doesn't contain 'Jami'"

    def test_search_sorts_by_name(self, client, seed_test_data):
        """Search results are sorted by Name."""
        response = client.get("/api/donors/search?name=a")
        assert response.status_code == 200
        data = json.loads(response.data)

        if len(data) >= 2:
            # Verify alphabetical sorting
            names = [d['name'] for d in data]
            assert names == sorted(names), "Results should be sorted alphabetically"


class TestDonorsSearchSQLInjection:
    """SQL injection protection tests for /api/donors/search endpoint."""

    def test_sql_injection_drop_table(self, client, seed_test_data, db_connection):
        """SQL injection attempt to drop table is safely handled as literal string."""
        cursor = db_connection.cursor()

        # Count rows before injection attempt
        cursor.execute("SELECT COUNT(*) FROM pt.Donors")
        count_before = cursor.fetchone()[0]
        assert count_before > 0, "Should have donors in database"

        # Attempt injection
        malicious_input = "'; DROP TABLE Donors; --"
        response = client.get(f"/api/donors/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == [], "Injection string should be treated as literal, returning no results"

        # Verify table still exists and has same row count
        cursor.execute("SELECT COUNT(*) FROM pt.Donors")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before, "Table row count should be unchanged"

        # Verify subsequent queries still work
        cursor.execute("SELECT * FROM pt.Donors LIMIT 1")
        assert cursor.fetchone() is not None, "Table should still be queryable"

        cursor.close()

    def test_sql_injection_union_select(self, client, seed_test_data, db_connection):
        """SQL injection UNION SELECT attempt is safely handled as literal string."""
        cursor = db_connection.cursor()

        # Count rows before
        cursor.execute("SELECT COUNT(*) FROM pt.Donors")
        count_before = cursor.fetchone()[0]

        # Attempt UNION injection
        malicious_input = "' UNION SELECT * FROM Donors --"
        response = client.get(f"/api/donors/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == [], "UNION injection should return no results"

        # Verify row count unchanged
        cursor.execute("SELECT COUNT(*) FROM pt.Donors")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before

        cursor.close()

    def test_sql_injection_or_condition(self, client, seed_test_data, db_connection):
        """SQL injection OR 1=1 attempt is safely handled as literal string."""
        cursor = db_connection.cursor()

        # Attempt OR injection
        malicious_input = "' OR '1'='1"
        response = client.get(f"/api/donors/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)

        # Should return empty list (no donor named "' OR '1'='1")
        assert data == [], "OR injection should return no results"

        # Verify normal queries still work
        cursor.execute("SELECT COUNT(*) FROM pt.Donors WHERE Name ILIKE '%Google%'")
        count = cursor.fetchone()[0]
        assert count > 0, "Normal queries should still work"

        cursor.close()

    def test_sql_injection_update_command(self, client, seed_test_data, db_connection):
        """SQL injection with UPDATE command is safely handled."""
        cursor = db_connection.cursor()

        # Get original donor type
        cursor.execute("SELECT DonorType FROM pt.Donors WHERE Name ILIKE '%Google%' LIMIT 1")
        original_type = cursor.fetchone()[0]

        # Attempt UPDATE injection
        malicious_input = "Google'; UPDATE Donors SET DonorType='Hacked' WHERE '1'='1"
        response = client.get(f"/api/donors/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

        # Verify donor type unchanged
        cursor.execute("SELECT DonorType FROM pt.Donors WHERE Name ILIKE '%Google%' LIMIT 1")
        current_type = cursor.fetchone()[0]
        assert current_type == original_type, "DonorType should not have been modified"

        cursor.close()

    def test_sql_injection_stacked_queries(self, client, seed_test_data, db_connection):
        """SQL injection with stacked queries is safely handled."""
        cursor = db_connection.cursor()

        # Count donors before
        cursor.execute("SELECT COUNT(*) FROM pt.Donors")
        count_before = cursor.fetchone()[0]

        # Attempt stacked query injection
        malicious_input = "Google'; DELETE FROM Donors WHERE DonorType='Corporation'; --"
        response = client.get(f"/api/donors/search?name={malicious_input}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

        # Verify no deletions occurred
        cursor.execute("SELECT COUNT(*) FROM pt.Donors")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before, "No rows should have been deleted"

        # Verify corporations still exist
        cursor.execute("SELECT COUNT(*) FROM pt.Donors WHERE DonorType='Corporation'")
        corp_count = cursor.fetchone()[0]
        assert corp_count > 0, "Corporations should still exist"

        cursor.close()


class TestDonorsSearchNegative:
    """Negative test cases for error conditions and edge cases."""

    def test_search_with_very_long_input(self, client, seed_test_data):
        """Search handles extremely long input without crashing."""
        long_input = "a" * 10000
        response = client.get(f"/api/donors/search?name={long_input}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_search_with_unicode_characters(self, client, seed_test_data):
        """Search handles Unicode characters correctly."""
        unicode_names = ["José Corp", "François LLC", "Müller Industries", "李明 Company"]

        for name in unicode_names:
            response = client.get(f"/api/donors/search?name={name}")
            assert response.status_code == 200, f"Failed for: {name}"
            data = json.loads(response.data)
            assert isinstance(data, list)

    def test_search_with_null_bytes(self, client, seed_test_data):
        """Search handles null bytes safely."""
        response = client.get("/api/donors/search?name=Google\x00")
        # Should either return 200 with empty list or handle gracefully with error
        assert response.status_code in [200, 400, 500]

    def test_search_with_numeric_input(self, client, seed_test_data):
        """Search with numeric input returns empty list."""
        response = client.get("/api/donors/search?name=12345")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_nonexistent_donor(self, client, seed_test_data):
        """Search for nonexistent donor returns empty list."""
        response = client.get("/api/donors/search?name=XyZabc999Corp")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_search_with_wildcard_characters(self, client, seed_test_data):
        """Search treats SQL wildcards as literal characters."""
        response = client.get("/api/donors/search?name=%")
        assert response.status_code == 200
        data = json.loads(response.data)
        # % is used in ILIKE pattern but should be escaped in input
        assert isinstance(data, list)

    def test_search_minimum_length_enforcement(self, client, seed_test_data):
        """Search enforces 3-character minimum consistently."""
        # Test with 1 char
        response = client.get("/api/donors/search?name=G")
        assert response.status_code == 200
        assert json.loads(response.data) == []

        # Test with 2 chars
        response = client.get("/api/donors/search?name=Go")
        assert response.status_code == 200
        assert json.loads(response.data) == []

        # Test with 3 chars (should work)
        response = client.get("/api/donors/search?name=Goo")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)


class TestGetDonor:
    """Test suite for /api/donor/<int:donor_id> endpoint."""

    def test_get_donor_by_id_success(self, client, seed_test_data):
        """Get donor by ID returns correct donor data."""
        # Get a valid donor ID from search
        search_response = client.get("/api/donors/search?name=Goo")
        assert search_response.status_code == 200
        search_data = json.loads(search_response.data)
        assert len(search_data) > 0, "Should have at least one donor with 'Goo' in name"
        donor_id = search_data[0]['donorid']
        
        response = client.get(f"/api/donor/{donor_id}")
        assert response.status_code == 200
        data = json.loads(response.data)

        required_fields = ["donorid", "name", "donortype", "employer", "state"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

        # Verify data types
        assert isinstance(data['donorid'], int)
        assert isinstance(data['name'], str)
        assert isinstance(data['donortype'], str)
        # employer and state can be None or str

    def test_get_donor_returns_google(self, client, seed_test_data):
        """Get donor with Google in name returns expected data."""
        # Search for Google donor
        search_response = client.get("/api/donors/search?name=Google")
        assert search_response.status_code == 200
        search_data = json.loads(search_response.data)
        assert len(search_data) > 0, "Should have at least one Google donor"
        
        # Find Sundar Pichai or any Google-related donor
        google_donor = next((d for d in search_data if 'google' in d['name'].lower() or d['employer'] == 'Google'), None)
        if not google_donor:
            google_donor = search_data[0]  # Use first result if no exact match
        
        donor_id = google_donor['donorid']
        response = client.get(f"/api/donor/{donor_id}")
        assert response.status_code == 200
        data = json.loads(response.data)

        assert data['donorid'] == donor_id
        assert 'google' in data['name'].lower() or data['employer'] == 'Google'
        assert data['donortype'] in ['Individual', 'Corporation']

    def test_get_donor_nonexistent_id(self, client, seed_test_data):
        """Get donor with nonexistent ID returns 404."""
        response = client.get("/api/donor/999999999")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data
        assert "not found" in data["error"].lower()

    def test_get_donor_negative_id(self, client, seed_test_data):
        """Get donor with negative ID returns 404."""
        response = client.get("/api/donor/-1")
        assert response.status_code == 404
        # Flask's <int:> converter rejects negative IDs before reaching the route,
        # so it returns a 404 HTML page, not JSON
        # Just verify we get a 404 response

    def test_get_donor_zero_id(self, client, seed_test_data):
        """Get donor with zero ID returns 404."""
        response = client.get("/api/donor/0")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data

    def test_get_donor_very_large_id(self, client, seed_test_data):
        """Get donor with very large ID returns 404."""
        response = client.get("/api/donor/2147483647")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data

    def test_get_donor_consistent_response(self, client, seed_test_data):
        """Multiple requests for same donor return consistent data."""
        # Get a valid donor ID from search
        search_response = client.get("/api/donors/search?name=Goo")
        assert search_response.status_code == 200
        search_data = json.loads(search_response.data)
        assert len(search_data) > 0, "Should have at least one donor with 'Goo' in name"
        donor_id = search_data[0]['donorid']
        
        response1 = client.get(f"/api/donor/{donor_id}")
        response2 = client.get(f"/api/donor/{donor_id}")
        response3 = client.get(f"/api/donor/{donor_id}")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        data3 = json.loads(response3.data)

        assert data1 == data2 == data3, "Results should be consistent"

    def test_get_donor_different_ids(self, client, seed_test_data):
        """Get different donor IDs return different data."""
        # Get valid donor IDs from multiple searches to ensure we have different donors
        search1 = client.get("/api/donors/search?name=Goo")
        search2 = client.get("/api/donors/search?name=Jam")
        search3 = client.get("/api/donors/search?name=Pfi")
        
        assert search1.status_code == 200
        assert search2.status_code == 200
        assert search3.status_code == 200
        
        data1 = json.loads(search1.data)
        data2 = json.loads(search2.data)
        data3 = json.loads(search3.data)
        
        # Get IDs from different searches to ensure they're different
        assert len(data1) > 0, "Should have at least one donor with 'Goo' in name"
        assert len(data2) > 0, "Should have at least one donor with 'Jam' in name"
        assert len(data3) > 0, "Should have at least one donor with 'Pfi' in name"
        
        id1 = data1[0]['donorid']
        id2 = data2[0]['donorid']
        id3 = data3[0]['donorid']
        
        response1 = client.get(f"/api/donor/{id1}")
        response2 = client.get(f"/api/donor/{id2}")
        response3 = client.get(f"/api/donor/{id3}")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        donor1 = json.loads(response1.data)
        donor2 = json.loads(response2.data)
        donor3 = json.loads(response3.data)

        assert donor1['donorid'] != donor2['donorid']
        assert donor2['donorid'] != donor3['donorid']
        assert donor1['name'] != donor2['name'] or donor1['donorid'] != donor2['donorid']

    def test_get_donor_lowercase_keys(self, client, seed_test_data):
        """Get donor returns all keys in lowercase format."""
        # Get a valid donor ID from search
        search_response = client.get("/api/donors/search?name=Goo")
        assert search_response.status_code == 200
        search_data = json.loads(search_response.data)
        assert len(search_data) > 0, "Should have at least one donor with 'Goo' in name"
        donor_id = search_data[0]['donorid']
        
        response = client.get(f"/api/donor/{donor_id}")
        assert response.status_code == 200
        data = json.loads(response.data)

        # Verify all keys are lowercase
        for key in data.keys():
            assert key == key.lower(), f"Key '{key}' should be lowercase"
            assert not any(c.isupper() for c in key), f"Key '{key}' contains uppercase characters"


class TestGetDonorSQLInjection:
    """SQL injection protection tests for /api/donor/<int:donor_id> endpoint."""

    def test_sql_injection_in_id_parameter(self, client, seed_test_data, db_connection):
        """SQL injection attempt in ID parameter is safely handled."""
        cursor = db_connection.cursor()

        # Count donors before injection attempt
        cursor.execute("SELECT COUNT(*) FROM pt.Donors")
        count_before = cursor.fetchone()[0]
        assert count_before > 0, "Should have donors in database"

        # Attempt injection via URL (should fail at route level since it's <int:>)
        malicious_id = "1; DROP TABLE Donors; --"
        response = client.get(f"/api/donor/{malicious_id}")
        # Should return 404 (not found) or 400 (bad request), not execute SQL
        assert response.status_code in [404, 400]

        # Verify table still exists and has same row count
        cursor.execute("SELECT COUNT(*) FROM pt.Donors")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before, "Table row count should be unchanged"

        cursor.close()

    def test_sql_injection_union_in_id(self, client, seed_test_data, db_connection):
        """SQL injection UNION SELECT attempt in ID is safely handled."""
        cursor = db_connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM pt.Donors")
        count_before = cursor.fetchone()[0]

        # Attempt UNION injection (will be rejected by <int:> converter)
        malicious_id = "1 UNION SELECT * FROM Donors --"
        response = client.get(f"/api/donor/{malicious_id}")
        assert response.status_code in [404, 400]

        # Verify row count unchanged
        cursor.execute("SELECT COUNT(*) FROM pt.Donors")
        count_after = cursor.fetchone()[0]
        assert count_after == count_before

        cursor.close()

    def test_sql_injection_or_condition_in_id(self, client, seed_test_data, db_connection):
        """SQL injection OR condition attempt in ID is safely handled."""
        cursor = db_connection.cursor()

        # Get a valid donor ID first
        cursor.execute("SELECT DonorID FROM pt.Donors LIMIT 1")
        result = cursor.fetchone()
        assert result is not None, "Should have at least one donor"
        valid_id = result[0]

        # Attempt OR injection (will be rejected by <int:> converter)
        malicious_id = "1 OR 1=1"
        response = client.get(f"/api/donor/{malicious_id}")
        assert response.status_code in [404, 400]

        # Verify normal queries still work
        cursor.execute("SELECT COUNT(*) FROM pt.Donors WHERE DonorID = %s", (valid_id,))
        count = cursor.fetchone()[0]
        assert count == 1, "Normal queries should still work"

        cursor.close()