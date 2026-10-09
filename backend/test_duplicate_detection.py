from agents.duplicate_detection_agent import detect_duplicates


# ============================================================
# DUPLICATE TEST BUG
# ============================================================

bug_data = {
    "bug_description": "When the user enters valid login details, the application crashes.",
    "severity": "High",
    "priority": "P1",
    "affected_component": "Authentication/Login",
    "exception_type": "NullPointerException",
    "error_message": "Authentication failed",
    "failure_point": "LoginService.authenticate()",
    "code_path": "LoginController -> LoginService"
}


# ============================================================
# RUN DUPLICATE DETECTION AGENT
# ============================================================

result = detect_duplicates(bug_data)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n===================================")
print("     DUPLICATE DETECTION")
print("===================================")

print("\nOverall Status:")
print(result.get("status"))

print("\nMatching Historical Bugs:")

matches = result.get("matches", [])

if not matches:

    print("\nNo similar historical bugs found.")

else:

    for match in matches:

        print("\nBug ID:", match.get("bug_id"))
        print("Status:", match.get("status"))
        print("Similarity Score:", match.get("similarity_score"))
        print("Description:", match.get("description"))
        print("Resolution:", match.get("resolution"))

print("\n===================================")