from backend.defect_retriever import retrieve_relevant_defects


def detect_duplicates(bug_data):
    """
    Detect whether a submitted bug is:
    - Duplicate
    - Related
    - New

    Uses embedding-based semantic retrieval.
    """

    relevant_defects = retrieve_relevant_defects(bug_data)

    if not relevant_defects:
        return {
            "status": "New",
            "matches": [],
            "explanation": (
                "No sufficiently similar historical defects "
                "were found."
            )
        }

    matches = []

    for defect in relevant_defects:

        score = float(
            defect.get("similarity_score", 0)
        )

        percentage = float(
            defect.get(
                "similarity_percentage",
                score * 100
            )
        )

        if score >= 0.80:

            status = "Duplicate"

        elif score >= 0.50:

            status = "Related"

        else:

            continue

        matches.append({

            "bug_id": defect.get(
                "bug_id",
                "Unknown"
            ),

            "status": status,

            "similarity_score": round(
                score,
                4
            ),

            "similarity_percentage": round(
                percentage,
                2
            ),

            "description": defect.get(
                "description",
                ""
            ),

            "component": defect.get(
                "component",
                ""
            ),

            "exception_type": defect.get(
                "exception_type",
                ""
            ),

            "root_cause": defect.get(
                "root_cause",
                ""
            ),

            "resolution": defect.get(
                "resolution",
                ""
            ),

            "source": defect.get(
                "source",
                "Historical Knowledge Base"
            )
        })

    matches.sort(
        key=lambda item: item["similarity_score"],
        reverse=True
    )

    if not matches:

        return {
            "status": "New",
            "matches": [],
            "explanation": (
                "No historical bug crossed the "
                "configured similarity threshold."
            )
        }

    highest_score = matches[0]["similarity_score"]

    if highest_score >= 0.80:

        overall_status = "Duplicate"

        explanation = (
            "A highly similar historical defect was found. "
            "The current bug is likely a duplicate."
        )

    else:

        overall_status = "Related"

        explanation = (
            "A semantically related historical defect "
            "was found, but the similarity is not high "
            "enough to classify it as a confirmed duplicate."
        )

    return {

        "status": overall_status,

        "matches": matches,

        "explanation": explanation,

        "thresholds": {
            "duplicate": 0.80,
            "related": 0.50
        }
    }