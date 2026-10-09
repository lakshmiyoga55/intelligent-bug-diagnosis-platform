import json
import sys
import os

# Allow this file to work both:
# 1. From project root
# 2. Directly from backend folder

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.defect_retriever import retrieve_relevant_defects
from backend.agents.duplicate_detection_agent import detect_duplicates
from backend.agents.root_cause_agent import root_cause_analysis
from backend.agents.remediation_agent import generate_remediation


TEST_FILE = os.path.join(
    PROJECT_ROOT,
    "backend",
    "test_bugs.json"
)


def run_m4_tests():

    with open(TEST_FILE, "r", encoding="utf-8") as file:
        bugs = json.load(file)

    all_results = []

    for bug in bugs:

        print("\n========================================")
        print(f"TESTING: {bug['bug_id']}")
        print("========================================")

        print("\nBug:")
        print(bug["bug_description"])

        # ========================================
        # 1. RAG / KNOWLEDGE BASE RETRIEVAL
        # ========================================

        retrieved = retrieve_relevant_defects(bug)

        print("\n--- Retrieved Evidence ---")

        if retrieved:

            for defect in retrieved[:3]:

                print(
                    defect["bug_id"],
                    "| Score:",
                    round(defect["similarity_score"], 4),
                    "| Percentage:",
                    f'{defect["similarity_percentage"]:.2f}%'
                )

        else:
            print("No historical evidence found.")

        # ========================================
        # 2. DUPLICATE DETECTION
        # ========================================

        duplicate_result = detect_duplicates(bug)

        print("\n--- Duplicate Detection ---")

        print(
            "Status:",
            duplicate_result.get("status", "Unknown")
        )

        for match in duplicate_result.get("matches", [])[:3]:

            print(
                match.get("bug_id", "Unknown"),
                "|",
                match.get("status", "Unknown"),
                "| Score:",
                round(match.get("similarity_score", 0), 4)
            )

        # ========================================
        # 3. ROOT CAUSE ANALYSIS
        # ========================================

        root_cause_result = root_cause_analysis(bug)

        print("\n--- Root Cause ---")

        print(
            "Conclusion:",
            root_cause_result.get(
                "root_cause",
                "Insufficient Evidence"
            )
        )

        print(
            "Confidence:",
            root_cause_result.get(
                "confidence",
                0
            )
        )

        # ========================================
        # 4. REMEDIATION
        # ========================================

        remediation_result = generate_remediation(
            bug,
            root_cause_result,
            duplicate_result
        )

        print("\n--- Remediation ---")

        print(
            "Recommendation:",
            remediation_result.get(
                "recommended_fix",
                "Insufficient Evidence"
            )
        )

        print(
            "Confidence:",
            remediation_result.get(
                "confidence",
                0
            )
        )

        # ========================================
        # SAVE RESULT
        # ========================================

        test_result = {
            "test_bug_id": bug["bug_id"],
            "retrieved_evidence": retrieved[:3],
            "duplicate_status": duplicate_result.get(
                "status",
                "Unknown"
            ),
            "root_cause": root_cause_result.get(
                "root_cause",
                "Insufficient Evidence"
            ),
            "root_cause_confidence": root_cause_result.get(
                "confidence",
                0
            ),
            "recommended_fix": remediation_result.get(
                "recommended_fix",
                "Insufficient Evidence"
            ),
            "remediation_confidence": remediation_result.get(
                "confidence",
                0
            )
        }

        all_results.append(test_result)

    return all_results


if __name__ == "__main__":

    results = run_m4_tests()

    print("\n")
    print("========================================")
    print("M4 END-TO-END TEST COMPLETED")
    print("========================================")

    print(
        f"Total test bugs: {len(results)}"
    )

    print("\nSummary:")

    for result in results:

        print(
            result["test_bug_id"],
            "| Duplicate:",
            result["duplicate_status"],
            "| Root Cause:",
            result["root_cause"],
            "| Fix:",
            result["recommended_fix"]
        )

    print("\n========================================")