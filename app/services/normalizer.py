import re

# =============================================================================
#  SYNONYMS — maps user query variants → canonical keyword
#  Format: "canonical_key": ["variant1", "variant2", ...]
#  Normalizer replaces ALL variants with the canonical key before matching.
# =============================================================================

SYNONYMS = {

    # ── PROGRAM / COURSE NAMES ────────────────────────────────────────────────
    "btech": [
        "b.tech", "b tech", "b.tech.", "bachelor of technology",
        "bachelor in technology", "btech", "undergraduate engineering",
        "ug engineering", "bachelors in engineering", "b tech course",
        "btech program", "b.tech degree", "be", "b.e",
    ],
    "cse": [
        "computer science", "computer science engineering",
        "computer science & engineering", "cs engineering",
        "computer engineering", "it engineering", "computer sci",
        "cs & it", "computer science and engineering",
    ],
    "aiml": [
        "ai", "ml", "ai & ml", "ai and ml", "ai-ml",
        "artificial intelligence", "machine learning",
        "artificial intelligence and machine learning",
        "deep learning", "neural networks", "ai engineering",
    ],
    "ece": [
        "electronics", "communication", "electronics and communication",
        "electronics & communication", "ec", "eee",
        "electrical electronics", "electronics engineering",
    ],
    "me": [
        "mechanical", "mechanical engineering", "mech",
        "mech engineering", "mech engg",
    ],
    "civil": [
        "civil engineering", "civil engg", "construction",
    ],
    "bca": [
        "bachelor of computer applications", "b.c.a", "bca course",
    ],
    "bba": [
        "bachelor of business administration", "b.b.a", "bba course",
    ],
    "mba": [
        "master of business administration", "m.b.a", "mba program",
        "masters in management", "pgdm",
    ],
    "mca": [
        "master of computer applications", "m.c.a", "mca program",
        "masters in computer applications",
    ],

    # ── FEES / COSTS ──────────────────────────────────────────────────────────
    "fee": [
        "fees", "cost", "charges", "tuition", "tuition fee", "tuition fees",
        "fee structure", "annual fees", "course fees", "total fees",
        "admission fees", "college fees", "btech fees", "engineering fees",
        "hostel fees", "total cost", "per year fees", "semester fees",
        "affordable fees", "low fees", "fee details", "kitna",
    ],

    # ── PLACEMENT ─────────────────────────────────────────────────────────────
    "placement": [
        "placements", "placement record", "job placements",
        "campus placement", "recruitment", "job opportunities",
        "highest package", "average package", "salary package",
        "placement percentage", "placement rate", "top recruiters",
        "companies visiting", "placement cell", "training and placement",
        "highest salary", "average salary", "placement statistics",
        "placement 2024", "placement 2025", "placement 2026",
        "job offers", "lpa", "package", "offer letter",
    ],

    # ── CAMPUS / ENVIRONMENT ──────────────────────────────────────────────────
    "campus": [
        "campus life", "infrastructure", "facilities", "facility",
        "environment", "hostel", "labs", "laboratories", "library",
        "sports facilities", "gym", "canteen", "mess", "hostel facilities",
        "campus environment", "college campus", "modern infrastructure",
        "smart classrooms", "college facilities", "auditorium",
        "swimming pool", "playground", "rooma",
    ],

    # ── ACHIEVEMENTS / RANKINGS ───────────────────────────────────────────────
    "achievement": [
        "achievements", "rankings", "awards", "accreditation",
        "naac", "iso certified", "top ranked", "best engineering college",
        "ranking in up", "top private college", "emerging institute",
        "hackathon wins", "student achievements", "college ranking",
        "best in kanpur", "15 years", "drdo", "hackshodh",
    ],

    # ── SCHOLARSHIPS ──────────────────────────────────────────────────────────
    "scholarship": [
        "scholarships", "financial aid", "up scholarship",
        "national scholarship", "nsp", "gov scholarship",
        "fee waiver", "merit scholarship", "stipend",
    ],

    # ── ADMISSION ─────────────────────────────────────────────────────────────
    "admission": [
        "admissions", "admission process", "admission open",
        "admission enquiry", "cutoff", "eligibility",
        "entrance exam", "aktu admission", "btech admission",
        "direct admission", "apply", "application",
    ],

    # ── COLLEGE / INSTITUTE ───────────────────────────────────────────────────
    "college": [
        "institute", "university", "engineering college",
        "private college", "private engineering college",
        "private institute", "best college", "top college",
        "engineering institute", "technical institute", "btech college",
        "aktu affiliated college", "aktu college", "kanpur college",
        "kanpur engineering college", "private university",
        "group of institutions", "education group",
        "allenhouse group", "superhouse group", "allenhouse",
        "ait", "aim", "superhouse",
    ],

    # ── HOD / HEAD OF DEPARTMENT ──────────────────────────────────────────────
    "hod": [
        "head of department", "head of dept", "department head",
        "h o d", "dept head", "faculty head", "incharge",
        "in charge", "head", "hod bca", "hod bba", "hod mba",
        "hod cse", "hod ece", "hod me", "hod civil",
        "bca hod", "bba hod", "mba hod", "cse hod",
        "ece hod", "mechanical hod", "civil hod",
        "who is hod", "hod of",
    ],

    # ── FACULTY / STAFF ROLES ─────────────────────────────────────────────────
    "faculty": [
        "faculties", "professor", "professors", "teacher", "teachers",
        "staff", "lecturer", "teaching staff", "assistant professor",
        "associate professor", "faculty member",
    ],
    "dean": [
        "dean academics", "dean student welfare", "dean research",
        "academic dean", "student welfare", "research dean",
    ],
    "chairman": [
        "chairperson", "chief", "top authority", "head of institution",
        "who runs", "who leads", "founder",
    ],
    "director": [
        "director engineering", "director administration",
        "additional director", "institutional director",
    ],

    # ── PERSON NAMES — MANAGEMENT ─────────────────────────────────────────────
    "mukhtarul": ["mukhtarul amin", "amin", "mukhtar"],
    "manoj": ["manoj misra", "manoj kumar misra", "prof misra"],
    "rubby": ["rubby chawla", "dr chawla", "dr rubby"],
    "atul": ["atul chaturvedi", "prof chaturvedi", "prof atul"],

    # ── PERSON NAMES — FACULTY / HOD ─────────────────────────────────────────
    "bharat": ["bharat tripathi", "dr bharat", "dr tripathi", "tripathi"],
    "shishir": ["shishir gupta", "dr shishir", "dr gupta"],
    "azharuddin": ["dr azharuddin", "azhar"],
    "sudhir": ["sudhir singh", "dr sudhir", "dr singh sudhir"],
    "praneet": ["praneet madhav", "mr praneet", "mr madhav"],
    "mayank": ["mayank maheshwari", "dr mayank", "dr maheshwari"],
    "rajeev": ["rajeev sachan", "rajeev kumar sachan", "dr rajeev", "dr sachan"],
    "saurabh": ["saurabh shukla", "mr saurabh", "mr shukla"],
    "sudha": ["sudha dhawan", "dr sudha", "dr dhawan"],
    "varun": ["varun shukla", "dr varun", "dr varun shukla"],
    "shashwat": ["shashwat mishra", "mr shashwat", "mr mishra"],
    "kawaljeet": ["kawaljeet kaur", "ms kawaljeet", "ms kaur"],

    # ── PERSON NAMES — PLACEMENT STAFF ────────────────────────────────────────
    "lalit": ["lalit kumar", "mr lalit", "mr lalit kumar"],
    "ruchi": ["ruchi tiwari", "ms ruchi", "ms tiwari"],

    # ── CONTACT / PHONE ───────────────────────────────────────────────────────
    "contact": [
        "phone", "number", "call", "helpline", "telephone",
        "mobile", "reach", "contact number", "admission cell",
        "office number", "8127405222", "8127505222",
    ],

    # ── EVENTS ────────────────────────────────────────────────────────────────
    "event": [
        "events", "fest", "festival", "hackathon", "exuberance",
        "cultural", "techno", "sports", "annual fest", "seminar",
        "workshop", "conference", "ichis", "budget pe charcha",
    ],

    # ── COURSES GENERAL ───────────────────────────────────────────────────────
    "courses": [
        "course", "programs", "branches", "streams",
        "specializations", "degree", "academic programs",
        "curriculum", "all courses", "available courses",
    ],
}

# =============================================================================
#  STOP WORDS — filtered out before scoring
# =============================================================================

STOP_WORDS = {
    "is", "the", "a", "an", "of", "and", "in", "to", "for",
    "with", "on", "at", "by", "from", "who", "what", "where",
    "when", "why", "how", "are", "am", "it", "this", "that",
    "these", "those", "tell", "me", "about", "can", "you",
    "give", "details", "please", "know", "want", "was", "has",
    "have", "do", "does", "did", "its", "their", "our", "your",
    "which", "any", "some", "get", "info", "information",
}


# =============================================================================
#  NORMALIZE
# =============================================================================

def normalize(text: str) -> str:
    text = text.lower()
    # Keep alphanumerics, spaces, & (for AI&ML etc.)
    text = re.sub(r"[^a-z0-9\s&]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    # Replace synonym variants with canonical key (longest match first)
    all_variants = []
    for key, variants in SYNONYMS.items():
        for val in variants:
            all_variants.append((val, key))
    # Sort by length descending so longer phrases are replaced first
    all_variants.sort(key=lambda x: -len(x[0]))

    for val, key in all_variants:
        pattern = r"\b" + re.escape(val) + r"\b"
        if re.search(pattern, text):
            text = re.sub(pattern, key, text)

    # Remove stop words
    words = text.split()
    filtered = [w for w in words if w not in STOP_WORDS]

    return " ".join(filtered)
