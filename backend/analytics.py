
import json
import os
from collections import Counter
from datetime import datetime

from backend.defect_retriever import text_similarity


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

HISTORICAL_FILE = os.path.join(
    PROJECT_ROOT, "historical_defects.json"
)
SUBMITTED_FILE = os.path.join(
    PROJECT_ROOT, "submitted_bugs.json"
)


# ============================================================
# LOAD JSON FILE
# ============================================================

def load_json_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


# ============================================================
# CLEAN AND COUNT VALUES
# ============================================================

def clean_value(value, default="Unknown"):
    if value is None:
        return default

    value = str(value).strip()
    return value if value else default


def count_values(records, field):
    values = [
        clean_value(record.get(field))
        for record in records
    ]

    return dict(
        sorted(
            Counter(values).items(),
            key=lambda item: (-item[1], item[0])
        )
    )


def get_most_common(frequency):
    if not frequency:
        return None

    item = max(
        frequency.items(),
        key=lambda pair: pair[1]
    )
    return [item[0], item[1]]


def get_component(record):
    return record.get(
        "component",
        record.get("affected_component")
    )


# ============================================================
# CREATE TEXT FOR BUG SIMILARITY
# ============================================================

def create_cluster_text(record):
    description = clean_value(
        record.get(
            "bug_description",
            record.get("description", "")
        ),
        ""
    )

    component = clean_value(
        get_component(record), ""
    )

    exception_type = clean_value(
        record.get("exception_type", ""), ""
    )

    root_cause = clean_value(
        record.get("root_cause", ""), ""
    )

    programming_language = clean_value(
        record.get("programming_language", ""), ""
    )

    stack_trace = clean_value(
        record.get("stack_trace", ""), ""
    )

    error_logs = clean_value(
        record.get("error_logs", ""), ""
    )

    return (
        f"Bug Description: {description}\n"
        f"Component: {component}\n"
        f"Exception: {exception_type}\n"
        f"Root Cause: {root_cause}\n"
        f"Programming Language: {programming_language}\n"
        f"Stack Trace: {stack_trace}\n"
        f"Error Logs: {error_logs}"
    )


# ============================================================
# LIGHTWEIGHT BUG CLUSTERING
# No SentenceTransformer, PyTorch or NumPy required
# ============================================================

def generate_semantic_clusters(records):
    """
    Group similar submitted bugs using lightweight
    word-frequency cosine similarity.

    Historical defects are not cluster members.
    A submitted bug belongs to at most one cluster.

    Note: This is lexical similarity, not embedding-based
    semantic similarity.
    """

    submitted_records = [
        record for record in records
        if record.get("record_type") == "Submitted"
    ]

    if len(submitted_records) < 2:
        return []

    # Lexical similarity threshold: tune after testing.
    SIMILARITY_THRESHOLD = 0.30

    bug_texts = []
    bug_ids = []
    components = []

    for index, record in enumerate(submitted_records):
        fallback_id = f"BUG-{index + 1}"

        bug_ids.append(
            clean_value(record.get("bug_id"), fallback_id)
        )

        bug_texts.append(create_cluster_text(record))

        components.append(
            clean_value(get_component(record), "")
        )

    # Calculate pairwise similarities without NumPy.
    total_bugs = len(submitted_records)

    similarity_matrix = [
        [0.0] * total_bugs
        for _ in range(total_bugs)
    ]

    for i in range(total_bugs):
        similarity_matrix[i][i] = 1.0

        for j in range(i + 1, total_bugs):
            similarity = text_similarity(
                bug_texts[i],
                bug_texts[j]
            )

            similarity_matrix[i][j] = similarity
            similarity_matrix[j][i] = similarity

    visited = set()
    clusters = []

    # Find connected groups of similar submitted bugs.
    for start_index in range(total_bugs):
        if start_index in visited:
            continue

        queue = [start_index]
        visited.add(start_index)
        cluster_indexes = set()

        while queue:
            current_index = queue.pop(0)
            cluster_indexes.add(current_index)

            for other_index in range(total_bugs):
                if other_index in visited:
                    continue

                similarity = similarity_matrix[
                    current_index
                ][other_index]

                if similarity >= SIMILARITY_THRESHOLD:
                    visited.add(other_index)
                    queue.append(other_index)

        # Ignore groups containing only one bug.
        if len(cluster_indexes) < 2:
            continue

        sorted_indexes = sorted(cluster_indexes)

        cluster_bug_ids = [
            bug_ids[index]
            for index in sorted_indexes
        ]

        pairwise_scores = []

        for i in range(len(sorted_indexes)):
            for j in range(i + 1, len(sorted_indexes)):
                index_a = sorted_indexes[i]
                index_b = sorted_indexes[j]

                pairwise_scores.append(
                    similarity_matrix[index_a][index_b]
                )

        average_similarity = (
            round(
                sum(pairwise_scores)
                / len(pairwise_scores)
                * 100,
                2
            )
            if pairwise_scores else 0
        )

        cluster_components = [
            components[index]
            for index in sorted_indexes
            if components[index]
            and components[index] != "Unknown"
        ]

        if cluster_components:
            theme = Counter(
                cluster_components
            ).most_common(1)[0][0]
        else:
            theme = "Similar Bug Pattern"

        cluster_number = len(clusters) + 1

        clusters.append({
            "cluster_id": f"CLUSTER-{cluster_number}",
            "theme": theme,
            "bug_count": len(cluster_bug_ids),
            "bug_ids": cluster_bug_ids,
            "average_similarity": average_similarity,
            "similarity_threshold": SIMILARITY_THRESHOLD,
            "description": (
                f"{len(cluster_bug_ids)} submitted bugs "
                f"form a similar-text cluster around {theme}."
            )
        })

    return clusters


# ============================================================
# GENERATE ANALYTICS
# ============================================================

def generate_analytics(filters=None):
    historical = load_json_file(HISTORICAL_FILE)
    submitted = load_json_file(SUBMITTED_FILE)

    all_records = []

    for record in historical:
        item = dict(record)
        item["record_type"] = "Historical"
        all_records.append(item)

    for record in submitted:
        item = dict(record)
        item["record_type"] = "Submitted"
        all_records.append(item)

    filters = filters or {}
    filtered_records = []

    # --------------------------------------------------------
    # APPLY FILTERS
    # --------------------------------------------------------

    for record in all_records:
        component = clean_value(get_component(record))
        severity = clean_value(record.get("severity"))
        priority = clean_value(record.get("priority"))
        exception_type = clean_value(
            record.get("exception_type")
        )

        if (
            filters.get("component")
            and component != filters["component"]
        ):
            continue

        if (
            filters.get("severity")
            and severity != filters["severity"]
        ):
            continue

        if (
            filters.get("priority")
            and priority != filters["priority"]
        ):
            continue

        if (
            filters.get("exception_type")
            and exception_type != filters["exception_type"]
        ):
            continue

        timestamp = str(record.get("timestamp") or "")

        if filters.get("start_date") and timestamp:
            if timestamp[:10] < filters["start_date"]:
                continue

        if filters.get("end_date") and timestamp:
            if timestamp[:10] > filters["end_date"]:
                continue

        filtered_records.append(record)

    # --------------------------------------------------------
    # FREQUENCY COUNTS
    # --------------------------------------------------------

    component_frequency = {}
    exception_frequency = {}
    severity_frequency = {}
    priority_frequency = {}
    root_cause_frequency = {}
    resolution_frequency = {}
    duplicate_status_frequency = {}

    for record in filtered_records:
        fields = {
            "component": clean_value(get_component(record)),
            "exception": clean_value(
                record.get("exception_type")
            ),
            "severity": clean_value(record.get("severity")),
            "priority": clean_value(record.get("priority")),
            "root_cause": clean_value(
                record.get("root_cause")
            ),
            "resolution": clean_value(
                record.get("resolution")
            ),
            "duplicate_status": clean_value(
                record.get("duplicate_status")
            )
        }

        frequency_targets = {
            "component": component_frequency,
            "exception": exception_frequency,
            "severity": severity_frequency,
            "priority": priority_frequency,
            "root_cause": root_cause_frequency,
            "resolution": resolution_frequency,
            "duplicate_status": duplicate_status_frequency
        }

        for field, value in fields.items():
            target = frequency_targets[field]
            target[value] = target.get(value, 0) + 1

    # --------------------------------------------------------
    # RECURRING PATTERNS
    # --------------------------------------------------------

    recurring_patterns = []

    for component, count in component_frequency.items():
        if component != "Unknown" and count >= 2:
            recurring_patterns.append({
                "type": "Affected Component",
                "pattern": component,
                "frequency": count,
                "description": (
                    f"{component} was affected by {count} defects."
                )
            })

    for exception_type, count in exception_frequency.items():
        if exception_type != "Unknown" and count >= 2:
            recurring_patterns.append({
                "type": "Exception Type",
                "pattern": exception_type,
                "frequency": count,
                "description": (
                    f"{exception_type} occurred in {count} defects."
                )
            })

    # --------------------------------------------------------
    # BUG CLUSTERS
    # --------------------------------------------------------

    semantic_clusters = generate_semantic_clusters(
        filtered_records
    )

    # --------------------------------------------------------
    # MONTHLY TIME ANALYSIS
    # --------------------------------------------------------

    time_analysis = {}

    for record in filtered_records:
        timestamp = record.get("timestamp")

        if not timestamp:
            continue

        try:
            date_value = datetime.fromisoformat(
                str(timestamp).replace("Z", "+00:00")
            )

            month_key = date_value.strftime("%Y-%m")

            time_analysis[month_key] = (
                time_analysis.get(month_key, 0) + 1
            )

        except (ValueError, TypeError):
            continue

    # --------------------------------------------------------
    # AVAILABLE FILTER VALUES
    # --------------------------------------------------------

    available_components = sorted({
        clean_value(get_component(record))
        for record in all_records
    })

    available_severities = sorted({
        clean_value(record.get("severity"))
        for record in all_records
    })

    available_priorities = sorted({
        clean_value(record.get("priority"))
        for record in all_records
    })

    available_exceptions = sorted({
        clean_value(record.get("exception_type"))
        for record in all_records
    })

    # --------------------------------------------------------
    # FINAL ANALYTICS RESULT
    # --------------------------------------------------------

    return {
        "total_bugs": len(filtered_records),

        "historical_bugs": sum(
            1 for record in filtered_records
            if record.get("record_type") == "Historical"
        ),

        "submitted_bugs": sum(
            1 for record in filtered_records
            if record.get("record_type") == "Submitted"
        ),

        "most_affected_component": get_most_common(
            component_frequency
        ),

        "most_common_exception": get_most_common(
            exception_frequency
        ),

        "component_frequency": component_frequency,
        "exception_frequency": exception_frequency,
        "severity_frequency": severity_frequency,
        "priority_frequency": priority_frequency,
        "duplicate_status_frequency": duplicate_status_frequency,
        "root_cause_frequency": root_cause_frequency,
        "resolution_frequency": resolution_frequency,
        "recurring_patterns": recurring_patterns,
        "semantic_clusters": semantic_clusters,
        "time_analysis": dict(sorted(time_analysis.items())),

        "available_filters": {
            "components": available_components,
            "severities": available_severities,
            "priorities": available_priorities,
            "exception_types": available_exceptions
        }
    }
