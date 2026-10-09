import os
import json

from openai import OpenAI
from dotenv import load_dotenv

from backend.defect_retriever import retrieve_relevant_defects


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key
) if api_key else None


def root_cause_analysis(bug_data):

    # -----------------------------------------------------
    # Retrieve historical defects
    # -----------------------------------------------------

    relevant_defects = retrieve_relevant_defects(bug_data)

    if not relevant_defects:

        return {
            "root_cause": "Insufficient Evidence",
            "confidence": 0,
            "reasoning": "No relevant historical defects were found.",
            "evidence_type": "None",
            "supporting_evidence": []
        }

    # -----------------------------------------------------
    # Prefer an exact/current approved KB match
    # -----------------------------------------------------

    target_bug_id = bug_data.get("bug_id")

    selected_defect = None

    if target_bug_id:

        for defect in relevant_defects:

            if defect.get("bug_id") == target_bug_id:

                selected_defect = defect
                break

    # -----------------------------------------------------
    # If no exact ID match, use highest similarity
    # -----------------------------------------------------

    if selected_defect is None:

        selected_defect = max(
            relevant_defects,
            key=lambda defect: float(
                defect.get("similarity_score", 0)
            )
        )

    similarity_score = float(
        selected_defect.get(
            "similarity_score",
            0
        )
    )

    # -----------------------------------------------------
    # Build historical context
    # -----------------------------------------------------

    historical_context = ""

    for defect in relevant_defects[:5]:

        historical_context += f"""
Bug ID: {defect.get("bug_id")}
Description: {defect.get("description")}
Component: {defect.get("component")}
Exception: {defect.get("exception_type")}
Historical Root Cause: {defect.get("root_cause")}
Historical Resolution: {defect.get("resolution")}
Confirmed Fix: {defect.get("confirmed_fix", "")}
Approval Status: {defect.get("approval_status", "")}
Similarity Score: {defect.get("similarity_score", 0)}
-----------------------------------
"""

    # -----------------------------------------------------
    # No OpenAI API key
    # -----------------------------------------------------

    if client is None:

        return {
            "root_cause": selected_defect.get(
                "root_cause",
                "Insufficient Evidence"
            ),

            "confidence": round(
                similarity_score,
                2
            ),

            "reasoning": (
                "The probable root cause was identified "
                "from the most relevant historical defect "
                "in the knowledge base."
            ),

            "evidence_type": "Historical Evidence",

            "supporting_evidence": [

                {
                    "bug_id": selected_defect.get("bug_id"),

                    "description": selected_defect.get(
                        "description"
                    ),

                    "resolution": selected_defect.get(
                        "resolution"
                    ),

                    "confirmed_fix": selected_defect.get(
                        "confirmed_fix",
                        ""
                    ),

                    "similarity_score": similarity_score,

                    "approval_status": selected_defect.get(
                        "approval_status",
                        ""
                    )
                }
            ]
        }

    # -----------------------------------------------------
    # LLM analysis
    # -----------------------------------------------------

    try:

        response = client.chat.completions.create(

            model="gpt-4o-mini",

            messages=[

                {
                    "role": "system",

                    "content": (
                        "You are a software root cause "
                        "analysis agent. Return only valid JSON."
                    )
                },

                {
                    "role": "user",

                    "content": f"""
Analyze the current bug using the historical evidence.

Current Bug:
{bug_data.get("bug_description", "")}

Component:
{bug_data.get("affected_component", "")}

Exception:
{bug_data.get("exception_type", "")}

Historical Evidence:
{historical_context}

Return JSON:

{{
    "root_cause": "Most probable root cause",
    "confidence": 0.0,
    "reasoning": "Explanation",
    "evidence_type": "Historical Evidence"
}}
"""
                }
            ],

            temperature=0.2
        )

        result_text = (
            response
            .choices[0]
            .message
            .content
        )

        result_text = result_text.replace(
            "```json",
            ""
        )

        result_text = result_text.replace(
            "```",
            ""
        )

        result = json.loads(
            result_text.strip()
        )

        result["supporting_evidence"] = [

            {
                "bug_id": selected_defect.get(
                    "bug_id"
                ),

                "description": selected_defect.get(
                    "description"
                ),

                "resolution": selected_defect.get(
                    "resolution"
                ),

                "confirmed_fix": selected_defect.get(
                    "confirmed_fix",
                    ""
                ),

                "similarity_score": similarity_score,

                "approval_status": selected_defect.get(
                    "approval_status",
                    ""
                )
            }
        ]

        return result

    # -----------------------------------------------------
    # LLM failure → historical fallback
    # -----------------------------------------------------

    except Exception as e:

        return {

            "root_cause": selected_defect.get(
                "root_cause",
                "Insufficient Evidence"
            ),

            "confidence": round(
                similarity_score,
                2
            ),

            "reasoning": (
                "LLM analysis was unavailable. "
                "The result is based on the most relevant "
                "historical knowledge base record."
            ),

            "evidence_type":
                "Historical Evidence - Fallback",

            "supporting_evidence": [

                {
                    "bug_id": selected_defect.get(
                        "bug_id"
                    ),

                    "description": selected_defect.get(
                        "description"
                    ),

                    "resolution": selected_defect.get(
                        "resolution"
                    ),

                    "confirmed_fix": selected_defect.get(
                        "confirmed_fix",
                        ""
                    ),

                    "similarity_score": similarity_score,

                    "approval_status": selected_defect.get(
                        "approval_status",
                        ""
                    )
                }
            ],

            "fallback_reason": str(e)
        }