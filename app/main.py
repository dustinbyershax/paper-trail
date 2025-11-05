import psycopg2
import psycopg2.extras
import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from app import config


app = Flask(__name__)

# Enable CORS in development only (security requirement)
if os.getenv('FLASK_ENV') == 'development':
    CORS(app)
    print("CORS enabled for development")

# --- TOPIC TO INDUSTRY MAPPING ---
TOPIC_INDUSTRY_MAP = {
    "Health": ["Health Professionals", "Pharmaceuticals", "Health Services", "Hospitals & Nursing Homes"],
    "Finance": ["Real Estate", "Commercial Banks", "Securities & Investment", "Insurance", "Finance"],
    "Technology": ["Telecom Services", "Internet", "Electronics"],
    "Defense": ["Defense Aerospace"],
    "Energy": ["Oil & Gas", "Electric Utilities", "Gas Utilities"],
    "Law": ["Lawyers & Lobbyists", "Consulting", "Business Services"],
    "Education": ["Education"],
    "Foreign Relations": ["Pro-Israel"],
    "Government Operations": ["Government"]
}


def get_db_connection():
    """Establishes database connection."""
    conn = psycopg2.connect(**config.conn_params)
    cursor = conn.cursor()
    cursor.execute("SET search_path TO pt, public;")
    conn.commit()
    cursor.close()
    return conn

@app.route('/')
def index():
    """Serves the main index.html file."""
    return render_template('index.html')

@app.route('/donor_search.html')
def donor_search():
    """Serves the donor_search.html file."""
    return render_template('donor_search.html')

# --- NEW ROUTE FOR FEEDBACK PAGE ---
@app.route('/feedback.html')
def feedback():
    """Serves the feedback.html file."""
    return render_template('feedback.html')
# -----------------------------------

@app.route('/api/politicians/search')
def search_politicians():
    """Searches for politicians by name."""
    query = request.args.get('name', '')
    if len(query) < 2:
        return jsonify([])

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

      # Using 'Politicians' table name based on previous lack of error
        sql = """
            SELECT PoliticianID, FirstName, LastName, Party, State, Role, IsActive
            FROM Politicians
            WHERE (FirstName || ' ' || LastName) ILIKE %s
            ORDER BY IsActive DESC, LastName, FirstName;
        """
        search_query = f"%{query}%"
        cur.execute(sql, (search_query,))


        politicians = cur.fetchall()

        cur.close()
        return jsonify([dict(p) for p in politicians])

    except (Exception, psycopg2.Error) as e:
        print(f"Error searching politicians: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/politician/<int:politician_id>')
def get_politician(politician_id):
    """Gets a single politician by ID."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        sql = """
            SELECT PoliticianID, FirstName, LastName, Party, State, Role, IsActive
            FROM Politicians
            WHERE PoliticianID = %s;
        """
        cur.execute(sql, (politician_id,))
        politician = cur.fetchone()
        cur.close()

        if politician is None:
            return jsonify({"error": "Politician not found"}), 404

        return jsonify(dict(politician))

    except (Exception, psycopg2.Error) as e:
        print(f"Error fetching politician: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/donors/search')
def search_donors_route():
    """Searches for donors by name."""
    query = request.args.get('name', '')
    if len(query) < 3:  # Match the 3-char minimum from the frontend
        return jsonify([])

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Query the 'Donors' table
        sql = """
            SELECT DonorID, Name, DonorType, Employer, State
            FROM Donors
            WHERE Name ILIKE %s
            ORDER BY Name;
        """
        search_query = f"%{query}%"
        cur.execute(sql, (search_query,))
        donors = cur.fetchall()
        cur.close()

        # Format the keys to be lowercase to match the JavaScript
        donor_list = []
        for d in donors:
            donor_list.append({
                "donorid": d['donorid'],
                "name": d['name'],
                "donortype": d['donortype'],
                "employer": d['employer'],
                "state": d['state']
            })

        return jsonify(donor_list)

    except (Exception, psycopg2.Error) as e:
        print(f"Error searching donors: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/donor/<int:donor_id>')
def get_donor(donor_id):
    """Gets a single donor by ID."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        sql = """
            SELECT DonorID, Name, DonorType, Employer, State
            FROM Donors
            WHERE DonorID = %s;
        """
        cur.execute(sql, (donor_id,))
        donor = cur.fetchone()
        cur.close()

        if donor is None:
            return jsonify({"error": "Donor not found"}), 404

        # Format keys to lowercase to match the JavaScript
        return jsonify({
            "donorid": donor['donorid'],
            "name": donor['name'],
            "donortype": donor['donortype'],
            "employer": donor['employer'],
            "state": donor['state']
        })

    except (Exception, psycopg2.Error) as e:
        print(f"Error fetching donor: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/donor/<int:donor_id>/donations')
def get_donor_contributions(donor_id):
    """Gets all donations for a specific donor, joined with politician info."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Join donations with politicians to get the recipient's info
        sql = """
            SELECT 
                t.Amount, 
                t.Date,
                p.FirstName, 
                p.LastName, 
                p.Party, 
                p.State
            FROM donations t
            JOIN Politicians p ON t.PoliticianID = p.PoliticianID
            WHERE t.DonorID = %s
            ORDER BY t.Date DESC, t.Amount DESC;
        """
        cur.execute(sql, (donor_id,))
        donations = cur.fetchall()
        cur.close()

        # Format the list to match what the frontend JavaScript expects
        donation_list = []
        for d in donations:
            donation_list.append({
                # Ensure amount is a float for JSON
                "amount": float(d['amount']), 
                "date": d['date'],
                "firstname": d['firstname'],
                "lastname": d['lastname'],
                "party": d['party'],
                "state": d['state']
            })
        
        return jsonify(donation_list)

    except (Exception, psycopg2.Error) as e:
        print(f"Error fetching donor contributions: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/politician/<int:politician_id>/votes')
def get_politician_votes(politician_id):
    """Gets paginated and filtered vote history for a politician."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        page = int(request.args.get('page', 1))
        per_page = 10
        offset = (page - 1) * per_page
        sort_order = request.args.get('sort', 'desc').upper()
        if sort_order not in ['ASC', 'DESC']:
            sort_order = 'DESC'

        bill_types = request.args.getlist('type') # e.g., ['hr', 's']
        bill_subjects = request.args.getlist('subject')

        where_clauses = ["v.PoliticianID = %s"]
        params = [politician_id]

        # --- NEW Bill Type Filter Logic ---
        if bill_types:
            # Build OR conditions for bill numbers starting with the types
            # Example: "(b.BillNumber ILIKE 'hr %' OR b.BillNumber ILIKE 's %')"
            type_conditions = []
            for bill_type in bill_types:
                # Add a condition like "b.BillNumber ILIKE %s"
                type_conditions.append("b.BillNumber ILIKE %s")
                # Add the corresponding pattern like 'hr %' to params
                params.append(f"{bill_type}%")
            
            # Join the conditions with OR and wrap in parentheses
            where_clauses.append(f"({' OR '.join(type_conditions)})")
        # --- END NEW Bill Type Filter Logic ---

        if bill_subjects:
            where_clauses.append("b.subjects && %s")
            params.append(bill_subjects)

        where_sql = " AND ".join(where_clauses)

        count_sql = f"SELECT COUNT(*) FROM votes v JOIN bills b ON v.BillID = b.BillID WHERE {where_sql};"
        # Make sure params are passed as a tuple
        cur.execute(count_sql, tuple(params))
        total_votes = cur.fetchone()['count']
        total_pages = (total_votes + per_page - 1) // per_page

        # Selecting columns that exist in your tables
        data_sql = f"""
            SELECT v.VoteID, v.vote, b.BillNumber, b.Title, b.DateIntroduced, b.subjects
            FROM votes v
            JOIN bills b ON v.BillID = b.BillID
            WHERE {where_sql}
            ORDER BY b.DateIntroduced {sort_order}
            LIMIT %s OFFSET %s;
        """
        # Create a new list for data query params including limit and offset
        data_params = list(params)
        data_params.extend([per_page, offset])

        cur.execute(data_sql, tuple(data_params))
        votes_data = cur.fetchall()

        votes_list = []
        for row in votes_data:
            votes_list.append({
                "VoteID": row['voteid'],
                "Vote": row['vote'],
                "BillNumber": row['billnumber'],
                "Title": row['title'],
                "DateIntroduced": row['dateintroduced'],
                "subjects": row['subjects']
            })

        cur.close()

        return jsonify({
            "pagination": {
                "currentPage": page,
                "totalPages": total_pages,
                "totalVotes": total_votes
            },
            "votes": votes_list
        })

    except (Exception, psycopg2.Error) as e:
        print(f"Error fetching votes: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/politician/<int:politician_id>/donations/summary')
def get_donation_summary(politician_id):
    """Gets UNFILTERED donation summary, grouped by INDUSTRY."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Use lowercase table names (matching votes query and confirmed working)
        sql = """
            SELECT d.Industry, SUM(t.Amount) AS TotalAmount
            FROM donations t
            JOIN donors d ON t.DonorID = d.DonorID
            WHERE t.PoliticianID = %s
            GROUP BY d.Industry
            HAVING d.Industry IS NOT NULL
            ORDER BY TotalAmount DESC;
        """

        # Debug: Check if donations exist for this politician (using lowercase table name)
        check_sql = "SELECT COUNT(*) FROM donations WHERE PoliticianID = %s;"
        cur.execute(check_sql, (politician_id,))
        donation_count = cur.fetchone()[0]
        print(f"DEBUG: Total donations for politician_id {politician_id}: {donation_count}")

        # Debug: Check if donors have Industry set (using lowercase table names)
        check_industry_sql = """
            SELECT COUNT(*) FROM donations t
            JOIN donors d ON t.DonorID = d.DonorID
            WHERE t.PoliticianID = %s AND d.Industry IS NOT NULL;
        """
        cur.execute(check_industry_sql, (politician_id,))
        industry_count = cur.fetchone()[0]
        print(f"DEBUG: Donations with Industry set: {industry_count}")

        # Execute the query
        cur.execute(sql, (politician_id,))
        summary_data = cur.fetchall()

        print(f"DEBUG: Query returned {len(summary_data)} rows for politician_id {politician_id}")
        if len(summary_data) > 0:
            print(f"DEBUG: First row: {summary_data[0]}")
        else:
            print(f"DEBUG: No rows returned - this politician has no donation data in the database")

        summary_list = []
        for row in summary_data:
            # Handle both lowercase and uppercase column names from PostgreSQL
            industry = row.get('industry') or row.get('Industry') or 'Other'
            totalamount = float(row.get('totalamount') or row.get('TotalAmount') or 0)
            summary_list.append({
                "industry": industry,
                "totalamount": totalamount
            })

        cur.close()
        return jsonify(summary_list)

    except (Exception, psycopg2.Error) as e:
        print(f"Error fetching donation summary: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/politician/<int:politician_id>/donations/summary/filtered')
def get_filtered_donation_summary(politician_id):
    """Gets donation summary filtered by a bill topic."""
    topic = request.args.get('topic')
    if not topic:
        return jsonify({"error": "No topic specified"}), 400

    industries = TOPIC_INDUSTRY_MAP.get(topic)
    if not industries:
        return jsonify([])

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Use lowercase table names to match how PostgreSQL stores them
        sql = """
            SELECT d.Industry, SUM(t.Amount) AS TotalAmount
            FROM donations t
            JOIN donors d ON t.DonorID = d.DonorID
            WHERE t.PoliticianID = %s
            AND d.Industry = ANY(%s)
            GROUP BY d.Industry
            HAVING d.Industry IS NOT NULL
            ORDER BY TotalAmount DESC;
        """

        cur.execute(sql, (politician_id, industries))
        summary_data = cur.fetchall()

        summary_list = [
            # Assuming Industry and Amount column names are correct
            {"industry": row['industry'], "totalamount": float(row['totalamount'])}
            for row in summary_data
        ]

        cur.close()
        return jsonify(summary_list)

    except (Exception, psycopg2.Error) as e:
        print(f"Error fetching filtered donation summary: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/bills/subjects')
def get_all_bill_subjects():
    """Gets all unique bill subjects from the Bills table."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Use UNNEST to expand the 'subjects' array column,
        # get all distinct non-null subjects, and order them.
        sql = """
            SELECT DISTINCT UNNEST(subjects) AS subject 
            FROM Bills 
            WHERE subjects IS NOT NULL AND subjects != '{}'
            ORDER BY subject;
        """
        cur.execute(sql)
        results = cur.fetchall()
        
        # Convert the list of dicts ([{'subject': 'Health'}, ...])
        # into a simple list of strings (['Health', ...])
        subject_list = [row['subject'] for row in results] 
        
        cur.close()
        return jsonify(subject_list) # Flask automatically returns this as JSON

    except (Exception, psycopg2.Error) as e:
        print(f"Error fetching bill subjects: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=debug_mode)
