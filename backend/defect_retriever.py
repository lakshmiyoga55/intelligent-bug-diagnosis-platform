
import json
import os
import re
import math
from collections import Counter

# Project paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

# Support the knowledge base in either location
BACKEND_KB_FILE = os.path.join(BASE_DIR, "historical_defects.json")
ROOT_KB_FILE = os.path.join(PROJECT_DIR, "historical_defects.json")

KB_FILE = (
    BACKEND_KB_FILE
    if os.path.exists(BACKEND_KB_FILE)
    else ROOT_KB_FILE
)

VECTOR_STORE_FILE = os.path.join(BASE_DIR, "vector_store.json")

MODEL_NAME = "lightweight-text-similarity-v1"
TOP_K = 5


def tokenize(text):
    """Convert text into lowercase word tokens."""
    return re.findall(r"[a-z0-9_]+", str(text).lower())


def text_similarity(text_a, text_b):
    """Calculate cosine similarity using word frequencies."""
    words_a = Counter(tokenize(text_a))
    words_b = Counter(tokenize(text_b))

    if not words_a or not words_b:
        return 0.0

    common_words = words_a.keys() & words_b.keys()

    dot_product = sum(
        words_a[word] * words_b[word]
        for word in common_words
    )

    magnitude_a = math.sqrt(
        sum(value * value for value in words_a.values())
    )
    magnitude_b = math.sqrt(
        sum(value * value for value in words_b.values())
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    score = dot_product / (magnitude_a * magnitude_b)
    return max(0.0, min(1.0, score))


def load_knowledge_base():
    """Load historical defects from the available JSON file."""
    try:
        with open(KB_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            records = data.get("records", data.get("defects", []))
            return records if isinstance(records, list) else []

        return []

    except FileNotFoundError:
        print(f"Knowledge base not found: {KB_FILE}")
        return []

    except json.JSONDecodeError as error:
        print(f"Invalid knowledge-base JSON: {error}")
        return []


def create_embedding_text(defect):
    """Create searchable text from a historical defect."""
    return " ".join([
        str(defect.get("description", "")),
        str(defect.get("component", "")),
        str(defect.get("exception_type", "")),
        str(defect.get("root_cause", "")),
        str(defect.get("resolution", "")),
        str(defect.get("confirmed_fix", ""))
    ]).strip()


def create_bug_search_text(bug_data):
    """Create searchable text from the submitted bug."""
    return " ".join([
        str(bug_data.get("bug_description", "")),
        str(bug_data.get("affected_component", "")),
        str(bug_data.get("exception_type", "")),
        str(bug_data.get("error_message", "")),
        str(bug_data.get("stack_trace", "")),
        str(bug_data.get("error_logs", ""))
    ]).strip()


def build_vector_store():
    """Build a lightweight searchable store from historical defects."""
    defects = load_knowledge_base()

    if not defects:
        print("No historical defects found. Search store was not rebuilt.")
        return []

    vector_records = []

    for defect in defects:
        if not isinstance(defect, dict):
            continue

        record = dict(defect)
        record["search_text"] = create_embedding_text(defect)
        vector_records.append(record)

    with open(VECTOR_STORE_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {
                "model": MODEL_NAME,
                "records": vector_records
            },
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Search store created with {len(vector_records)} records.")
    return vector_records


def load_vector_store():
    """Load the store or rebuild it when necessary."""
    try:
        with open(VECTOR_STORE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if (
            isinstance(data, dict)
            and data.get("model") == MODEL_NAME
            and isinstance(data.get("records"), list)
        ):
            return data["records"]

    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return build_vector_store()


def retrieve_relevant_defects(bug_data, top_k=TOP_K):
    """Rank historical defects using weighted text similarity."""
    vector_records = load_vector_store()

    if not vector_records:
        return []

    submitted_description = bug_data.get("bug_description", "")
    submitted_component = bug_data.get("affected_component", "")
    submitted_exception = bug_data.get("exception_type", "")
    submitted_error = bug_data.get("error_message", "")
    submitted_failure = bug_data.get("failure_point", "")

    results = []

    for record in vector_records:
        if not isinstance(record, dict):
            continue

        description = record.get("description", "")
        component = record.get("component", "")
        exception_type = record.get("exception_type", "")
        root_cause = record.get("root_cause", "")
        resolution = record.get("resolution", "")

        # Compare the main description and structured fields.
        description_score = text_similarity(
            submitted_description, description
        )
        component_score = text_similarity(
            submitted_component, component
        )
        exception_score = text_similarity(
            submitted_exception, exception_type
        )

        # Error message can match historical descriptions or root causes.
        error_score = max(
            text_similarity(submitted_error, description),
            text_similarity(submitted_error, root_cause)
        )

        failure_score = text_similarity(
            submitted_failure, root_cause
        )

        # Include only fields that have values on both sides.
        weighted_scores = []

        if str(submitted_description).strip() and str(description).strip():
            weighted_scores.append((description_score, 0.50))

        if str(submitted_component).strip() and str(component).strip():
            weighted_scores.append((component_score, 0.20))

        if str(submitted_exception).strip() and str(exception_type).strip():
            weighted_scores.append((exception_score, 0.20))

        if str(submitted_error).strip():
            if description.strip() or root_cause.strip():
                weighted_scores.append((error_score, 0.08))

        if str(submitted_failure).strip() and str(root_cause).strip():
            weighted_scores.append((failure_score, 0.02))

        if weighted_scores:
            total_weight = sum(weight for _, weight in weighted_scores)
            similarity = sum(
                score * weight for score, weight in weighted_scores
            ) / total_weight
        else:
            similarity = 0.0

        result = {
            "bug_id": record.get("bug_id", "Unknown"),
            "description": description,
            "component": component,
            "exception_type": exception_type,
            "severity": record.get("severity", "Unknown"),
            "priority": record.get("priority", "Unknown"),
            "root_cause": root_cause,
            "resolution": resolution,
            "confirmed_fix": record.get("confirmed_fix", ""),
            "status": record.get("status", ""),
            "approval_status": record.get("approval_status", ""),
            "source": record.get(
                "source", "Historical Knowledge Base"
            ),
            "similarity_score": round(similarity, 4),
            "similarity_percentage": round(similarity * 100, 2)
        }

        results.append(result)

    results.sort(
        key=lambda item: item["similarity_score"],
        reverse=True
    )

    return results[:max(0, top_k)]


if __name__ == "__main__":
    print("Building lightweight search store...")
    records = build_vector_store()
    print(f"Search store contains {len(records)} records.")
