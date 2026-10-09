from backend.defect_retriever import retrieve_relevant_defects


def generate_remediation(
    bug_data,
    root_cause_result,
    duplicate_result
):

    # ------------------------------------------------
    # Retrieve historical defects
    # ------------------------------------------------

    historical_defects = retrieve_relevant_defects(
        bug_data
    )

    if not historical_defects:

        return {
            "recommended_fix": "Insufficient Evidence",
            "confidence": 0,
            "evidence_type": "None",
            "supporting_evidence": []
        }

    # ------------------------------------------------
    # Prefer exact bug ID when available
    # ------------------------------------------------

    target_bug_id = bug_data.get(
        "bug_id"
    )

    selected_defect = None

    if target_bug_id:

        for defect in historical_defects:

            if defect.get("bug_id") == target_bug_id:

                selected_defect = defect
                break

    # ------------------------------------------------
    # Otherwise use highest similarity
    # ------------------------------------------------

    if selected_defect is None:

        selected_defect = max(
            historical_defects,
            key=lambda defect: float(
                defect.get(
                    "similarity_score",
                    0
                )
            )
        )

    # ------------------------------------------------
    # Get information
    # ------------------------------------------------

    root_cause = root_cause_result.get(
        "root_cause",
        "Unknown"
    )

    duplicate_status = duplicate_result.get(
        "status",
        "New"
    )

    bug_id = selected_defect.get(
        "bug_id",
        "Unknown"
    )

    resolution = selected_defect.get(
        "resolution",
        ""
    )

    confirmed_fix = selected_defect.get(
        "confirmed_fix",
        ""
    )

    similarity_score = float(
        selected_defect.get(
            "similarity_score",
            0
        )
    )

    # ------------------------------------------------
    # Generate recommendation
    # ------------------------------------------------

    if duplicate_status == "Duplicate":

        recommended_fix = (
            f"Apply the historical resolution used for "
            f"{bug_id}: {resolution}"
        )

        confidence = 0.90

        evidence_type = "Historical Resolution"

    elif duplicate_status == "Related":

        recommended_fix = (
            f"Consider the historical resolution from "
            f"{bug_id}: {resolution}. "
            f"Validate it against the current root cause "
            f"before applying."
        )

        confidence = 0.75

        evidence_type = "Historical Resolution"

    else:

        recommended_fix = (
            f"Use the historical resolution from "
            f"{bug_id} as a reference: {resolution}. "
            f"Further investigation is required before "
            f"applying the fix."
        )

        confidence = 0.50

        evidence_type = "Historical Reference"

    # ------------------------------------------------
    # Return structured result
    # ------------------------------------------------

    return {

        "recommended_fix":
            recommended_fix,

        "confidence":
            confidence,

        "evidence_type":
            evidence_type,

        "root_cause_used":
            root_cause,

        "supporting_evidence": [

            {
                "bug_id":
                    bug_id,

                "resolution":
                    resolution,

                "confirmed_fix":
                    confirmed_fix,

                "similarity_score":
                    similarity_score,

                "approval_status":
                    selected_defect.get(
                        "approval_status",
                        ""
                    )
            }
        ]
    }