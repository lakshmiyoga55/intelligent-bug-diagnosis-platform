from defect_retriever import retrieve_relevant_defects


bug_data = {
    "bug_description": "When the user enters valid login details, the application crashes.",
    "affected_component": "Authentication/Login",
    "exception_type": "NullPointerException"
}


results = retrieve_relevant_defects(bug_data)


print("\n===================================")
print("   HISTORICAL DEFECT RETRIEVAL")
print("===================================")

for defect in results:

    print("\nBug ID:", defect["bug_id"])
    print("Description:", defect["description"])
    print("Component:", defect["component"])
    print("Exception:", defect["exception_type"])
    print("Similarity Score:", defect["similarity_score"])
    print("Root Cause:", defect["root_cause"])
    print("Resolution:", defect["resolution"])

print("\n===================================")