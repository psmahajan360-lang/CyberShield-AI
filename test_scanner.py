from scanner import scan_url


def show_result(url):

    result = scan_url(url)

    # ==========================================
    # Basic URL Information
    # ==========================================

    domain = result.get("domain", "")

    url_length = result.get("url_length", len(url))

    digit_count = result.get("digit_count", 0)

    # ==========================================
    # Advanced Feature Calculation
    # ==========================================

    # Domain length
    domain_length = len(domain)

    # Subdomain count
    domain_parts = domain.split(".")

    if len(domain_parts) > 2:
        subdomain_count = len(domain_parts) - 2
    else:
        subdomain_count = 0

    # Path depth
    clean_url = url.split("://", 1)[-1]

    if "/" in clean_url:
        path = clean_url.split("/", 1)[1]
        path = path.split("?", 1)[0]

        if path:
            path_depth = len(
                [part for part in path.split("/") if part]
            )
        else:
            path_depth = 0
    else:
        path_depth = 0

    # Digit ratio
    if url_length > 0:
        digit_ratio = digit_count / url_length
    else:
        digit_ratio = 0

    # HTTPS status
    if url.lower().startswith("https://"):
        https_status = "YES"
    else:
        https_status = "NO"

    # ==========================================
    # Result Header
    # ==========================================

    print("\n===================================")
    print("       CyberShield AI Result")
    print("===================================")

    print("\nURL:", url)

    # ==========================================
    # ML ANALYSIS
    # ==========================================

    print("\n-----------------------------------")
    print("          ML ANALYSIS")
    print("-----------------------------------")

    print("ML Prediction   :", result["ml_prediction"])
    print("ML Confidence   :", result["ml_probability"], "%")

    # ==========================================
    # URL FEATURE ANALYSIS
    # ==========================================

    print("\n-----------------------------------")
    print("       URL FEATURE ANALYSIS")
    print("-----------------------------------")

    print("Domain          :", domain)
    print("URL Length      :", url_length)
    print("Dots            :", result.get("dot_count", 0))
    print("Hyphens         :", result.get("hyphen_count", 0))
    print("Digits          :", digit_count)
    print("Question Marks  :", result.get("question_count", 0))
    print("Equal Signs     :", result.get("equal_count", 0))

    # ==========================================
    # ADVANCED SECURITY FEATURES
    # ==========================================

    print("\n-----------------------------------")
    print("      URL SECURITY FEATURES")
    print("-----------------------------------")

    print("Domain Length   :", domain_length)
    print("Subdomains      :", subdomain_count)
    print("Path Depth      :", path_depth)
    print("Digit Ratio     :", round(digit_ratio, 2))
    print("HTTPS           :", https_status)

    # ==========================================
    # RULE ANALYSIS
    # ==========================================

    print("\n-----------------------------------")
    print("         RULE ANALYSIS")
    print("-----------------------------------")

    print("Rule Prediction :", result["prediction"])
    print("Risk Score      :", result["risk_score"])

    # Risk Level
    if result["risk_score"] >= 6:

        risk_level = "HIGH RISK"

    elif result["risk_score"] >= 3:

        risk_level = "MEDIUM RISK"

    else:

        risk_level = "LOW RISK"

    print("Risk Level      :", risk_level)

    print("Issues Detected :", len(result["issues"]))

    # ==========================================
    # DETECTED THREATS
    # ==========================================

    if result["issues"]:

        print("\nDetected Threats:")

        for index, issue in enumerate(
            result["issues"],
            start=1
        ):

            print(f"{index}. {issue}")

    else:

        print("\nDetected Threats: None")

    # ==========================================
    # FINAL VERDICT
    # ==========================================

    print("\n-----------------------------------")
    print("          FINAL VERDICT")
    print("-----------------------------------")

    print(
        "Final Verdict:",
        result["final_verdict"]
    )

    if result["final_verdict"] == "PHISHING":

        print(
            "WARNING: This URL appears to be dangerous."
        )

    elif result["final_verdict"] == "SUSPICIOUS":

        print(
            "CAUTION: This URL shows suspicious characteristics."
        )

    elif result["final_verdict"] == "INVALID":

        print(
            "ERROR: Invalid URL."
        )

    else:

        print(
            "SAFE: This URL appears to be safe."
        )

    print("===================================")


# ==========================================
# CyberShield AI URL Scanner
# ==========================================

print("===================================")
print("     CyberShield AI URL Scanner")
print("===================================")


while True:

    url = input(
        "\nEnter URL (or type 'exit' to stop): "
    )

    if url.strip().lower() == "exit":

        print(
            "\nCyberShield AI Scanner stopped."
        )

        break

    show_result(url)