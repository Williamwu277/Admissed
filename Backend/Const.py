CHUNK_SIZE = 1000
USE_COLS = ["Year", "Status", "School", "Program", "Average", "Decision Date"]
ID_THRESHOLD = 1000000000
# non-exhaustive AI generated list 
SCHOOL_NICKNAMES = {
    "metropolitan": "Toronto Metropolitan University",
    "met": "Toronto Metropolitan University",
    "scarborough": "University of Toronto (Scarborough Campus)",
    "utsc": "University of Toronto (Scarborough Campus)",
    "uoft sc": "University of Toronto (Scarborough Campus)",
    "uoftsc": "University of Toronto (Scarborough Campus)",
    "mississauga": "University of Toronto (Mississauga Campus)",
    "uoft m": "University of Toronto (Mississauga Campus)",
    "uoftm": "University of Toronto (Mississauga Campus)",
    "utm": "University of Toronto (Mississauga Campus)",
    "toronto": "University of Toronto (St. George Campus)",
    "uoft sg": "University of Toronto (St. George Campus)",
    "uoftsg": "University of Toronto (St. George Campus)",
    "utsg": "University of Toronto (St. George Campus)",
    "uoft": "University of Toronto (St. George Campus)",
    "george": "University of Toronto (St. George Campus)",
    "waterloo": "University of Waterloo",
    "uw": "University of Waterloo",
    "york": "York University",
    "guelph": "University of Guelph",
    "carleton": "Carleton University",
    "western": "Western University",
    "ryerson": "Toronto Metropolitan University",
    "tmu": "Toronto Metropolitan University",
    "trent": "Trent University",
    "uoit": "Ontario Tech University",
    "ontariotech": "Ontario Tech University",
    "tech": "Ontario Tech University",
    "lakehead": "Lakehead University",
    "laurentian": "Laurentian University",
    "wilfrid": "Wilfrid Laurier University",
    "laurier": "Wilfrid Laurier University",
    "brock": "Brock University",
    "wlu": "Wilfrid Laurier University",
    "ubc": "University of British Columbia",
    "ubcv": "University of British Columbia (Vancouver Campus)",
    "ubco": "University of British Columbia (Okanagan Campus)",
    "okanagan": "University of British Columbia (Vancouver Campus)",
    "vancouver": "University of British Columbia (Okanagan Campus)",
    "british columbia": "University of British Columbia (Vancouver Campus)",
    "mcgill": "McGill University",
    "mcgu": "McGill University",
    "master": "McMaster University",
    "queen": "Queen's University",
    "ottawa": "University of Ottawa",
    "mac": "McMaster University",
}
# non-exhaustive AI generated list
PROGRAM_NICKNAMES = {
    "cs": "Computer Science",
    "computer science": "Computer Science",
    "comp eng": "Computer Engineering",
    "comp sci": "Computer Science",
    "rotman": "Rotman Commerce",
    "lifesci": "Life Science",
    "life sci": "Life Science",
    "bio": "Biology",
    "eng sci": "Engineering Science",
    "engsci": "Engineering Science",
    "bioeng": "Biomedical Engineering",
    "bme": "Biomedical Engineering",
    "chem": "Chemistry",
    "mech eng": "Mechanical Engineering",
    "mecheng": "Mechanical Engineering",
    "mechanical": "Mechanical Engineering",
    "ee": "Electrical Engineering",
    "civil eng": "Civil Engineering",
    "syde": "Systems Design Engineering",
    "systems design": "Systems Design Engineering",
    "ce": "Computer Engineering",
    "se": "Software Engineering",
    "software": "Software Engineering",
    "software eng": "Software Engineering",
    "c.s.": "Computer Science",
    "soft eng": "Software Engineering",
    "bio med": "Biomedical Sciences",
    "econ": "Economics",
    "eco": "Economics",
    "psych": "Psychology",
    "phys": "Physics",
    "math": "Mathematics",
    "maths": "Mathematics",
    "arts": "Arts",
    "bfa": "Bachelor of Fine Arts",
    "bba": "Bachelor of Business Administration",
    "mba": "Master of Business Administration",
    "law": "Law",
    "med": "Medicine",
    "nursing": "Nursing",
    "dentistry": "Dentistry",
    "pharm": "Pharmacy",
    "public health": "Public Health",
    "sociology": "Sociology",
    "anthro": "Anthropology",
    "history": "History",
    "ling": "Linguistics",
    "english": "English Literature",
    "theatre": "Theatre Studies",
    "journalism": "Journalism",
    "education": "Education",
    "arch": "Architecture",
    "urban planning": "Urban Planning",
    "environmental science": "Environmental Science",
    "environmental studies": "Environmental Studies",
    "agriculture": "Agriculture",
    "sustainability": "Sustainability",
    "engineering": "Engineering",
    "international relations": "International Relations",
    "communications": "Communications",
    "digital media": "Digital Media",
    "robotics": "Robotics",
    "ai": "Artificial Intelligence",
    "data science": "Data Science",
    "statistics": "Statistics",
    "public policy": "Public Policy",
    "health sciences": "Health Science",
    "genetics": "Genetics",
    "bioinformatics": "Bioinformatics",
    "med tech": "Medical Technology",
    "artsci": "Arts and Science",
    "social work": "Social Work",
    "criminology": "Criminology",
    "hospitality": "Hospitality Management",
    "tourism": "Tourism",
    "philosophy": "Philosophy",
    "mathematical physics": "Mathematical Physics",
    "biochemistry": "Biochemistry",
    "geology": "Geology",
    "geography": "Geography",
    "commerce": "Commerce",
    "gender": "Gender Studies",
    "afm": "Accounting and Financial Management",
    "sfm": "Sustainability and Financial Management",
    "cfm": "Computing and Financial Management",
    "farm": "Financial Analysis and Risk Management",
    "aeo": "Ivey Advanced Entry Opportunity",
    "kin": "Kinesiology",
    "geomatics": "Geomatics",
    "eng": "Engineering",
    "risk": "Financial Analysis and Risk Management",
    "health sci": "Health Science",
    "healthsci": "Health Science",
    "accounting and financial management": "Accounting and Financial Management",
    "gen sci": "Bachelor of Science",
    "schulich": "Schulich",
    "waterloo": "Waterloo",
    "laurier": "Wilfred Laurier",
    "sauder": "Sauder School of Business",
    "accounting": "Accounting"
}