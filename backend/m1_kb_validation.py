import os
import json

from backend.defect_retriever import (
    load_vector_store,
    retrieve_relevant_defects
)


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Files are inside backend folder
KB_FILE = os.path.join(
    BASE_DIR,
    "historical_defects.json"
)

VECTOR_FILE = os.path.join(
    BASE_DIR,
    "vector_store.json"
)


# --------------------------------------------------
# Required fields for Historical Defect KB
# --------------------------------------------------

REQUIRED_FIELDS = [
    "bug_id",
    "description",
    "component",
    "exception_type",
    "root_cause",
    "resolution"
]


# --------------------------------------------------
# Load Historical Knowledge Base
# --------------------------------------------------

def load_kb():

    if not os.path.exists(KB_FILE):

        print(
            "❌ historical_defects.json not found at:"
        )

        print(KB_FILE)

        return []

    try:

        with open(
            KB_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, list):

            print(
                "❌ Historical KB format is not a list"
            )

            return []

        return data

    except Exception as e:

        print(
            "❌ Error loading Historical KB:",
            e
        )

        return []


# --------------------------------------------------
# Validate individual KB record
# --------------------------------------------------

def validate_record(record):

    missing_fields = []

    for field in REQUIRED_FIELDS:

        value = record.get(field)

        if value is None:

            missing_fields.append(field)

        elif str(value).strip() == "":

            missing_fields.append(field)

    return missing_fields


# --------------------------------------------------
# Validate complete KB
# --------------------------------------------------

def validate_kb(records):

    print("\n======================================")
    print("M1 HISTORICAL KB VALIDATION")
    print("======================================")

    print(
        "\nTotal KB records:",
        len(records)
    )

    if len(records) == 0:

        print(
            "❌ No records found."
        )

        return False

    valid_count = 0
    invalid_count = 0

    print("\nRecord Validation:")
    print("--------------------------------------")

    for record in records:

        bug_id = record.get(
            "bug_id",
            "UNKNOWN"
        )

        missing_fields = validate_record(
            record
        )

        if len(missing_fields) == 0:

            print(
                f"✅ {bug_id} - Valid"
            )

            valid_count += 1

        else:

            print(
                f"❌ {bug_id} - Missing: "
                f"{', '.join(missing_fields)}"
            )

            invalid_count += 1

    print("\n--------------------------------------")

    print(
        "Valid records:",
        valid_count
    )

    print(
        "Invalid records:",
        invalid_count
    )

    return invalid_count == 0


# --------------------------------------------------
# Check Vector Store
# --------------------------------------------------

def check_vector_store():

    print("\n======================================")
    print("VECTOR STORE CHECK")
    print("======================================")

    if not os.path.exists(VECTOR_FILE):

        print(
            "❌ vector_store.json not found at:"
        )

        print(VECTOR_FILE)

        return False

    print(
        "✅ vector_store.json found"
    )

    try:

        vector_store = load_vector_store()

        if not vector_store:

            print(
                "❌ Vector store is empty"
            )

            return False

        print(
            "✅ Vector store loaded successfully"
        )

        print(
            "Vector records:",
            len(vector_store)
        )

        return True

    except Exception as e:

        print(
            "❌ Error loading vector store:",
            e
        )

        return False


# --------------------------------------------------
# Semantic Retrieval Test
# --------------------------------------------------

def test_semantic_retrieval():

    print("\n======================================")
    print("SEMANTIC RETRIEVAL TEST")
    print("======================================")

    test_bug = (
        "Login crashes because the user object "
        "is null during authentication"
    )

    print("\nTest Bug:")
    print(test_bug)

    try:

        results = retrieve_relevant_defects(
            test_bug,
            top_k=3
        )

        if not results:

            print(
                "\n❌ No similar defects retrieved."
            )

            return False

        print(
            "\nRetrieved Similar Defects:"
        )

        print(
            "--------------------------------------"
        )

        for index, result in enumerate(
            results,
            start=1
        ):

            # Handle dictionary results
            if isinstance(result, dict):

                bug_id = result.get(
                    "bug_id",
                    "Unknown"
                )

                similarity = result.get(
                    "similarity_percentage",
                    result.get(
                        "similarity_score",
                        0
                    )
                )

                print(
                    f"{index}. {bug_id} "
                    f"- Similarity: {similarity:.2f}"
                )

            # Handle string results safely
            else:

                print(
                    f"{index}. {result}"
                )

        print(
            "\n✅ Semantic retrieval working."
        )

        return True

    except Exception as e:

        print(
            "\n❌ Semantic retrieval failed:",
            e
        )

        return False


# --------------------------------------------------
# M1 Final Validation
# --------------------------------------------------

def run_m1_validation():

    print("\n")

    print(
        "######################################"
    )

    print(
        "# M1 KNOWLEDGE BASE VALIDATION"
    )

    print(
        "######################################"
    )

    records = load_kb()

    kb_status = validate_kb(
        records
    )

    vector_status = check_vector_store()

    retrieval_status = test_semantic_retrieval()

    print("\n")

    print(
        "======================================"
    )

    print(
        "M1 VALIDATION SUMMARY"
    )

    print(
        "======================================"
    )

    print(
        "Historical KB:",
        "PASS" if kb_status else "FAIL"
    )

    print(
        "Vector Store:",
        "PASS" if vector_status else "FAIL"
    )

    print(
        "Semantic Retrieval:",
        "PASS" if retrieval_status else "FAIL"
    )

    print(
        "\n======================================"
    )

    if (
        kb_status
        and vector_status
        and retrieval_status
    ):

        print(
            "✅ M1 KB IMPLEMENTATION VALIDATED"
        )

    else:

        print(
            "⚠️ M1 STILL HAS VALIDATION GAPS"
        )

    print(
        "======================================"
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    run_m1_validation()