def create_diagnosis_report(
    bug_data,
    triage_result,
    log_result,
    root_cause_result,
    duplicate_result,
    remediation_result
):

    return {
        "bug": bug_data,

        "triage": triage_result,

        "log_analysis": log_result,

        "root_cause": {
            "conclusion": root_cause_result.get(
                "root_cause"
            ),
            "confidence": root_cause_result.get(
                "confidence"
            ),
            "reasoning": root_cause_result.get(
                "reasoning"
            ),
            "supporting_evidence":
                root_cause_result.get(
                    "supporting_evidence",
                    []
                )
        },

        "duplicate_detection": {
            "status": duplicate_result.get(
                "status"
            ),
            "matches": duplicate_result.get(
                "matches",
                []
            )
        },

        "remediation": {
            "recommended_fix":
                remediation_result.get(
                    "recommended_fix"
                ),
            "confidence":
                remediation_result.get(
                    "confidence"
                ),
            "evidence_type":
                remediation_result.get(
                    "evidence_type"
                ),
            "supporting_evidence":
                remediation_result.get(
                    "supporting_evidence",
                    []
                )
        }
    }