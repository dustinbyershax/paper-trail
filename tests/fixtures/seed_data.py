from datetime import date, timedelta


def seed_politicians(cursor):
    """Seed 60 politicians with diverse attributes."""
    politicians = [
        # Democrats - Senate
        ("Joseph", "Biden", "Democrat", "Senate", "Delaware", None, True, "Senator"),
        (
            "Elizabeth",
            "Warren",
            "Democrat",
            "Senate",
            "Massachusetts",
            None,
            True,
            "Senator",
        ),
        (
            "Bernie",
            "Sanders",
            "Independent",
            "Senate",
            "Vermont",
            None,
            True,
            "Senator",
        ),
        ("Kamala", "Harris", "Democrat", "Senate", "California", None, True, "Senator"),
        ("Cory", "Booker", "Democrat", "Senate", "New Jersey", None, True, "Senator"),
        ("Amy", "Klobuchar", "Democrat", "Senate", "Minnesota", None, True, "Senator"),
        ("Chuck", "Schumer", "Democrat", "Senate", "New York", None, True, "Senator"),
        (
            "Kirsten",
            "Gillibrand",
            "Democrat",
            "Senate",
            "New York",
            None,
            True,
            "Senator",
        ),
        ("Dick", "Durbin", "Democrat", "Senate", "Illinois", None, True, "Senator"),
        ("Tammy", "Duckworth", "Democrat", "Senate", "Illinois", None, True, "Senator"),
        # Republicans - Senate
        (
            "Mitch",
            "McConnell",
            "Republican",
            "Senate",
            "Kentucky",
            None,
            True,
            "Senator",
        ),
        ("Ted", "Cruz", "Republican", "Senate", "Texas", None, True, "Senator"),
        ("John", "Cornyn", "Republican", "Senate", "Texas", None, True, "Senator"),
        ("Marco", "Rubio", "Republican", "Senate", "Florida", None, True, "Senator"),
        ("Rick", "Scott", "Republican", "Senate", "Florida", None, True, "Senator"),
        (
            "Lindsey",
            "Graham",
            "Republican",
            "Senate",
            "South Carolina",
            None,
            True,
            "Senator",
        ),
        (
            "Tim",
            "Scott",
            "Republican",
            "Senate",
            "South Carolina",
            None,
            True,
            "Senator",
        ),
        ("Josh", "Hawley", "Republican", "Senate", "Missouri", None, True, "Senator"),
        ("Tom", "Cotton", "Republican", "Senate", "Arkansas", None, True, "Senator"),
        (
            "John",
            "Thune",
            "Republican",
            "Senate",
            "South Dakota",
            None,
            True,
            "Senator",
        ),
        # Democrats - House
        (
            "Nancy",
            "Pelosi",
            "Democrat",
            "House",
            "California",
            11,
            True,
            "Representative",
        ),
        (
            "Alexandria",
            "Ocasio-Cortez",
            "Democrat",
            "House",
            "New York",
            14,
            True,
            "Representative",
        ),
        (
            "Adam",
            "Schiff",
            "Democrat",
            "House",
            "California",
            30,
            True,
            "Representative",
        ),
        (
            "Eric",
            "Swalwell",
            "Democrat",
            "House",
            "California",
            14,
            True,
            "Representative",
        ),
        (
            "Maxine",
            "Waters",
            "Democrat",
            "House",
            "California",
            43,
            True,
            "Representative",
        ),
        (
            "Jerry",
            "Nadler",
            "Democrat",
            "House",
            "New York",
            12,
            True,
            "Representative",
        ),
        ("Ilhan", "Omar", "Democrat", "House", "Minnesota", 5, True, "Representative"),
        (
            "Rashida",
            "Tlaib",
            "Democrat",
            "House",
            "Michigan",
            12,
            True,
            "Representative",
        ),
        (
            "Ayanna",
            "Pressley",
            "Democrat",
            "House",
            "Massachusetts",
            7,
            True,
            "Representative",
        ),
        (
            "Katie",
            "Porter",
            "Democrat",
            "House",
            "California",
            47,
            True,
            "Representative",
        ),
        (
            "Pramila",
            "Jayapal",
            "Democrat",
            "House",
            "Washington",
            7,
            True,
            "Representative",
        ),
        ("Ro", "Khanna", "Democrat", "House", "California", 17, True, "Representative"),
        ("Jamie", "Raskin", "Democrat", "House", "Maryland", 8, True, "Representative"),
        ("Ted", "Lieu", "Democrat", "House", "California", 36, True, "Representative"),
        (
            "Zoe",
            "Lofgren",
            "Democrat",
            "House",
            "California",
            18,
            True,
            "Representative",
        ),
        # Republicans - House
        (
            "Kevin",
            "McCarthy",
            "Republican",
            "House",
            "California",
            20,
            True,
            "Representative",
        ),
        (
            "Marjorie",
            "Taylor Greene",
            "Republican",
            "House",
            "Georgia",
            14,
            True,
            "Representative",
        ),
        ("Matt", "Gaetz", "Republican", "House", "Florida", 1, True, "Representative"),
        ("Jim", "Jordan", "Republican", "House", "Ohio", 4, True, "Representative"),
        (
            "Steve",
            "Scalise",
            "Republican",
            "House",
            "Louisiana",
            1,
            True,
            "Representative",
        ),
        (
            "Elise",
            "Stefanik",
            "Republican",
            "House",
            "New York",
            21,
            True,
            "Representative",
        ),
        (
            "Lauren",
            "Boebert",
            "Republican",
            "House",
            "Colorado",
            3,
            True,
            "Representative",
        ),
        (
            "Madison",
            "Cawthorn",
            "Republican",
            "House",
            "North Carolina",
            11,
            False,
            "Representative",
        ),
        ("Paul", "Gosar", "Republican", "House", "Arizona", 9, True, "Representative"),
        ("Andy", "Biggs", "Republican", "House", "Arizona", 5, True, "Representative"),
        (
            "Louie",
            "Gohmert",
            "Republican",
            "House",
            "Texas",
            1,
            False,
            "Representative",
        ),
        ("Mo", "Brooks", "Republican", "House", "Alabama", 5, False, "Representative"),
        (
            "Scott",
            "Perry",
            "Republican",
            "House",
            "Pennsylvania",
            10,
            True,
            "Representative",
        ),
        ("Chip", "Roy", "Republican", "House", "Texas", 21, True, "Representative"),
        # Governors
        ("Gavin", "Newsom", "Democrat", None, "California", None, True, "Governor"),
        ("Ron", "DeSantis", "Republican", None, "Florida", None, True, "Governor"),
        ("Greg", "Abbott", "Republican", None, "Texas", None, True, "Governor"),
        ("Gretchen", "Whitmer", "Democrat", None, "Michigan", None, True, "Governor"),
        ("Andrew", "Cuomo", "Democrat", None, "New York", None, False, "Governor"),
        ("Kathy", "Hochul", "Democrat", None, "New York", None, True, "Governor"),
        ("J.B.", "Pritzker", "Democrat", None, "Illinois", None, True, "Governor"),
        ("Kristi", "Noem", "Republican", None, "South Dakota", None, True, "Governor"),
        ("Brian", "Kemp", "Republican", None, "Georgia", None, True, "Governor"),
        ("Glenn", "Youngkin", "Republican", None, "Virginia", None, True, "Governor"),
    ]

    for politician in politicians:
        cursor.execute(
            """
            INSERT INTO pt.Politicians (FirstName, LastName, Party, Chamber, State, District, IsActive, Role)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
            politician,
        )


def seed_bills(cursor):
    """Seed 60 bills with diverse subjects."""
    base_date = date(2022, 1, 1)
    bills = [
        # Healthcare
        (
            "H.R.1",
            "Medicare for All Act",
            base_date,
            118,
            ["Health", "Medicare & Medicaid", "Healthcare Reform"],
        ),
        (
            "H.R.3",
            "Elijah E. Cummings Lower Drug Costs Now Act",
            base_date + timedelta(days=10),
            118,
            ["Health", "Prescription Drugs", "Pharmaceuticals"],
        ),
        (
            "S.1",
            "For the People Act",
            base_date + timedelta(days=15),
            118,
            ["Government Reform", "Voting Rights", "Campaign Finance"],
        ),
        (
            "S.4",
            "John R. Lewis Voting Rights Advancement Act",
            base_date + timedelta(days=20),
            118,
            ["Voting Rights", "Civil Rights", "Elections"],
        ),
        (
            "H.R.5",
            "Equality Act",
            base_date + timedelta(days=25),
            118,
            ["Civil Rights", "LGBTQ Rights", "Discrimination"],
        ),
        # Climate & Energy
        (
            "H.R.9",
            "Climate Action Now Act",
            base_date + timedelta(days=30),
            118,
            ["Environment", "Climate Change", "Energy"],
        ),
        (
            "S.987",
            "Clean Energy for America Act",
            base_date + timedelta(days=35),
            118,
            ["Energy", "Renewable Energy", "Climate"],
        ),
        (
            "H.R.1512",
            "Green New Deal Resolution",
            base_date + timedelta(days=40),
            118,
            ["Climate Change", "Energy", "Jobs"],
        ),
        (
            "S.674",
            "American Clean Energy and Security Act",
            base_date + timedelta(days=45),
            118,
            ["Energy", "Environment", "Climate"],
        ),
        (
            "H.R.763",
            "Energy Innovation and Carbon Dividend Act",
            base_date + timedelta(days=50),
            118,
            ["Climate", "Carbon Tax", "Energy"],
        ),
        # Defense
        (
            "H.R.2500",
            "National Defense Authorization Act",
            base_date + timedelta(days=55),
            118,
            ["Defense", "Military", "National Security"],
        ),
        (
            "S.1790",
            "National Defense Authorization Act",
            base_date + timedelta(days=60),
            118,
            ["Defense", "Military", "Veterans"],
        ),
        (
            "H.R.1585",
            "Military Construction Authorization Act",
            base_date + timedelta(days=65),
            118,
            ["Defense", "Military Construction", "Infrastructure"],
        ),
        (
            "S.1356",
            "Department of Defense Appropriations Act",
            base_date + timedelta(days=70),
            118,
            ["Defense", "Military Spending", "Budget"],
        ),
        (
            "H.R.2740",
            "Defense Production Act",
            base_date + timedelta(days=75),
            118,
            ["Defense", "Manufacturing", "National Security"],
        ),
        # Education
        (
            "H.R.2",
            "College Affordability Act",
            base_date + timedelta(days=80),
            118,
            ["Education", "Higher Education", "Student Loans"],
        ),
        (
            "S.2534",
            "Student Debt Cancellation Act",
            base_date + timedelta(days=85),
            118,
            ["Education", "Student Debt", "Higher Education"],
        ),
        (
            "H.R.865",
            "Public Service Loan Forgiveness Program",
            base_date + timedelta(days=90),
            118,
            ["Education", "Student Loans", "Public Service"],
        ),
        (
            "S.1234",
            "Education Freedom Scholarships Act",
            base_date + timedelta(days=95),
            118,
            ["Education", "School Choice", "Tax Credits"],
        ),
        (
            "H.R.3456",
            "Teacher Recruitment and Retention Act",
            base_date + timedelta(days=100),
            118,
            ["Education", "Teachers", "K-12"],
        ),
        # Finance & Banking
        (
            "H.R.10",
            "Financial CHOICE Act",
            base_date + timedelta(days=105),
            118,
            ["Finance", "Banking", "Regulation"],
        ),
        (
            "S.2155",
            "Economic Growth Act",
            base_date + timedelta(days=110),
            118,
            ["Finance", "Banking", "Economic Policy"],
        ),
        (
            "H.R.4790",
            "Cryptocurrency Regulation Act",
            base_date + timedelta(days=115),
            118,
            ["Finance", "Cryptocurrency", "Regulation"],
        ),
        (
            "S.3571",
            "Banking Reform Act",
            base_date + timedelta(days=120),
            118,
            ["Finance", "Banking", "Consumer Protection"],
        ),
        (
            "H.R.5983",
            "Securities and Exchange Commission Reform Act",
            base_date + timedelta(days=125),
            118,
            ["Finance", "Securities", "Markets"],
        ),
        # Technology
        (
            "H.R.6",
            "American Innovation and Competitiveness Act",
            base_date + timedelta(days=130),
            118,
            ["Technology", "Innovation", "Research"],
        ),
        (
            "S.1260",
            "Endless Frontier Act",
            base_date + timedelta(days=135),
            118,
            ["Technology", "Research", "China Competition"],
        ),
        (
            "H.R.2668",
            "CHIPS and Science Act",
            base_date + timedelta(days=140),
            118,
            ["Technology", "Semiconductors", "Manufacturing"],
        ),
        (
            "S.2992",
            "Data Privacy Act",
            base_date + timedelta(days=145),
            118,
            ["Technology", "Privacy", "Consumer Protection"],
        ),
        (
            "H.R.3684",
            "Infrastructure Investment and Jobs Act",
            base_date + timedelta(days=150),
            118,
            ["Infrastructure", "Technology", "Broadband"],
        ),
        # Immigration
        (
            "H.R.2002",
            "Dream and Promise Act",
            base_date + timedelta(days=155),
            118,
            ["Immigration", "DACA", "Citizenship"],
        ),
        (
            "S.348",
            "Immigration Reform Act",
            base_date + timedelta(days=160),
            118,
            ["Immigration", "Border Security", "Pathway to Citizenship"],
        ),
        (
            "H.R.1603",
            "Farm Workforce Modernization Act",
            base_date + timedelta(days=165),
            118,
            ["Immigration", "Agriculture", "Guest Workers"],
        ),
        (
            "S.2344",
            "Secure and Succeed Act",
            base_date + timedelta(days=170),
            118,
            ["Immigration", "Border Security", "DACA"],
        ),
        (
            "H.R.2214",
            "Asylum Seeker Work Authorization Act",
            base_date + timedelta(days=175),
            118,
            ["Immigration", "Asylum", "Employment"],
        ),
        # Criminal Justice
        (
            "H.R.7120",
            "George Floyd Justice in Policing Act",
            base_date + timedelta(days=180),
            118,
            ["Criminal Justice", "Police Reform", "Civil Rights"],
        ),
        (
            "S.3985",
            "Sentencing Reform Act",
            base_date + timedelta(days=185),
            118,
            ["Criminal Justice", "Sentencing", "Prison Reform"],
        ),
        (
            "H.R.2000",
            "First Step Act",
            base_date + timedelta(days=190),
            118,
            ["Criminal Justice", "Prison Reform", "Recidivism"],
        ),
        (
            "S.756",
            "Marijuana Legalization Act",
            base_date + timedelta(days=195),
            118,
            ["Criminal Justice", "Drug Policy", "Cannabis"],
        ),
        (
            "H.R.3884",
            "Qualified Immunity Reform Act",
            base_date + timedelta(days=200),
            118,
            ["Criminal Justice", "Police", "Civil Rights"],
        ),
        # Labor & Employment
        (
            "H.R.2001",
            "Raise the Wage Act",
            base_date + timedelta(days=205),
            118,
            ["Labor", "Minimum Wage", "Employment"],
        ),
        (
            "S.1242",
            "Protecting the Right to Organize Act",
            base_date + timedelta(days=210),
            118,
            ["Labor", "Unions", "Workers Rights"],
        ),
        (
            "H.R.397",
            "Workplace Violence Prevention Act",
            base_date + timedelta(days=215),
            118,
            ["Labor", "Workplace Safety", "Healthcare"],
        ),
        (
            "S.623",
            "Paid Family Leave Act",
            base_date + timedelta(days=220),
            118,
            ["Labor", "Family Leave", "Employment"],
        ),
        (
            "H.R.1319",
            "American Rescue Plan Act",
            base_date + timedelta(days=225),
            118,
            ["Labor", "Economic Relief", "COVID-19"],
        ),
        # Foreign Relations
        (
            "H.R.256",
            "Israel Security Assistance Support Act",
            base_date + timedelta(days=230),
            118,
            ["Foreign Relations", "Israel", "Defense"],
        ),
        (
            "S.2000",
            "Strategic Competition Act",
            base_date + timedelta(days=235),
            118,
            ["Foreign Relations", "China", "National Security"],
        ),
        (
            "H.R.6395",
            "NATO Support Act",
            base_date + timedelta(days=240),
            118,
            ["Foreign Relations", "NATO", "Defense"],
        ),
        (
            "S.2792",
            "Afghanistan War Powers Resolution",
            base_date + timedelta(days=245),
            118,
            ["Foreign Relations", "Afghanistan", "War Powers"],
        ),
        (
            "H.R.1158",
            "Uyghur Human Rights Policy Act",
            base_date + timedelta(days=250),
            118,
            ["Foreign Relations", "Human Rights", "China"],
        ),
        # Taxation
        (
            "H.R.5376",
            "Build Back Better Act",
            base_date + timedelta(days=255),
            118,
            ["Taxation", "Budget", "Social Programs"],
        ),
        (
            "S.3628",
            "Tax Cuts and Jobs Act",
            base_date + timedelta(days=260),
            118,
            ["Taxation", "Tax Reform", "Economy"],
        ),
        (
            "H.R.1994",
            "SALT Deduction Act",
            base_date + timedelta(days=265),
            118,
            ["Taxation", "State Taxes", "Deductions"],
        ),
        (
            "S.2059",
            "Carried Interest Loophole Elimination Act",
            base_date + timedelta(days=270),
            118,
            ["Taxation", "Hedge Funds", "Tax Reform"],
        ),
        (
            "H.R.4297",
            "Corporate Tax Reform Act",
            base_date + timedelta(days=275),
            118,
            ["Taxation", "Corporate Taxes", "Economy"],
        ),
        # Additional bills to reach 60
        (
            "H.R.8",
            "Bipartisan Background Checks Act",
            base_date + timedelta(days=280),
            118,
            ["Gun Control", "Background Checks", "Public Safety"],
        ),
        (
            "S.42",
            "Stop Dangerous Sanctuary Cities Act",
            base_date + timedelta(days=285),
            118,
            ["Immigration", "Law Enforcement", "Public Safety"],
        ),
        (
            "H.R.299",
            "Blue Water Navy Vietnam Veterans Act",
            base_date + timedelta(days=290),
            118,
            ["Veterans", "Healthcare", "Benefits"],
        ),
        (
            "S.134",
            "Women's Health Protection Act",
            base_date + timedelta(days=295),
            118,
            ["Healthcare", "Reproductive Rights", "Women's Rights"],
        ),
        (
            "H.R.1146",
            "Arctic Cultural and Coastal Plain Protection Act",
            base_date + timedelta(days=300),
            118,
            ["Environment", "Conservation", "Energy"],
        ),
    ]

    for bill in bills:
        cursor.execute(
            """
            INSERT INTO pt.Bills (BillNumber, Title, DateIntroduced, Congress, Subjects)
            VALUES (%s, %s, %s, %s, %s)
        """,
            bill,
        )


def seed_donors(cursor):
    """Seed 60 donors with diverse industries."""
    donors = [
        # Tech Industry
        ("Sundar Pichai", "Individual", "Google", "Technology", "Mountain View", "CA"),
        ("Tim Cook", "Individual", "Apple", "Technology", "Cupertino", "CA"),
        ("Satya Nadella", "Individual", "Microsoft", "Technology", "Redmond", "WA"),
        ("Mark Zuckerberg", "Individual", "Meta", "Internet", "Menlo Park", "CA"),
        ("Elon Musk", "Individual", "Tesla", "Technology", "Austin", "TX"),
        ("Jeff Bezos", "Individual", "Amazon", "Internet", "Seattle", "WA"),
        ("Google LLC", "Corporation", None, "Internet", "Mountain View", "CA"),
        ("Apple Inc", "Corporation", None, "Technology", "Cupertino", "CA"),
        ("Microsoft Corporation", "Corporation", None, "Technology", "Redmond", "WA"),
        ("Meta Platforms", "Corporation", None, "Internet", "Menlo Park", "CA"),
        # Finance & Banking
        ("Jamie Dimon", "Individual", "JPMorgan Chase", "Finance", "New York", "NY"),
        (
            "Brian Moynihan",
            "Individual",
            "Bank of America",
            "Finance",
            "Charlotte",
            "NC",
        ),
        (
            "Charles Scharf",
            "Individual",
            "Wells Fargo",
            "Finance",
            "San Francisco",
            "CA",
        ),
        ("Jane Fraser", "Individual", "Citigroup", "Finance", "New York", "NY"),
        ("David Solomon", "Individual", "Goldman Sachs", "Finance", "New York", "NY"),
        (
            "JPMorgan Chase & Co",
            "Corporation",
            None,
            "Commercial Banks",
            "New York",
            "NY",
        ),
        (
            "Bank of America Corp",
            "Corporation",
            None,
            "Commercial Banks",
            "Charlotte",
            "NC",
        ),
        (
            "Goldman Sachs Group",
            "Corporation",
            None,
            "Securities & Investment",
            "New York",
            "NY",
        ),
        (
            "Morgan Stanley",
            "Corporation",
            None,
            "Securities & Investment",
            "New York",
            "NY",
        ),
        (
            "BlackRock Inc",
            "Corporation",
            None,
            "Securities & Investment",
            "New York",
            "NY",
        ),
        # Healthcare & Pharma
        ("Pfizer Inc", "Corporation", None, "Pharmaceuticals", "New York", "NY"),
        (
            "Johnson & Johnson",
            "Corporation",
            None,
            "Pharmaceuticals",
            "New Brunswick",
            "NJ",
        ),
        ("Merck & Co", "Corporation", None, "Pharmaceuticals", "Rahway", "NJ"),
        ("AstraZeneca", "Corporation", None, "Pharmaceuticals", "Cambridge", "UK"),
        (
            "UnitedHealth Group",
            "Corporation",
            None,
            "Health Services",
            "Minnetonka",
            "MN",
        ),
        ("Anthem Inc", "Corporation", None, "Health Insurance", "Indianapolis", "IN"),
        ("CVS Health", "Corporation", None, "Health Services", "Woonsocket", "RI"),
        (
            "Kaiser Permanente",
            "Corporation",
            None,
            "Hospitals & Nursing Homes",
            "Oakland",
            "CA",
        ),
        (
            "Mayo Clinic",
            "Corporation",
            None,
            "Hospitals & Nursing Homes",
            "Rochester",
            "MN",
        ),
        (
            "Cleveland Clinic",
            "Corporation",
            None,
            "Hospitals & Nursing Homes",
            "Cleveland",
            "OH",
        ),
        # Energy
        ("ExxonMobil", "Corporation", None, "Oil & Gas", "Irving", "TX"),
        ("Chevron Corporation", "Corporation", None, "Oil & Gas", "San Ramon", "CA"),
        ("ConocoPhillips", "Corporation", None, "Oil & Gas", "Houston", "TX"),
        ("Duke Energy", "Corporation", None, "Electric Utilities", "Charlotte", "NC"),
        (
            "NextEra Energy",
            "Corporation",
            None,
            "Electric Utilities",
            "Juno Beach",
            "FL",
        ),
        (
            "Southern Company",
            "Corporation",
            None,
            "Electric Utilities",
            "Atlanta",
            "GA",
        ),
        (
            "Consolidated Edison",
            "Corporation",
            None,
            "Electric Utilities",
            "New York",
            "NY",
        ),
        (
            "Dominion Energy",
            "Corporation",
            None,
            "Electric Utilities",
            "Richmond",
            "VA",
        ),
        # Defense
        ("Lockheed Martin", "Corporation", None, "Defense Aerospace", "Bethesda", "MD"),
        ("Boeing Company", "Corporation", None, "Defense Aerospace", "Chicago", "IL"),
        (
            "Raytheon Technologies",
            "Corporation",
            None,
            "Defense Aerospace",
            "Waltham",
            "MA",
        ),
        (
            "Northrop Grumman",
            "Corporation",
            None,
            "Defense Aerospace",
            "Falls Church",
            "VA",
        ),
        ("General Dynamics", "Corporation", None, "Defense Aerospace", "Reston", "VA"),
        # PACs
        ("ActBlue", "PAC", None, "Democratic", "Somerville", "MA"),
        ("WinRed", "PAC", None, "Republican", "Arlington", "VA"),
        (
            "American Federation of Teachers",
            "PAC",
            None,
            "Labor Unions",
            "Washington",
            "DC",
        ),
        (
            "National Education Association",
            "PAC",
            None,
            "Labor Unions",
            "Washington",
            "DC",
        ),
        (
            "Service Employees International Union",
            "PAC",
            None,
            "Labor Unions",
            "Washington",
            "DC",
        ),
        ("National Rifle Association", "PAC", None, "Gun Rights", "Fairfax", "VA"),
        ("Planned Parenthood", "PAC", None, "Reproductive Rights", "New York", "NY"),
        # Real Estate
        ("Blackstone Group", "Corporation", None, "Real Estate", "New York", "NY"),
        (
            "Brookfield Asset Management",
            "Corporation",
            None,
            "Real Estate",
            "Toronto",
            "ON",
        ),
        (
            "Simon Property Group",
            "Corporation",
            None,
            "Real Estate",
            "Indianapolis",
            "IN",
        ),
        ("Prologis Inc", "Corporation", None, "Real Estate", "San Francisco", "CA"),
        ("Equity Residential", "Corporation", None, "Real Estate", "Chicago", "IL"),
        # Lawyers & Lobbyists
        (
            "Kirkland & Ellis",
            "Corporation",
            None,
            "Lawyers & Lobbyists",
            "Chicago",
            "IL",
        ),
        (
            "Latham & Watkins",
            "Corporation",
            None,
            "Lawyers & Lobbyists",
            "Los Angeles",
            "CA",
        ),
        ("DLA Piper", "Corporation", None, "Lawyers & Lobbyists", "Chicago", "IL"),
        ("Baker McKenzie", "Corporation", None, "Lawyers & Lobbyists", "Chicago", "IL"),
        ("Skadden Arps", "Corporation", None, "Lawyers & Lobbyists", "New York", "NY"),
    ]

    for donor in donors:
        # Extract values: (Name, DonorType, Employer, Industry, City, State)
        # Schema has: (name, donortype, employer, state, industry) - no City column
        name, donortype, employer, industry, _, state = donor
        cursor.execute(
            """
            INSERT INTO pt.Donors (Name, DonorType, Employer, State, Industry)
            VALUES (%s, %s, %s, %s, %s)
        """,
            (name, donortype, employer, state, industry),
        )


def seed_donations(cursor):
    """Seed 70 donations linking donors to politicians."""
    # First, get politician IDs
    cursor.execute(
        "SELECT PoliticianID FROM pt.Politicians ORDER BY PoliticianID LIMIT 30"
    )
    politician_ids = [row[0] for row in cursor.fetchall()]

    # Get donor IDs
    cursor.execute("SELECT DonorID FROM pt.Donors ORDER BY DonorID LIMIT 60")
    donor_ids = [row[0] for row in cursor.fetchall()]

    base_date = date(2022, 1, 1)
    donations = []

    # Create varied donations
    for i in range(70):
        donor_id = donor_ids[i % len(donor_ids)]
        politician_id = politician_ids[i % len(politician_ids)]
        # Vary amounts from $100 to $10,000
        amount = 100 + (i * 137) % 9900
        donation_date = base_date + timedelta(days=i * 5)
        contribution_type = "Individual" if i % 3 == 0 else "PAC/Party"

        donations.append(
            (donor_id, politician_id, amount, donation_date, contribution_type)
        )

    for donation in donations:
        cursor.execute(
            """
            INSERT INTO pt.Donations (DonorID, PoliticianID, Amount, Date, ContributionType)
            VALUES (%s, %s, %s, %s, %s)
        """,
            donation,
        )


def seed_votes(cursor):
    """Seed 80 votes linking politicians to bills."""
    # Get politician IDs (Representatives and Senators)
    cursor.execute(
        "SELECT PoliticianID FROM pt.Politicians WHERE Role IN ('Senator', 'Representative') ORDER BY PoliticianID LIMIT 40"
    )
    politician_ids = [row[0] for row in cursor.fetchall()]

    # Get bill IDs
    cursor.execute("SELECT BillID FROM pt.Bills ORDER BY BillID LIMIT 60")
    bill_ids = [row[0] for row in cursor.fetchall()]

    votes_list = ["Yea", "Nay", "Present", "Not Voting"]
    votes = []

    # Create votes - each bill gets multiple votes from different politicians
    for i in range(80):
        politician_id = politician_ids[i % len(politician_ids)]
        bill_id = bill_ids[i % len(bill_ids)]
        vote = votes_list[i % len(votes_list)]

        votes.append((politician_id, bill_id, vote))

    for vote in votes:
        cursor.execute(
            """
            INSERT INTO pt.Votes (PoliticianID, BillID, Vote)
            VALUES (%s, %s, %s)
        """,
            vote,
        )


def seed_all_data(cursor):
    """Seed all tables with comprehensive test data."""
    seed_politicians(cursor)
    seed_bills(cursor)
    seed_donors(cursor)
    seed_donations(cursor)
    seed_votes(cursor)
