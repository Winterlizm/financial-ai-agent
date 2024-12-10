EXPENSE_CATEGORIES = {
    "הוצאות_ישירות": {
        "sub_categories": {
            "חומרים": [],
            "משלוחים": [],
            "אריזות": [],
            "קבלני משנה - ישיר": [],
            "עובדים - ישיר": []
        },
        "keywords": ["חומר גלם", "משלוח", "שליח", "אריזה", "קבלן"]
    },
    "שיווק_ומכירות": {
        "sub_categories": {
            "ממומן": ["פייסבוק", "גוגל", "מטא"],
            "ייעוצים שיווקיים": [],
            "קמפיינר": [],
            "הוצאות שיווק אחרות": [],
            "מיתוג": []
        }
    },
    "הנהלה_וכלליות": {
        "sub_categories": {
            "משרד": ["ארנונה", "חשמל", "מים", "שכירות"],
            "מקצועי": ["רו\"ח", "עו\"ד", "ייעוץ"],
            "תוכנות": ["זום", "מייקרוסופט", "גוגל"],
            "ביטוח": ["ביטוח עסק", "אחריות מקצועית"],
            "רכב": ["דלק", "ליסינג", "ביטוח רכב"],
            "עמלות": ["עמלת סליקה", "עמלת ניכיון", "עמלות בנק"]
        }
    }
}

SPECIAL_CREDITS = {
    "החזרים_ותקבולים_מיוחדים": {
        "ביטוח_לאומי": [
            "ב\"ל מילואי",
            "דמי לידה",
            "דמי אבטלה",
            "נפגעי עבודה",
            "מענק קורונה",
            "בטוח לאומי",
            "ביטוח לאומי",
            "ב.לאומי",
            "ב\"ל"
        ],
        "הכנסות_מימון": [
            "פרעון פקדון",
            "ריבית מפקדון",
            "ריבית זכות"
        ],
        "החזרי_מס": [
            "החזר מס הכנס",
            "זיכוי ממס"
        ]
    }
}

def normalize_text(text: str) -> str:
    """
    מנרמל טקסט להשוואה - מסיר תווים מיוחדים ורווחים מיותרים
    """
    replacements = {
        "\"": "",
        "'": "",
        ".": "",
        "-": " ",
        "_": " "
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return " ".join(text.lower().split())

def classify_transaction(description: str, amount: float, is_credit: bool = False) -> tuple[str, str]:
    """
    מסווג תנועה לקטגוריה ראשית ותת-קטגוריה
    returns: (main_category, sub_category)
    """
    normalized_desc = normalize_text(description)
    
    # בדיקה אם זה תקבול מיוחד
    if is_credit:
        for main_cat, sub_cats in SPECIAL_CREDITS.items():
            for sub_cat, keywords in sub_cats.items():
                if any(normalize_text(k) in normalized_desc for k in keywords):
                    return main_cat, sub_cat
    
    # בדיקת הוצאות
    for main_cat, data in EXPENSE_CATEGORIES.items():
        # בדיקת מילות מפתח כלליות לקטגוריה
        if "keywords" in data and any(k in normalized_desc for k in data["keywords"]):
            return main_cat, "כללי"
            
        # בדיקת תת-קטגוריות
        for sub_cat, keywords in data["sub_categories"].items():
            if any(normalize_text(k) in normalized_desc for k in keywords):
                return main_cat, sub_cat
    
    return "לא מסווג", "דורש בדיקה"