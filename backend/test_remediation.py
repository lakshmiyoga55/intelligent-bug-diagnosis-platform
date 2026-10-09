from agents.root_cause_agent import root_cause_analysis
from agents.duplicate_detection_agent import detect_duplicates
from agents.remediation_agent import generate_remediation


# ============================================================
# CURRENT BUG
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
# ROOT CAUSE
# ============================================================

root_cause_result = root_cause_analysis(bug_data)


# ============================================================
# DUPLICATE DETECTION
# ============================================================

duplicate_result = detect_duplicates(bug_data)


# ============================================================
# REMEDIATION
# ============================================================

remediation_result = generate_remediation(
    bug_data,
    root_cause_result,
    duplicate_result
)


# ============================================================
# DISPLAY
# ============================================================

print("\n===================================")
print("       REMEDIATION ANALYSIS")
print("===================================")

print("\nRecommended Fix:")
print(remediation_result.get("recommended_fix"))

print("\nConfidence:")
print(remediation_result.get("confidence"))

print("\nEvidence Type:")
print(remediation_result.get("evidence_type"))

print("\nSupporting Evidence:")

for evidence in remediation_result.get(
    "supporting_evidence", []
):

    print("\nBug ID:", evidence.get("bug_id"))
    print("Resolution:", evidence.get("resolution"))
    print(
        "Similarity Score:",
        evidence.get("similarity_score")
    )

print("\n===================================")