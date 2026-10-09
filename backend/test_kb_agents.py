from backend.defect_retriever import retrieve_relevant_defects
from backend.agents.root_cause_agent import root_cause_analysis
from backend.agents.duplicate_detection_agent import detect_duplicates
from backend.agents.remediation_agent import generate_remediation


def main():

    bug_data = {
        "bug_id": "BUG-107",
        "bug_title": "Search fails for empty keyword",
        "bug_description": "Search fails when the user enters an empty keyword.",
        "affected_component": "Search",
        "component": "Search",
        "exception_type": "IllegalArgumentException",
        "severity": "Medium",
        "priority": "P2",
        "root_cause": "Empty search input was not validated.",
        "resolution": "Added validation to reject empty search keywords.",
        "confirmed_fix": (
            "Validated the fix by testing empty, valid, "
            "and boundary search inputs successfully."
        )
    }

    print("\n==============================================")
    print("       M4.2 - THREE AGENT KB VERIFICATION")
    print("==============================================")

    # -------------------------------------------------
    # 1. ROOT CAUSE AGENT
    # -------------------------------------------------

    print("\n[1] ROOT CAUSE AGENT")
    print("----------------------------------------------")

    root_cause_result = root_cause_analysis(bug_data)

    root_evidence = root_cause_result.get(
        "supporting_evidence",
        []
    )

    root_found = any(
        item.get("bug_id") == "BUG-107"
        for item in root_evidence
    )

    print("Root Cause:")
    print(root_cause_result.get("root_cause"))

    print("Evidence:")

    for item in root_evidence:
        print(
            f"  {item.get('bug_id')} -> "
            f"{item.get('similarity_score', 0)}"
        )

    if root_found:
        print("RESULT: PASS - BUG-107 retrieved")
    else:
        print("RESULT: FAIL - BUG-107 not retrieved")

    # -------------------------------------------------
    # 2. DUPLICATE DETECTION AGENT
    # -------------------------------------------------

    print("\n[2] DUPLICATE DETECTION AGENT")
    print("----------------------------------------------")

    duplicate_result = detect_duplicates(bug_data)

    duplicate_matches = duplicate_result.get(
        "matches",
        []
    )

    duplicate_found = any(
        item.get("bug_id") == "BUG-107"
        for item in duplicate_matches
    )

    print("Duplicate Status:")
    print(duplicate_result.get("status"))

    print("Matches:")

    for item in duplicate_matches:
        print(
            f"  {item.get('bug_id')} -> "
            f"{item.get('similarity_score', 0)}"
        )

    if duplicate_found:
        print("RESULT: PASS - BUG-107 retrieved")
    else:
        print("RESULT: FAIL - BUG-107 not retrieved")

    # -------------------------------------------------
    # 3. REMEDIATION AGENT
    # -------------------------------------------------

    print("\n[3] REMEDIATION AGENT")
    print("----------------------------------------------")

    remediation_result = generate_remediation(
        bug_data,
        root_cause_result,
        duplicate_result
    )

    remediation_evidence = remediation_result.get(
        "supporting_evidence",
        []
    )

    remediation_found = any(
        item.get("bug_id") == "BUG-107"
        for item in remediation_evidence
    )

    print("Recommended Fix:")
    print(
        remediation_result.get(
            "recommended_fix"
        )
    )

    print("Evidence:")

    for item in remediation_evidence:
        print(
            f"  {item.get('bug_id')} -> "
            f"{item.get('resolution')}"
        )

    if remediation_found:
        print("RESULT: PASS - BUG-107 retrieved")
    else:
        print("RESULT: FAIL - BUG-107 not retrieved")

    # -------------------------------------------------
    # FINAL RESULT
    # -------------------------------------------------

    print("\n==============================================")
    print("             FINAL M4.2 RESULT")
    print("==============================================")

    passed = sum([
        root_found,
        duplicate_found,
        remediation_found
    ])

    print(
        f"Agents Passed: {passed}/3"
    )

    if passed == 3:
        print("\nM4.2 THREE-AGENT KB RETRIEVAL: PASSED")
        print("BUG-107 is accessible to all three agents.")
    else:
        print("\nM4.2 THREE-AGENT KB RETRIEVAL: INCOMPLETE")

    print("==============================================")


if __name__ == "__main__":
    main()