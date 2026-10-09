import json
import os
from datetime import datetime


# =========================================
# CONFIGURATION
# =========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KB_FILE = os.path.join(
    BASE_DIR,
    "historical_defects.json"
)


# =========================================
# LOAD KNOWLEDGE BASE
# =========================================

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


# =========================================
# SAVE KNOWLEDGE BASE
# =========================================

def save_knowledge_base(defects):

    with open(
        KB_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            defects,
            file,
            indent=4
        )


# =========================================
# ADD RESOLVED BUG
# =========================================

def add_resolved_bug(
    bug_id,
    description,
    component,
    exception_type,
    root_cause,
    resolution,
    confirmed_fix,
    approval_status="Pending",
    severity="Unknown",
    priority="Unknown",
    source="Resolved Bug"
):

    # =========================================
    # VALIDATION
    # =========================================

    required_fields = {

        "bug_id":
            bug_id,

        "description":
            description,

        "component":
            component,

        "root_cause":
            root_cause,

        "resolution":
            resolution,

        "confirmed_fix":
            confirmed_fix
    }

    for field, value in required_fields.items():

        if not value or not str(value).strip():

            return {

                "success":
                    False,

                "message":
                    f"Missing required field: {field}"
            }

    # =========================================
    # APPROVAL VALIDATION
    # =========================================

    allowed_approval_status = [

        "Pending",

        "Approved",

        "Rejected"
    ]

    if approval_status not in allowed_approval_status:

        return {

            "success":
                False,

            "message":
                "Invalid approval status. "
                "Use Pending, Approved, or Rejected."
        }

    # =========================================
    # ONLY APPROVED BUGS ENTER KB
    # =========================================

    if approval_status != "Approved":

        return {

            "success":
                False,

            "message":
                "Bug cannot be added to the knowledge base "
                "until it is approved."
        }

    # =========================================
    # LOAD KNOWLEDGE BASE
    # =========================================

    defects = load_knowledge_base()

    # =========================================
    # DUPLICATE BUG ID CHECK
    # =========================================

    for defect in defects:

        if defect.get("bug_id") == bug_id:

            return {

                "success":
                    False,

                "message":
                    f"Bug {bug_id} already exists "
                    "in the knowledge base."
            }

    # =========================================
    # CREATE KNOWLEDGE RECORD
    # =========================================

    new_defect = {

        "bug_id":
            bug_id,

        "description":
            description,

        "component":
            component,

        "exception_type":
            exception_type,

        "severity":
            severity,

        "priority":
            priority,

        "root_cause":
            root_cause,

        "resolution":
            resolution,

        "confirmed_fix":
            confirmed_fix,

        "status":
            "Resolved",

        "approval_status":
            approval_status,

        "source":
            source,

        "timestamp":
            datetime.now().isoformat()
    }

    # =========================================
    # ADD TO KNOWLEDGE BASE
    # =========================================

    defects.append(
        new_defect
    )

    save_knowledge_base(
        defects
    )

    # =========================================
    # SUCCESS RESPONSE
    # =========================================

    return {

        "success":
            True,

        "message":
            f"Approved bug {bug_id} added to knowledge base.",

        "record":
            new_defect
    }


# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    result = add_resolved_bug(

        bug_id="BUG-107",

        description=
            "Search fails when the user enters an empty keyword",

        component=
            "Search",

        exception_type=
            "IllegalArgumentException",

        severity=
            "Medium",

        priority=
            "P2",

        root_cause=
            "Empty search input was not validated",

        resolution=
            "Added validation to reject empty search keywords",

        confirmed_fix=
            "Validated the fix by testing empty, valid, and boundary search inputs successfully.",

        approval_status=
            "Approved",

        source=
            "Approved Resolved Bug"
    )

    print("\n===================================")
    print("       KNOWLEDGE BASE UPDATE")
    print("===================================")

    print("\nSuccess:")
    print(result["success"])

    print("\nMessage:")
    print(result["message"])

    if result.get("record"):

        print("\nAdded Bug:")
        print(result["record"])

    print("\n===================================")