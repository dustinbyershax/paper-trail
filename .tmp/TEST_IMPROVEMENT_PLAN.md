# Test Infrastructure & Quality Improvement Plan

**Status:** ✅ Phase 1-3 Complete (on `update-test-base` branch)
**Started:** 2025-11-03
**Completed:** 2025-11-03
**Target:** 90%+ test coverage with comprehensive test infrastructure

## Summary of Completed Work

**Branch:** `update-test-base` (commit: `05ae2e6`)

**Test Results:** All 135 tests passing in 5.69s

### Key Accomplishments

1. **Critical Database Safety** ✅
   - Created `paper_trail_test` database
   - Added TESTING environment variable check in `app/config.py`
   - Created `.env.test` with test database configuration
   - Added safety check in `tests/conftest.py` to prevent production data corruption

2. **Comprehensive Test Rewrite** ✅
   - Rewrote all 5 API test files from scratch
   - Total: 135 tests (up from 144, more focused)
   - Strong assertions validating specific seed data values
   - Test breakdown:
     * `test_api_politicians.py`: 24 tests
     * `test_api_donors.py`: 24 tests
     * `test_api_bills.py`: 17 tests
     * `test_api_donations.py`: 30 tests
     * `test_api_votes.py`: 40 tests

3. **SQL Injection Protection** ✅
   - Added 24 SQL injection tests across all endpoints
   - Tests prove parameterization works by verifying:
     * Table row counts unchanged before/after injection attempts
     * Injection strings treated as literals (return empty results)
     * Subsequent queries still work (tables not dropped/modified)

4. **Edge Case Coverage** ✅
   - Unicode characters, special characters, null bytes
   - Very long inputs (10,000+ characters)
   - Invalid IDs, empty parameters, nonexistent resources
   - Pagination edge cases (negative page, zero page, very high page)
   - Consistency validation (multiple calls return same data)

**Next Steps:** Remaining phases (UV support, CI/CD, documentation) or merge to `main`

---

## Phase 1: Test Database Infrastructure ✅ COMPLETE

**Goal:** Isolate tests from production data completely

### Tasks
- [x] Create `app/config.py` with test database configuration
- [x] Create `.env.test` template with test database credentials
- [x] Update `tests/conftest.py` with database fixtures:
  - `db_connection` - test database connection
  - `setup_test_db` - session-scoped schema creation
  - `seed_test_data` - comprehensive seed data (50+ records per table)
  - `clean_db` - cleanup between tests
- [x] Create `tests/fixtures/seed_data.py` with known test data

**Database Details:**
- Test database name: `paper_trail_test`
- Seed data: 50+ records per table (comprehensive coverage)
- Schema: Uses `pt` schema like production
- Isolation: Clean tables between tests

---

## Phase 2: Strengthen Test Assertions ✅ COMPLETE

**Goal:** Make tests verify actual behavior, not just "didn't crash"

### Tasks
- [x] Fix weak assertions in `test_api_politicians.py` (24 tests - completely rewritten)
- [x] Fix weak assertions in `test_api_donors.py` (24 tests - completely rewritten)
- [x] Fix weak assertions in `test_api_bills.py` (17 tests - completely rewritten)
- [x] Fix weak assertions in `test_api_donations.py` (30 tests - completely rewritten)
- [x] Fix weak assertions in `test_api_votes.py` (40 tests - completely rewritten)
- [x] Strengthen ALL SQL injection tests to prove parameterization works (24 injection tests added)

**Anti-patterns to fix:**
```python
# BAD: Just checks it returns something
assert isinstance(data, list)

# GOOD: Verifies actual business logic
assert len(data) == 2
assert 'biden' in data[0]['firstname'].lower()
```

**SQL Injection test improvements:**
```python
# Must verify:
1. Table row counts unchanged before/after injection
2. Injection treated as literal string (returns empty list)
3. Subsequent queries still work (table not dropped)
```

---

## Phase 3: Add Negative Test Cases ✅ COMPLETE

**Goal:** Test error conditions and edge cases properly

### Tasks
- [x] Add negative tests for politicians endpoint (6 tests in TestPoliticiansSearchNegative)
- [x] Add negative tests for donors endpoint (7 tests in TestDonorsSearchNegative)
- [x] Add negative tests for donations endpoint (5 tests in TestFilteredDonationSummaryEdgeCases)
- [x] Add negative tests for votes endpoint (13 tests in TestPoliticianVotesEdgeCases)
- [x] Add negative tests for bills endpoint (7 tests in TestBillSubjectsEdgeCases)
- [ ] Standardize error responses in `app/main.py` (deferred - API works correctly)

**New test scenarios:**
- Database connection failures
- Invalid input types (overflow, scientific notation)
- Empty result scenarios (politician with $0 donations)
- Null/empty fields (bills with null subjects)
- Page overflow (page=2147483648)
- Concurrent request handling

**Error standardization:**
- 400 for invalid input
- 404 for not found
- 500 for database/server errors
- 200 with empty list for "no results"

---

## Phase 4: Move Tests to Standard Location ✅ N/A - ALREADY DONE

**Goal:** Follow Python conventions

**Status:** Tests were already in standard `tests/` directory. This phase was not needed.

---

## Phase 5: Add UV Support (Keep pip compatibility) ⏳

**Goal:** Support both pip and uv workflows

### Tasks
- [ ] Create `pyproject.toml` with:
  - Python 3.13 requirement
  - Core dependencies (Flask, psycopg2, python-dotenv, gunicorn)
  - Dev dependencies (pytest, pytest-cov, black, ruff)
  - Tool configs (pytest, black, ruff)
- [ ] Keep existing `requirements.txt` for pip users
- [ ] Update README.md with both setup options

---

## Phase 6: GitHub Actions CI/CD ⏳

**Goal:** Automated testing on all PRs with strict quality gates

### Tasks
- [ ] Create `.github/workflows/tests.yml`:
  - PostgreSQL 16 service container
  - Python 3.13 + uv setup
  - Database schema bootstrap
  - Run tests with coverage
  - **Enforce 90% coverage threshold** (fail PR if below)
  - Upload coverage to Codecov
- [ ] Add status badge to README.md

**CI Requirements:**
- ✅ All tests must pass
- ✅ 90%+ code coverage (enforced)
- ✅ Pristine output (no warnings/errors)
- ✅ PostgreSQL 16 service container
- ✅ Automated on all PRs

---

## Phase 7: Documentation ⏳

**Goal:** Comprehensive testing documentation

### Tasks
- [ ] Create `tests/README.md` with:
  - Test database setup instructions
  - How to run tests locally (pip and uv)
  - TDD workflow expectations
  - Assertion strength requirements
  - Coverage expectations (>90%)
  - How to add seed data for new features

---

## Implementation Order

1. **Phase 1** (Test Database) - **MUST BE FIRST** - Everything depends on this
2. **Phase 4** (Move tests) - Clean directory structure before major changes
3. **Phases 2 & 3** (in parallel) - Strengthen assertions + Add negative tests
4. **Phase 5** (UV + pip support) - Modernize tooling
5. **Phase 6** (CI/CD) - Requires all previous phases complete
6. **Phase 7** (Documentation) - Final step

---

## Success Criteria

- ✅ Tests run against isolated `paper_trail_test` database
- ✅ Tests create and destroy test data for each test
- ✅ All assertions verify specific expected values (not just types)
- ✅ SQL injection tests prove parameterization works (no execution)
- ✅ Negative tests cover errors, empty results, invalid input
- ✅ CI/CD passes on every PR
- ✅ 90%+ code coverage enforced in CI
- ✅ Pristine test output (no warnings/errors in logs)
- ✅ Both pip and uv workflows supported

---

## Configuration Decisions

- **Test DB Name:** `paper_trail_test`
- **Seed Data Size:** 50+ records per table (comprehensive)
- **Coverage Threshold:** 90% (enforced in CI, PR fails if below)
- **Dependency Management:** Both `pyproject.toml` and `requirements.txt`

---

## Current Test Issues from PR #1

**Critical Issues Found:**
1. ❌ Tests use production database (dangerous)
2. ❌ Weak assertions (testing types, not behavior)
3. ❌ SQL injection tests don't verify parameterization
4. ❌ Missing negative test cases
5. ❌ API inconsistency not caught (PascalCase vs snake_case)
6. ❌ Tautological assertions (`if len(data) > 0: assert len(data) > 0`)
7. ❌ No CI/CD pipeline

**Test Count:** 144 existing tests need strengthening + ~30 new tests needed

---

## Progress Tracking

**Phase 1:** ✅ 100% complete (on `update-test-base` branch)
**Phase 2:** ✅ 100% complete (on `update-test-base` branch)
**Phase 3:** ✅ 100% complete (on `update-test-base` branch)
**Phase 4:** ✅ N/A (already done)
**Phase 5:** ⏳ 0% complete (UV support - not started)
**Phase 6:** ⏳ 0% complete (CI/CD - not started)
**Phase 7:** ⏳ 0% complete (Documentation - not started)

**Overall:** 43% complete (3 of 7 phases done)

**Work Location:** All completed work is on the `update-test-base` branch, not yet merged to `main`

---

## Notes

- User follows strict TDD principles - tests must verify actual behavior
- User requires pristine test output - no warnings or errors in logs
- All changes must be systematic and thorough (no shortcuts)
- SQL injection tests are particularly important to prove security
- Test isolation is critical - each test must be independent
