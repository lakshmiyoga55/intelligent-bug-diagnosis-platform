from agents.root_cause_agent import root_cause_analysis


# Sample bug
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


# Run Root Cause Agent
result = root_cause_analysis(bug_data)


print("\n===================================")
print("       ROOT CAUSE ANALYSIS")
print("===================================")

print("\nRoot Cause:")
print(result.get("root_cause"))

print("\nConfidence:")
print(result.get("confidence"))

print("\nReasoning:")
print(result.get("reasoning"))

print("\nSupporting Evidence:")

for evidence in result.get("supporting_evidence", []):

    print("\nBug ID:", evidence.get("bug_id"))
    print("Description:", evidence.get("description"))
    print("Resolution:", evidence.get("resolution"))

print("\n===================================")