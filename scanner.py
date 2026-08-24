import re
import joblib

# ==========================================
# CyberShield AI - Load ML Model
# ==========================================

model = joblib.load(
    "model/logistic_phishing_model.pkl"
)

vectorizer = joblib.load(
    "model/logistic_tfidf_vectorizer.pkl"
)


# ==========================================
# Suspicious TLDs
# ==========================================

SUSPICIOUS_TLDS = [
    ".cf",
    ".tk",
    ".ml",
    ".ga",
    ".gq"
]


# ==========================================
# Suspicious Keywords
# ==========================================

SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "verification",
    "secure",
    "account",
    "update",
    "password",
    "signin",
    "bank",
    "payment",
    "confirm"
]


# ==========================================
# Extract Domain
# ==========================================

def extract_domain(url):

    domain = re.sub(
        r"^https?://",
        "",
        url,
        flags=re.IGNORECASE
    )

    if "@" in domain:

        domain = domain.split("@")[-1]

    domain = domain.split("/")[0]

    domain = domain.split(":")[0]

    return domain.lower()


# ==========================================
# Blacklist Check
# ==========================================

def check_blacklist(domain):

    blacklist = [
        "evil.com",
        "phishing.com",
        "malware.com",
        "fakebank.com"
    ]

    return domain in blacklist


# ==========================================
# Scan URL
# ==========================================

def scan_url(url):

    url = url.strip()

    risk_score = 0

    issues = []


    # ======================================
    # URL Validation
    # ======================================

    if url == "":

        return {

            "prediction": "Invalid URL",

            "final_verdict": "INVALID",

            "ml_prediction": "Unknown",

            "ml_probability": 0,

            "ml_confidence": 0,

            "phishing_probability": 0,

            "safe_probability": 0,

            "risk_score": 0,

            "issues": [
                "Please enter a website URL."
            ]

        }


    if not url.startswith(
        ("http://", "https://")
    ):

        return {

            "prediction": "Invalid URL",

            "final_verdict": "INVALID",

            "ml_prediction": "Unknown",

            "ml_probability": 0,

            "ml_confidence": 0,

            "phishing_probability": 0,

            "safe_probability": 0,

            "risk_score": 0,

            "issues": [
                "URL must start with http:// or https://"
            ]

        }


    # ======================================
    # ML Prediction
    # ======================================

    url_features = vectorizer.transform(
        [url]
    )


    ml_prediction = model.predict(
        url_features
    )[0]


    # ======================================
    # ML Probabilities
    # ======================================

    probabilities = model.predict_proba(
        url_features
    )[0]


    # --------------------------------------
    # Class 0 = Safe
    # Class 1 = Phishing
    # --------------------------------------

    safe_probability = float(
        probabilities[0]
    )

    phishing_probability = float(
        probabilities[1]
    )


    # ======================================
    # ML Label
    # ======================================

    if ml_prediction == 1:

        ml_label = "Phishing"

    else:

        ml_label = "Safe"


    # ======================================
    # AI Confidence
    # ======================================

    if ml_label == "Phishing":

        ml_confidence = phishing_probability

    else:

        ml_confidence = safe_probability


    # ======================================
    # Domain
    # ======================================

    domain = extract_domain(
        url
    )


    # ======================================
    # URL Features
    # ======================================

    url_length = len(url)

    dot_count = url.count(".")

    hyphen_count = url.count("-")

    digit_count = sum(
        char.isdigit()
        for char in url
    )

    question_count = url.count("?")

    equal_count = url.count("=")


    # ======================================
    # HTTPS Check
    # ======================================

    if url.startswith("http://"):

        risk_score += 1

        issues.append(
            "Uses HTTP instead of HTTPS"
        )


    # ======================================
    # Blacklist Check
    # ======================================

    if check_blacklist(domain):

        risk_score += 5

        issues.append(
            "Blacklisted Domain"
        )


    # ======================================
    # Suspicious TLD Check
    # ======================================

    for tld in SUSPICIOUS_TLDS:

        if domain.endswith(tld):

            risk_score += 2

            issues.append(
                "Suspicious TLD: " + tld
            )

            break


    # ======================================
    # Suspicious Keyword Check
    # ======================================

    found_keywords = []

    url_lower = url.lower()


    for keyword in SUSPICIOUS_KEYWORDS:

        if keyword in url_lower:

            found_keywords.append(
                keyword
            )


    if found_keywords:

        risk_score += 2

        issues.append(
            "Suspicious Keywords: "
            + ", ".join(found_keywords)
        )


    # ======================================
    # URL Length Check
    # ======================================

    if url_length > 100:

        risk_score += 2

        issues.append(
            "Very Long URL"
        )

    elif url_length > 75:

        risk_score += 1

        issues.append(
            "Long URL"
        )


    # ======================================
    # Subdomain Check
    # ======================================

    if dot_count >= 4:

        risk_score += 1

        issues.append(
            "Too Many Subdomains"
        )


    # ======================================
    # @ Symbol Check
    # ======================================

    if "@" in url:

        risk_score += 2

        issues.append(
            "Contains @ Symbol"
        )


    # ======================================
    # Digit Check
    # ======================================

    if digit_count >= 3:

        risk_score += 1

        issues.append(
            "Contains 3 or More Digits"
        )


    # ======================================
    # IP Address Check
    # ======================================

    ip_pattern = r"\d+\.\d+\.\d+\.\d+"


    if re.search(
        ip_pattern,
        url
    ):

        risk_score += 3

        issues.append(
            "Contains IP Address"
        )


    # ======================================
    # Question Mark Check
    # ======================================

    if question_count > 0:

        risk_score += 1

        issues.append(
            "Contains ? Symbol"
        )


    # ======================================
    # Equal Sign Check
    # ======================================

    if equal_count > 0:

        risk_score += 1

        issues.append(
            "Contains = Symbol"
        )


    # ======================================
    # Rule-Based Prediction
    # ======================================

    if risk_score == 0:

        prediction = "Safe"

    elif risk_score <= 3:

        prediction = "Suspicious"

    else:

        prediction = "High Risk"


    # ======================================
    # Final Verdict
    # ======================================

    if (
        ml_label == "Phishing"
        and phishing_probability >= 0.50
    ):

        final_verdict = "PHISHING"

    elif risk_score >= 4:

        final_verdict = "PHISHING"

    elif phishing_probability >= 0.20:

        final_verdict = "SUSPICIOUS"

    else:

        final_verdict = "SAFE"


    # ======================================
    # Security Analysis
    # ======================================

    security_analysis = {

        "https": (

            "Secure"

            if url.startswith("https://")

            else "Not Secure"
        ),


        "domain_status": (

            "Blacklisted"

            if check_blacklist(domain)

            else "Not Blacklisted"
        ),


        "ip_address": (

            "Detected"

            if re.search(
                ip_pattern,
                url
            )

            else "Not Detected"
        ),


        "suspicious_tld": (

            "Detected"

            if any(
                domain.endswith(tld)
                for tld in SUSPICIOUS_TLDS
            )

            else "Not Detected"
        ),


        "suspicious_keywords": (

            found_keywords

            if found_keywords

            else "None"
        )

    }


    # ======================================
    # AI Analysis
    # ======================================

    ai_analysis = {

        "model":
            "TF-IDF + Logistic Regression",


        "prediction":
            ml_label,


        "confidence":
            round(
                ml_confidence * 100,
                2
            ),


        "phishing_probability":
            round(
                phishing_probability * 100,
                2
            ),


        "safe_probability":
            round(
                safe_probability * 100,
                2
            ),


        "assessment": (

            "AI strongly suspects this URL as phishing"

            if ml_label == "Phishing"

            else
            "AI considers this URL safe"

        )

    }


    # ======================================
    # Risk Breakdown
    # ======================================

    risk_breakdown = {


        "protocol_risk": (

            1

            if url.startswith("http://")

            else 0

        ),


        "domain_risk": (

            5

            if check_blacklist(domain)

            else 0

        ),


        "tld_risk": (

            2

            if any(
                domain.endswith(tld)
                for tld in SUSPICIOUS_TLDS
            )

            else 0

        ),


        "keyword_risk": (

            2

            if found_keywords

            else 0

        ),


        "url_length_risk": (

            2

            if url_length > 100

            else

            1

            if url_length > 75

            else 0

        ),


        "subdomain_risk": (

            1

            if dot_count >= 4

            else 0

        ),


        "special_character_risk": (

            (2 if "@" in url else 0)

            +

            (1 if question_count > 0 else 0)

            +

            (1 if equal_count > 0 else 0)

        ),


        "digit_risk": (

            1

            if digit_count >= 3

            else 0

        ),


        "ip_risk": (

            3

            if re.search(
                ip_pattern,
                url
            )

            else 0

        )

    }


    # ======================================
    # Return Result
    # ======================================

    return {

        # Rule prediction
        "prediction":
            prediction,


        # Final verdict
        "final_verdict":
            final_verdict,


        # ML prediction
        "ml_prediction":
            ml_label,


        # ----------------------------------
        # Probability Values
        # ----------------------------------

        # Phishing probability
        "ml_probability":
            round(
                phishing_probability * 100,
                2
            ),


        # AI confidence
        "ml_confidence":
            round(
                ml_confidence * 100,
                2
            ),


        # Explicit probabilities
        "phishing_probability":
            round(
                phishing_probability * 100,
                2
            ),


        "safe_probability":
            round(
                safe_probability * 100,
                2
            ),


        # Risk
        "risk_score":
            risk_score,


        # Issues
        "issues":
            issues,


        # URL information
        "domain":
            domain,


        "url_length":
            url_length,


        "dot_count":
            dot_count,


        "hyphen_count":
            hyphen_count,


        "digit_count":
            digit_count,


        "question_count":
            question_count,


        "equal_count":
            equal_count,


        # Security Analysis
        "security_analysis":
            security_analysis,


        # AI Analysis
        "ai_analysis":
            ai_analysis,


        # Risk Breakdown
        "risk_breakdown":
            risk_breakdown

    }