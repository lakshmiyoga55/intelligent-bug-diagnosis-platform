from backend.kb_manager import add_resolved_bug


def approve_and_add_bug(data):
    required_fields = [
        "bug_id",
        "description",
        "component",
        "root_cause",
        "resolution"
    ]

    for field in required_fields:
        if not data.get(field):
            return {
                "success": False,
                "message": f"Missing required field: {field}"
            }

    return add_resolved_bug(
        bug_id=data["bug_id"],
        description=data["description"],
        component=data["component"],
        exception_type=data.get("exception_type", ""),
        severity=data.get("severity", "Unknown"),
        priority=data.get("priority", "Unknown"),
        root_cause=data["root_cause"],
        resolution=data["resolution"],
        source=data.get("source", "Approved Resolved Bug")
    )