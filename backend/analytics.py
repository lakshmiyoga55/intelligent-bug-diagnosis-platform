import json
import os
from collections import Counter
from datetime import datetime

import numpy as np

from backend.defect_retriever import model


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

HISTORICAL_FILE = os.path.join(
    PROJECT_ROOT,
    "historical_defects.json"
)

SUBMITTED_FILE = os.path.join(
    PROJECT_ROOT,
    "submitted_bugs.json"
)


# ============================================================
# LOAD JSON FILE
# ============================================================

def load_json_file(filename):

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (
        FileNotFoundError,
        json.JSONDecodeError,
        OSError
    ):

        return []


# ============================================================
# CLEAN VALUE
# ============================================================

def clean_value(
    value,
    default="Unknown"
):

    if value is None:
        return default

    value = str(value).strip()

    if not value:
        return default

    return value


# ============================================================
# COUNT VALUES
# ============================================================

def count_values(
    records,
    field
):

    values = []

    for record in records:

        value = clean_value(
            record.get(field)
        )

        values.append(value)

    return dict(
        sorted(
            Counter(values).items(),
            key=lambda x: (-x[1], x[0])
        )
    )


# ============================================================
# MOST COMMON VALUE
# ============================================================

def get_most_common(
    frequency
):

    if not frequency:
        return None

    item = max(
        frequency.items(),
        key=lambda x: x[1]
    )

    return [
        item[0],
        item[1]
    ]


# ============================================================
# CREATE SEARCH TEXT
# ============================================================

def create_cluster_text(record):

    description = clean_value(
        record.get(
            "bug_description",
            record.get(
                "description",
                ""
            )
        ),
        ""
    )

    component = clean_value(
        record.get(
            "component",
            record.get(
                "affected_component",
                ""
            )
        ),
        ""
    )

    exception_type = clean_value(
        record.get(
            "exception_type",
            ""
        ),
        ""
    )

    root_cause = clean_value(
        record.get(
            "root_cause",
            ""
        ),
        ""
    )

    programming_language = clean_value(
        record.get(
            "programming_language",
            ""
        ),
        ""
    )

    stack_trace = clean_value(
        record.get(
            "stack_trace",
            ""
        ),
        ""
    )

    error_logs = clean_value(
        record.get(
            "error_logs",
            ""
        ),
        ""
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
# SEMANTIC CLUSTERING
# ============================================================

def generate_semantic_clusters(records):

    """
    Generate semantic clusters only among submitted bugs.

    Historical defects are NOT added as cluster members.
    The same submitted bug is assigned to only one cluster.

    Embeddings are generated using the same
    SentenceTransformer model used by the defect retriever.
    """

    # --------------------------------------------------------
    # Only submitted records
    # --------------------------------------------------------

    submitted_records = [

        record

        for record in records

        if record.get(
            "record_type"
        ) == "Submitted"

    ]

    if len(submitted_records) < 2:
        return []


    # --------------------------------------------------------
    # Similarity threshold
    # --------------------------------------------------------

    SIMILARITY_THRESHOLD = 0.70


    # --------------------------------------------------------
    # Create bug texts
    # --------------------------------------------------------

    bug_texts = []

    bug_ids = []

    components = []


    for index, record in enumerate(
        submitted_records
    ):

        bug_id = clean_value(
            record.get(
                "bug_id",
                f"BUG-{index + 1}"
            ),
            f"BUG-{index + 1}"
        )

        bug_ids.append(
            bug_id
        )


        bug_texts.append(
            create_cluster_text(
                record
            )
        )


        component = clean_value(
            record.get(
                "component",
                record.get(
                    "affected_component",
                    ""
                )
            ),
            ""
        )

        components.append(
            component
        )


    # --------------------------------------------------------
    # Generate embeddings
    # --------------------------------------------------------

    try:

        embeddings = model.encode(
            bug_texts,
            normalize_embeddings=True
        )

        embeddings = np.asarray(
            embeddings
        )

    except Exception as error:

        print(
            "Semantic clustering error:",
            error
        )

        return []


    # --------------------------------------------------------
    # Cosine similarity matrix
    #
    # Because embeddings are normalized,
    # dot product = cosine similarity.
    # --------------------------------------------------------

    similarity_matrix = np.matmul(
        embeddings,
        embeddings.T
    )


    # --------------------------------------------------------
    # Build graph of semantically similar bugs
    # --------------------------------------------------------

    total_bugs = len(
        submitted_records
    )

    visited = set()

    clusters = []


    for start_index in range(
        total_bugs
    ):

        if start_index in visited:
            continue


        # ----------------------------------------------------
        # Breadth-first search
        # to find connected semantic bugs
        # ----------------------------------------------------

        queue = [
            start_index
        ]

        cluster_indexes = set()

        visited.add(
            start_index
        )


        while queue:

            current_index = queue.pop(
                0
            )

            cluster_indexes.add(
                current_index
            )


            for other_index in range(
                total_bugs
            ):

                if other_index in visited:
                    continue


                similarity = float(
                    similarity_matrix[
                        current_index,
                        other_index
                    ]
                )


                if (
                    similarity
                    >= SIMILARITY_THRESHOLD
                ):

                    visited.add(
                        other_index
                    )

                    queue.append(
                        other_index
                    )


        # ----------------------------------------------------
        # Ignore single-bug clusters
        # ----------------------------------------------------

        if len(
            cluster_indexes
        ) < 2:

            continue


        sorted_indexes = sorted(
            cluster_indexes
        )


        cluster_bug_ids = [

            bug_ids[index]

            for index
            in sorted_indexes

        ]


        # ----------------------------------------------------
        # Calculate pairwise similarity
        # ----------------------------------------------------

        pairwise_scores = []


        for i in range(
            len(sorted_indexes)
        ):

            for j in range(
                i + 1,
                len(sorted_indexes)
            ):

                index_a = sorted_indexes[i]

                index_b = sorted_indexes[j]


                similarity = float(
                    similarity_matrix[
                        index_a,
                        index_b
                    ]
                )


                pairwise_scores.append(
                    similarity
                )


        if pairwise_scores:

            average_similarity = round(
                (
                    sum(
                        pairwise_scores
                    )
                    /
                    len(
                        pairwise_scores
                    )
                ) * 100,
                2
            )

        else:

            average_similarity = 0


        # ----------------------------------------------------
        # Determine cluster theme
        # ----------------------------------------------------

        cluster_components = [

            components[index]

            for index
            in sorted_indexes

            if components[index]
            and components[index]
            != "Unknown"

        ]


        if cluster_components:

            component_counter = Counter(
                cluster_components
            )

            theme = component_counter.most_common(
                1
            )[0][0]

        else:

            theme = "Semantic Bug Pattern"


        # ----------------------------------------------------
        # Create cluster
        # ----------------------------------------------------

        cluster_number = (
            len(clusters) + 1
        )


        cluster = {

            "cluster_id":
                f"CLUSTER-{cluster_number}",

            "theme":
                theme,

            "bug_count":
                len(cluster_bug_ids),

            "bug_ids":
                cluster_bug_ids,

            "average_similarity":
                average_similarity,

            "similarity_threshold":
                SIMILARITY_THRESHOLD,

            "description":
                (
                    f"{len(cluster_bug_ids)} "
                    f"submitted bugs form a "
                    f"semantic cluster around "
                    f"{theme}."
                )
        }


        clusters.append(
            cluster
        )


    return clusters


# ============================================================
# GENERATE ANALYTICS
# ============================================================

def generate_analytics(
    filters=None
):

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    historical = load_json_file(
        HISTORICAL_FILE
    )

    submitted = load_json_file(
        SUBMITTED_FILE
    )

    all_records = []


    # --------------------------------------------------------
    # HISTORICAL RECORDS
    # --------------------------------------------------------

    for record in historical:

        record = dict(
            record
        )

        record["record_type"] = (
            "Historical"
        )

        all_records.append(
            record
        )


    # --------------------------------------------------------
    # SUBMITTED RECORDS
    # --------------------------------------------------------

    for record in submitted:

        record = dict(
            record
        )

        record["record_type"] = (
            "Submitted"
        )

        all_records.append(
            record
        )


    # --------------------------------------------------------
    # APPLY FILTERS
    # --------------------------------------------------------

    filters = filters or {}

    filtered_records = []


    for record in all_records:

        component = clean_value(
            record.get(
                "component",
                record.get(
                    "affected_component"
                )
            )
        )


        severity = clean_value(
            record.get(
                "severity"
            )
        )


        priority = clean_value(
            record.get(
                "priority"
            )
        )


        exception_type = clean_value(
            record.get(
                "exception_type"
            )
        )


        # ----------------------------------------------------
        # COMPONENT FILTER
        # ----------------------------------------------------

        if (
            filters.get(
                "component"
            )
            and component
            != filters[
                "component"
            ]
        ):

            continue


        # ----------------------------------------------------
        # SEVERITY FILTER
        # ----------------------------------------------------

        if (
            filters.get(
                "severity"
            )
            and severity
            != filters[
                "severity"
            ]
        ):

            continue


        # ----------------------------------------------------
        # PRIORITY FILTER
        # ----------------------------------------------------

        if (
            filters.get(
                "priority"
            )
            and priority
            != filters[
                "priority"
            ]
        ):

            continue


        # ----------------------------------------------------
        # EXCEPTION FILTER
        # ----------------------------------------------------

        if (
            filters.get(
                "exception_type"
            )
            and exception_type
            != filters[
                "exception_type"
            ]
        ):

            continue


        # ----------------------------------------------------
        # DATE FILTER
        # ----------------------------------------------------

        timestamp = record.get(
            "timestamp",
            ""
        )


        if filters.get(
            "start_date"
        ):

            if timestamp:

                record_date = (
                    timestamp[:10]
                )

                if (
                    record_date
                    <
                    filters[
                        "start_date"
                    ]
                ):

                    continue


        if filters.get(
            "end_date"
        ):

            if timestamp:

                record_date = (
                    timestamp[:10]
                )

                if (
                    record_date
                    >
                    filters[
                        "end_date"
                    ]
                ):

                    continue


        filtered_records.append(
            record
        )


    # ========================================================
    # FREQUENCY DATA
    # ========================================================

    component_frequency = {}

    exception_frequency = {}

    severity_frequency = {}

    priority_frequency = {}

    root_cause_frequency = {}

    resolution_frequency = {}

    duplicate_status_frequency = {}


    for record in filtered_records:

        component = clean_value(
            record.get(
                "component",
                record.get(
                    "affected_component"
                )
            )
        )


        exception_type = clean_value(
            record.get(
                "exception_type"
            )
        )


        severity = clean_value(
            record.get(
                "severity"
            )
        )


        priority = clean_value(
            record.get(
                "priority"
            )
        )


        root_cause = clean_value(
            record.get(
                "root_cause"
            )
        )


        resolution = clean_value(
            record.get(
                "resolution"
            )
        )


        duplicate_status = clean_value(
            record.get(
                "duplicate_status"
            )
        )


        # ----------------------------------------------------
        # COMPONENT
        # ----------------------------------------------------

        component_frequency[
            component
        ] = (
            component_frequency.get(
                component,
                0
            ) + 1
        )


        # ----------------------------------------------------
        # EXCEPTION
        # ----------------------------------------------------

        exception_frequency[
            exception_type
        ] = (
            exception_frequency.get(
                exception_type,
                0
            ) + 1
        )


        # ----------------------------------------------------
        # SEVERITY
        # ----------------------------------------------------

        severity_frequency[
            severity
        ] = (
            severity_frequency.get(
                severity,
                0
            ) + 1
        )


        # ----------------------------------------------------
        # PRIORITY
        # ----------------------------------------------------

        priority_frequency[
            priority
        ] = (
            priority_frequency.get(
                priority,
                0
            ) + 1
        )


        # ----------------------------------------------------
        # ROOT CAUSE
        # ----------------------------------------------------

        root_cause_frequency[
            root_cause
        ] = (
            root_cause_frequency.get(
                root_cause,
                0
            ) + 1
        )


        # ----------------------------------------------------
        # RESOLUTION
        # ----------------------------------------------------

        resolution_frequency[
            resolution
        ] = (
            resolution_frequency.get(
                resolution,
                0
            ) + 1
        )


        # ----------------------------------------------------
        # DUPLICATE STATUS
        # ----------------------------------------------------

        duplicate_status_frequency[
            duplicate_status
        ] = (
            duplicate_status_frequency.get(
                duplicate_status,
                0
            ) + 1
        )


    # ========================================================
    # RECURRING PATTERNS
    # ========================================================

    recurring_patterns = []


    # --------------------------------------------------------
    # COMPONENT PATTERNS
    # --------------------------------------------------------

    for component, count in (
        component_frequency.items()
    ):

        if (
            component != "Unknown"
            and count >= 2
        ):

            recurring_patterns.append({

                "type":
                    "Affected Component",

                "pattern":
                    component,

                "frequency":
                    count,

                "description":
                    (
                        f"{component} was affected "
                        f"by {count} defects."
                    )
            })


    # --------------------------------------------------------
    # EXCEPTION PATTERNS
    # --------------------------------------------------------

    for (
        exception_type,
        count
    ) in exception_frequency.items():

        if (
            exception_type != "Unknown"
            and count >= 2
        ):

            recurring_patterns.append({

                "type":
                    "Exception Type",

                "pattern":
                    exception_type,

                "frequency":
                    count,

                "description":
                    (
                        f"{exception_type} occurred "
                        f"in {count} defects."
                    )
            })


    # ========================================================
    # SEMANTIC CLUSTERS
    # ========================================================

    semantic_clusters = (
        generate_semantic_clusters(
            filtered_records
        )
    )


    # ========================================================
    # TIME ANALYSIS
    # ========================================================

    time_analysis = {}


    for record in filtered_records:

        timestamp = record.get(
            "timestamp"
        )


        if not timestamp:
            continue


        try:

            date_value = (
                datetime.fromisoformat(
                    timestamp.replace(
                        "Z",
                        ""
                    )
                )
            )


            month_key = (
                date_value.strftime(
                    "%Y-%m"
                )
            )


            time_analysis[
                month_key
            ] = (
                time_analysis.get(
                    month_key,
                    0
                ) + 1
            )


        except (
            ValueError,
            TypeError
        ):

            continue


    # ========================================================
    # AVAILABLE FILTER VALUES
    # ========================================================

    available_components = sorted(
        set(

            clean_value(
                r.get(
                    "component",
                    r.get(
                        "affected_component"
                    )
                )
            )

            for r in all_records

        )
    )


    available_severities = sorted(
        set(

            clean_value(
                r.get(
                    "severity"
                )
            )

            for r in all_records

        )
    )


    available_priorities = sorted(
        set(

            clean_value(
                r.get(
                    "priority"
                )
            )

            for r in all_records

        )
    )


    available_exceptions = sorted(
        set(

            clean_value(
                r.get(
                    "exception_type"
                )
            )

            for r in all_records

        )
    )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {

        "total_bugs":
            len(
                filtered_records
            ),


        "historical_bugs":
            sum(

                1

                for r
                in filtered_records

                if r.get(
                    "record_type"
                )
                == "Historical"

            ),


        "submitted_bugs":
            sum(

                1

                for r
                in filtered_records

                if r.get(
                    "record_type"
                )
                == "Submitted"

            ),


        "most_affected_component":
            get_most_common(
                component_frequency
            ),


        "most_common_exception":
            get_most_common(
                exception_frequency
            ),


        "component_frequency":
            component_frequency,


        "exception_frequency":
            exception_frequency,


        "severity_frequency":
            severity_frequency,


        "priority_frequency":
            priority_frequency,


        "duplicate_status_frequency":
            duplicate_status_frequency,


        "root_cause_frequency":
            root_cause_frequency,


        "resolution_frequency":
            resolution_frequency,


        "recurring_patterns":
            recurring_patterns,


        "semantic_clusters":
            semantic_clusters,


        "time_analysis":
            dict(
                sorted(
                    time_analysis.items()
                )
            ),


        "available_filters": {

            "components":
                available_components,

            "severities":
                available_severities,

            "priorities":
                available_priorities,

            "exception_types":
                available_exceptions
        }
    }