import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer


# ==============================
# Configuration
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KB_FILE = os.path.join(BASE_DIR, "historical_defects.json")
VECTOR_STORE_FILE = os.path.join(BASE_DIR, "vector_store.json")

MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 5


# ==============================
# Load Embedding Model
# ==============================

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded successfully.")


# ==============================
# Knowledge Base
# ==============================

def load_knowledge_base():

    try:

        with open(
            KB_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):

        return []


# ==============================
# Create Text for Embedding
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


# ==============================
# Build Vector Store
# ==============================

def build_vector_store():

    defects = load_knowledge_base()

    if not defects:

        return []

    texts = [
        create_embedding_text(defect)
        for defect in defects
    ]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    vector_records = []

    for defect, embedding in zip(
        defects,
        embeddings
    ):

        vector_records.append({

            "bug_id":
                defect.get("bug_id", ""),

            "description":
                defect.get("description", ""),

            "component":
                defect.get("component", ""),

            "exception_type":
                defect.get("exception_type", ""),

            "severity":
                defect.get(
                    "severity",
                    "Unknown"
                ),

            "priority":
                defect.get(
                    "priority",
                    "Unknown"
                ),

            "root_cause":
                defect.get("root_cause", ""),

            "resolution":
                defect.get("resolution", ""),

            "confirmed_fix":
                defect.get(
                    "confirmed_fix",
                    ""
                ),

            "status":
                defect.get("status", ""),

            "approval_status":
                defect.get(
                    "approval_status",
                    ""
                ),

            "source":
                defect.get(
                    "source",
                    "Historical Knowledge Base"
                ),

            "timestamp":
                defect.get(
                    "timestamp",
                    ""
                ),

            "embedding":
                embedding.tolist()
        })

    with open(
        VECTOR_STORE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {
                "model": MODEL_NAME,
                "records": vector_records
            },
            file,
            indent=4
        )

    return vector_records


# ==============================
# Load Vector Store
# ==============================

def load_vector_store():

    try:

        with open(
            VECTOR_STORE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if data.get("model") != MODEL_NAME:

            return build_vector_store()

        return data.get(
            "records",
            []
        )

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):

        return build_vector_store()


# ==============================
# Convert Bug to Search Text
# ==============================

def create_bug_search_text(bug_data):

    return f"""
Bug Description:
{bug_data.get("bug_description", "")}

Component:
{bug_data.get("affected_component", "")}

Exception Type:
{bug_data.get("exception_type", "")}

Programming Language:
{bug_data.get("programming_language", "")}

Stack Trace:
{bug_data.get("stack_trace", "")}

Error Logs:
{bug_data.get("error_logs", "")}
""".strip()


# ==============================
# Semantic Retrieval
# ==============================

def retrieve_relevant_defects(
    bug_data,
    top_k=TOP_K
):

    vector_records = load_vector_store()

    if not vector_records:

        return []

    search_text = create_bug_search_text(
        bug_data
    )

    query_embedding = model.encode(
        search_text,
        normalize_embeddings=True
    )

    results = []

    for record in vector_records:

        stored_embedding = np.array(
            record.get(
                "embedding",
                []
            ),
            dtype=float
        )

        if stored_embedding.size == 0:

            continue

        similarity = float(
            np.dot(
                query_embedding,
                stored_embedding
            )
        )

        similarity = max(
            0.0,
            min(
                1.0,
                similarity
            )
        )

        result = {

            "bug_id":
                record.get(
                    "bug_id",
                    "Unknown"
                ),

            "description":
                record.get(
                    "description",
                    ""
                ),

            "component":
                record.get(
                    "component",
                    ""
                ),

            "exception_type":
                record.get(
                    "exception_type",
                    ""
                ),

            "severity":
                record.get(
                    "severity",
                    "Unknown"
                ),

            "priority":
                record.get(
                    "priority",
                    "Unknown"
                ),

            "root_cause":
                record.get(
                    "root_cause",
                    ""
                ),

            "resolution":
                record.get(
                    "resolution",
                    ""
                ),

            "confirmed_fix":
                record.get(
                    "confirmed_fix",
                    ""
                ),

            "status":
                record.get(
                    "status",
                    ""
                ),

            "approval_status":
                record.get(
                    "approval_status",
                    ""
                ),

            "source":
                record.get(
                    "source",
                    "Historical Knowledge Base"
                ),

            "similarity_score":
                round(
                    similarity,
                    4
                ),

            "similarity_percentage":
                round(
                    similarity * 100,
                    2
                )
        }

        results.append(result)

    results.sort(
        key=lambda item:
            item["similarity_score"],
        reverse=True
    )

    return results[:top_k]


# ==============================
# Test
# ==============================

if __name__ == "__main__":

    print("\nBuilding vector store...")

    records = build_vector_store()

    print(
        f"Vector store created with "
        f"{len(records)} records."
    )

    print("\nConfirmed Fix Verification:")

    for record in records:

        if record.get("bug_id") == "BUG-107":

            print(
                "Bug ID:",
                record.get("bug_id")
            )

            print(
                "Confirmed Fix:",
                record.get("confirmed_fix")
            )

            print(
                "Approval Status:",
                record.get("approval_status")
            )

            break