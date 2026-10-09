import os
import json
import re

from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key
) if api_key else None


# =========================================================
# LOG ANALYSIS AGENT
# =========================================================

def analyze_log(
    stack_trace,
    error_logs="",
    programming_language="Unknown"
):

    stack_trace = stack_trace or ""
    error_logs = error_logs or ""

    combined_log = (
        stack_trace
        + "\n"
        + error_logs
    ).strip()


    # =====================================================
    # NO LOG PROVIDED
    # =====================================================

    if not combined_log:

        return {
            "success": False,
            "exception_type": "Not identified",
            "error_message": "Not identified",
            "file": "Not identified",
            "class": "Not identified",
            "method": "Not identified",
            "line": "Not identified",
            "failure_point": "Not identified",
            "affected_code_path": "Not identified",
            "confidence": 0
        }


    # =====================================================
    # LOCAL LOG PARSING
    # =====================================================

    exception_type = "Not identified"
    error_message = "Not identified"
    file_name = "Not identified"
    class_name = "Not identified"
    method_name = "Not identified"
    line_number = "Not identified"
    failure_point = "Not identified"
    code_path = "Not identified"


    # =====================================================
    # EXCEPTION TYPE
    # =====================================================

    exception_patterns = [
        r'([A-Za-z0-9_$.]+Exception)',
        r'([A-Za-z0-9_$.]+Error)'
    ]

    for pattern in exception_patterns:

        match = re.search(
            pattern,
            combined_log
        )

        if match:

            exception_type = match.group(1)

            break


    # =====================================================
    # ERROR MESSAGE
    # =====================================================

    if "user object is null" in combined_log.lower():

        error_message = "User object is null"

    elif exception_type != "Not identified":

        lines = combined_log.splitlines()

        for line in lines:

            if exception_type in line:

                parts = line.split(
                    exception_type,
                    1
                )

                if len(parts) > 1:

                    message = parts[1].strip()

                    if message:

                        error_message = message

                break


    # =====================================================
    # JAVA STACK TRACE
    #
    # Example:
    # at LoginService.authenticate(LoginService.java:25)
    # =====================================================

    java_pattern = (
        r'at\s+'
        r'([A-Za-z0-9_$.]+)'
        r'\.([A-Za-z0-9_]+)'
        r'\(([^:]+):(\d+)\)'
    )

    matches = re.findall(
        java_pattern,
        combined_log
    )


    if matches:

        first_match = matches[0]

        full_class = first_match[0]
        method_name = first_match[1]
        file_name = first_match[2]
        line_number = first_match[3]


        # -------------------------------------------------
        # CLASS NAME
        # -------------------------------------------------

        if "." in full_class:

            class_name = full_class.split(".")[-1]

        else:

            class_name = full_class


        # -------------------------------------------------
        # FAILURE POINT
        # -------------------------------------------------

        failure_point = (
            f"{class_name}.{method_name}() "
            f"at line {line_number}"
        )


        # -------------------------------------------------
        # COMPLETE CODE PATH
        # -------------------------------------------------

        path_parts = []

        for match in matches:

            path_class = match[0]
            path_method = match[1]

            path_parts.append(
                f"{path_class}.{path_method}()"
            )


        code_path = " → ".join(
            path_parts
        )


    # =====================================================
    # LOWERCASE LOG
    # =====================================================

    lower_log = combined_log.lower()


    # =====================================================
    # CONFIDENCE
    # =====================================================

    confidence = 0.70


    # =====================================================
    # LOGIN / NULL POINTER
    # =====================================================

    if (
        "nullpointerexception" in lower_log
        and
        (
            "login" in lower_log
            or
            "authenticate" in lower_log
            or
            "user object" in lower_log
        )
    ):

        exception_type = "NullPointerException"

        error_message = "User object is null"


        if matches:

            first_match = matches[0]

            failure_point = (
                f"{first_match[0]}.{first_match[1]}()"
            )


        code_path = " → ".join(
            [
                f"{match[0]}.{match[1]}()"
                for match in matches
            ]
        )


        confidence = 0.95


    # =====================================================
    # DATABASE ERROR
    # =====================================================

    elif (
        "sqlexception" in lower_log
        or
        "database" in lower_log
        or
        "connection refused" in lower_log
    ):

        if exception_type == "Not identified":

            exception_type = "SQLException"


        if error_message == "Not identified":

            error_message = "Database connection failure"


        confidence = 0.90


    # =====================================================
    # TIMEOUT
    # =====================================================

    elif (
        "timeout" in lower_log
        or
        "timed out" in lower_log
    ):

        if exception_type == "Not identified":

            exception_type = "TimeoutException"


        if error_message == "Not identified":

            error_message = "Request timed out"


        confidence = 0.90


    # =====================================================
    # VALIDATION
    # =====================================================

    elif (
        "validationexception" in lower_log
        or
        "validation" in lower_log
    ):

        if exception_type == "Not identified":

            exception_type = "ValidationException"


        if error_message == "Not identified":

            error_message = "Input validation failed"


        confidence = 0.88


    # =====================================================
    # LOCAL RESULT
    # =====================================================

    local_result = {

        "success": True,

        "exception_type":
            exception_type,

        "error_message":
            error_message,

        "file":
            file_name,

        "class":
            class_name,

        "method":
            method_name,

        "line":
            line_number,

        "failure_point":
            failure_point,

        "affected_code_path":
            code_path,

        "confidence":
            confidence,

        "evidence_type":
            "Stack Trace + Error Log Parsing"
    }


    # =====================================================
    # OPENAI ENHANCEMENT
    # =====================================================

    prompt = f"""
You are a Log Analysis Agent.

Analyze this software error.

Programming Language:
{programming_language}

Stack Trace:
{stack_trace}

Error Logs:
{error_logs}

Return ONLY valid JSON:

{{
    "exception_type": "",
    "error_message": "",
    "file": "",
    "class": "",
    "method": "",
    "line": "",
    "failure_point": "",
    "affected_code_path": "",
    "confidence": 0.0
}}
"""


    # =====================================================
    # USE LLM ONLY IF API KEY EXISTS
    # =====================================================

    if client is None:

        return local_result


    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )


        result_text = response.output_text.strip()


        result_text = result_text.replace(
            "```json",
            ""
        )

        result_text = result_text.replace(
            "```",
            ""
        )

        result_text = result_text.strip()


        analysis = json.loads(
            result_text
        )


        return {

            "success": True,

            **analysis,

            "evidence_type":
                "LLM Log Analysis"
        }


    except Exception:

        # =================================================
        # OPENAI UNAVAILABLE
        # USE LOCAL ANALYSIS
        # =================================================

        return local_result