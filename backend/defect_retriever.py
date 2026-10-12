
import json
import os
import re
import math
from collections import Counter


# ==============================
# Configuration
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KB_FILE = os.path.join(BASE_DIR, "historical_defects.json")
VECTOR_STORE_FILE = os.path.join(BASE_DIR, "vector_store.json")

MODEL_NAME = "lightweight-text-similarity-v1"
TOP_K = 5


# ==============================
# Lightweight Text Processing
# ==============================

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

    return max(
        0.0,
        min(1.0, dot_product / (magnitude_a * magnitude_b))
    )


# ==============================
# Knowledge Base
# ==============================

def load_knowledge_base():
    try:
        with open(KB_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# ==============================
# Create Search Text
# ==============================

def create_embedding_text(defect):
    return f"""
Bug ID: {defect.get("bug_id", "")}
Description: {defect.get("description", "")}
Component: {defect.get("component", "")}
Exception Type: {defect.get("exception_type", "")}
Severity: {defect.get("severity", "")}
Priority: {defect.get("priority", "")}
Root Cause: {defect.get("root_cause", "")}
Resolution: {defect.get("resolution", "")}
Confirmed Fix: {defect.get("confirmed_fix", "")}
""".strip()


def create_bug_search_text(bug_data):
    return f"""
Bug Description: {bug_data.get("bug_description", "")}
Component: {bug_data.get("affected_component", "")}
Exception Type: {bug_data.get("exception_type", "")}
Programming Language: {bug_data.get("programming_language", "")}
Stack Trace: {bug_data.get("stack_trace", "")}
Error Logs: {bug_data.get("error_logs", "")}
""".strip()


# ==============================
# Build Lightweight Search Store
# ==============================

def build_vector_store():
    defects = load_knowledge_base()

    if not defects:
        return []

    vector_records = []

    for defect in defects:
        vector_records.append({
            "bug_id": defect.get("bug_id", ""),
            "description": defect.get("description", ""),
            "component": defect.get("component", ""),
            "exception_type": defect.get("exception_type", ""),
            "severity": defect.get("severity", "Unknown"),
            "priority": defect.get("priority", "Unknown"),
            "root_cause": defect.get("root_cause", ""),
            "resolution": defect.get("resolution", ""),
            "confirmed_fix": defect.get("confirmed_fix", ""),
            "status": defect.get("status", ""),
            "approval_status": defect.get("approval_status", ""),
            "source": defect.get(
                "source", "Historical Knowledge Base"
            ),
            "timestamp": defect.get("timestamp", ""),
            "search_text": create_embedding_text(defect)
        })

    with open(VECTOR_STORE_FILE, "w", encoding="utf-8") as file:
        json.dump({
            "model": MODEL_NAME,
            "records": vector_records
        }, file, indent=4)

    return vector_records


# ==============================
# Load Search Store
# ==============================

def load_vector_store():
    try:
        with open(VECTOR_STORE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if (
            not isinstance(data, dict)
            or data.get("model") != MODEL_NAME
            or not isinstance(data.get("records"), list)
        ):
            return build_vector_store()

        return data["records"]

    except (FileNotFoundError, json.JSONDecodeError):
        return build_vector_store()


# ==============================
# Retrieve Relevant Defects
# ==============================

def retrieve_relevant_defects(bug_data, top_k=TOP_K):
    vector_records = load_vector_store()

    if not vector_records:
        return []

    search_text = create_bug_search_text(bug_data)
    results = []

    for record in vector_records:
        stored_text = record.get("search_text", "")

        if not stored_text:
            stored_text = create_embedding_text(record)

        similarity = text_similarity(search_text, stored_text)

        result = {
            "bug_id": record.get("bug_id", "Unknown"),
            "description": record.get("description", ""),
            "component": record.get("component", ""),
            "exception_type": record.get("exception_type", ""),
            "severity": record.get("severity", "Unknown"),
            "priority": record.get("priority", "Unknown"),
            "root_cause": record.get("root_cause", ""),
            "resolution": record.get("resolution", ""),
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


# ==============================
# Test
# ==============================

if __name__ == "__main__":
    print("Building lightweight search store...")

    records = build_vector_store()

    print(f"Search store created with {len(records)} records.")
    print("Text similarity search is ready.")
