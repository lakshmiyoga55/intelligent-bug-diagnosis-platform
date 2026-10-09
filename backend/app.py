import json
import os
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

from backend.log_analysis import analyze_log

from backend.agents.root_cause_agent import root_cause_analysis
from backend.agents.duplicate_detection_agent import detect_duplicates
from backend.agents.remediation_agent import generate_remediation

from backend.diagnosis_report import create_diagnosis_report
from backend.analytics import generate_analytics


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)
CORS(app)


# =========================================================
# OPENAI CLIENT
# =========================================================

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key
) if api_key else None


# =========================================================
# SAVE SUBMITTED BUG
# =========================================================

def save_submitted_bug(bug_data):

    file_path = "submitted_bugs.json"

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            bugs = json.load(file)

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):

        bugs = []

    bugs.append(bug_data)

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            bugs,
            file,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# TRIAGE AGENT
# =========================================================

def triage_bug(
    bug_title,
    bug_description,
    stack_trace,
    error_logs,
    programming_language
):

    combined_text = " ".join([
        bug_title or "",
        bug_description or "",
        stack_trace or "",
        error_logs or ""
    ]).lower()


    # =====================================================
    # LOGIN / AUTHENTICATION
    # =====================================================

    login_keywords = [
        "login",
        "authentication",
        "authenticate",
        "sign in",
        "signin",
        "user object",
        "credential"
    ]

    null_keywords = [
        "nullpointerexception",
        "null pointer",
        "user object is null",
        "null user"
    ]

    if (
        any(
            word in combined_text
            for word in login_keywords
        )
        and
        any(
            word in combined_text
            for word in null_keywords
        )
    ):

        return {

            "severity": "High",

            "priority": "P1",

            "affected_component":
                "Authentication/Login",

            "confidence": 0.92,

            "reasoning": (
                "The bug causes application failure during "
                "user authentication and is associated with "
                "a null user object. This directly blocks "
                "login functionality."
            ),

            "evidence_type":
                "Structured Rule + Bug Evidence"
        }


    # =====================================================
    # PAYMENT / DATABASE
    # =====================================================

    payment_keywords = [
        "payment",
        "transaction",
        "checkout"
    ]

    database_keywords = [
        "sqlexception",
        "database",
        "db",
        "connection",
        "connection refused",
        "database unavailable"
    ]

    if (
        any(
            word in combined_text
            for word in payment_keywords
        )
        and
        any(
            word in combined_text
            for word in database_keywords
        )
    ):

        return {

            "severity": "Critical",

            "priority": "P0",

            "affected_component":
                "Payment",

            "confidence": 0.90,

            "reasoning": (
                "The failure affects payment processing and "
                "is associated with database connectivity, "
                "which can prevent financial transactions "
                "from completing."
            ),

            "evidence_type":
                "Structured Rule + Bug Evidence"
        }


    # =====================================================
    # REGISTRATION / VALIDATION
    # =====================================================

    registration_keywords = [
        "registration",
        "register",
        "signup",
        "sign up",
        "email"
    ]

    validation_keywords = [
        "validationexception",
        "validation",
        "empty email",
        "missing email",
        "invalid email"
    ]

    if (
        any(
            word in combined_text
            for word in registration_keywords
        )
        and
        any(
            word in combined_text
            for word in validation_keywords
        )
    ):

        return {

            "severity": "Medium",

            "priority": "P2",

            "affected_component":
                "User Registration",

            "confidence": 0.89,

            "reasoning": (
                "The defect affects user registration and "
                "indicates an input validation failure."
            ),

            "evidence_type":
                "Structured Rule + Bug Evidence"
        }


    # =====================================================
    # DASHBOARD / TIMEOUT
    # =====================================================

    dashboard_keywords = [
        "dashboard",
        "dashboard api"
    ]

    timeout_keywords = [
        "timeoutexception",
        "timeout",
        "timed out"
    ]

    if (
        any(
            word in combined_text
            for word in dashboard_keywords
        )
        and
        any(
            word in combined_text
            for word in timeout_keywords
        )
    ):

        return {

            "severity": "High",

            "priority": "P1",

            "affected_component":
                "Dashboard",

            "confidence": 0.90,

            "reasoning": (
                "The dashboard request is timing out, "
                "preventing the dashboard from loading "
                "successfully."
            ),

            "evidence_type":
                "Structured Rule + Bug Evidence"
        }


    # =====================================================
    # SEARCH
    # =====================================================

    search_keywords = [
        "search",
        "keyword",
        "search results"
    ]

    if any(
        word in combined_text
        for word in search_keywords
    ):

        return {

            "severity": "Medium",

            "priority": "P2",

            "affected_component":
                "Search",

            "confidence": 0.85,

            "reasoning": (
                "The reported issue affects search behaviour "
                "and may result in incorrect or incomplete "
                "search results."
            ),

            "evidence_type":
                "Structured Rule + Bug Evidence"
        }


    # =====================================================
    # OPENAI FALLBACK
    # =====================================================

    if client is None:

        return {

            "severity": "Medium",

            "priority": "P2",

            "affected_component":
                "Application",

            "confidence": 0.70,

            "reasoning": (
                "The issue was classified using structured "
                "bug information because live LLM analysis "
                "was unavailable."
            ),

            "evidence_type":
                "Structured Fallback"
        }


    prompt = f"""
You are a software bug triage agent.

Analyze the following bug.

Title:
{bug_title}

Programming Language:
{programming_language}

Description:
{bug_description}

Stack Trace:
{stack_trace}

Error Logs:
{error_logs}

Return ONLY valid JSON:

{{
    "severity": "Critical/High/Medium/Low",
    "priority": "P0/P1/P2/P3",
    "affected_component": "Component name",
    "confidence": 0.0,
    "reasoning": "Short explanation"
}}
"""

    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        result_text = (
            response
            .output_text
            .strip()
        )

        result_text = result_text.replace(
            "```json",
            ""
        )

        result_text = result_text.replace(
            "```",
            ""
        )

        result_text = result_text.strip()

        result = json.loads(
            result_text
        )

        result["evidence_type"] = (
            "LLM Analysis"
        )

        return result

    except Exception:

        return {

            "severity": "Medium",

            "priority": "P2",

            "affected_component":
                "Application",

            "confidence": 0.70,

            "reasoning": (
                "The issue was classified using structured "
                "bug information because live LLM analysis "
                "was unavailable."
            ),

            "evidence_type":
                "Structured Fallback"
        }


# =========================================================
# TRIAGE API
# =========================================================

@app.route(
    "/api/triage",
    methods=["POST"]
)
def triage():

    data = request.get_json() or {}

    result = triage_bug(

        data.get(
            "bug_title",
            ""
        ),

        data.get(
            "bug_description",
            ""
        ),

        data.get(
            "stack_trace",
            ""
        ),

        data.get(
            "error_logs",
            ""
        ),

        data.get(
            "programming_language",
            "Unknown"
        )
    )

    return jsonify(result)


# =========================================================
# LOG ANALYSIS API
# =========================================================

@app.route(
    "/api/log-analysis",
    methods=["POST"]
)
def log_analysis_api():

    data = request.get_json() or {}

    result = analyze_log(

        data.get(
            "stack_trace",
            ""
        ),

        data.get(
            "error_logs",
            ""
        ),

        data.get(
            "programming_language",
            "Unknown"
        )
    )

    return jsonify(result)


# =========================================================
# COMPLETE DIAGNOSIS
# =========================================================

@app.route(
    "/api/diagnose",
    methods=["POST"]
)
def diagnose():

    data = request.get_json() or {}


    # -----------------------------------------------------
    # INPUT
    # -----------------------------------------------------

    bug_title = data.get(
        "bug_title",
        ""
    )

    programming_language = data.get(
        "programming_language",
        "Unknown"
    )

    bug_description = data.get(
        "bug_description",
        ""
    )

    stack_trace = data.get(
        "stack_trace",
        ""
    )

    error_logs = data.get(
        "error_logs",
        ""
    )


    # -----------------------------------------------------
    # TRIAGE
    # -----------------------------------------------------

    triage_result = triage_bug(

        bug_title,

        bug_description,

        stack_trace,

        error_logs,

        programming_language
    )


    # -----------------------------------------------------
    # LOG ANALYSIS
    # -----------------------------------------------------

    log_result = analyze_log(

        stack_trace,

        error_logs,

        programming_language
    )


    # -----------------------------------------------------
    # STRUCTURED BUG DATA
    # -----------------------------------------------------

    bug_data = {

        "bug_title":
            bug_title,

        "programming_language":
            programming_language,

        "bug_description":
            bug_description,

        "stack_trace":
            stack_trace,

        "error_logs":
            error_logs,

        "severity":
            triage_result.get(
                "severity",
                "Unknown"
            ),

        "priority":
            triage_result.get(
                "priority",
                "Unknown"
            ),

        "affected_component":
            triage_result.get(
                "affected_component",
                "Unknown"
            ),

        "exception_type":
            log_result.get(
                "exception_type",
                ""
            ),

        "error_message":
            log_result.get(
                "error_message",
                ""
            ),

        "failure_point":
            log_result.get(
                "failure_point",
                ""
            ),

        "code_path":
            log_result.get(
                "affected_code_path",
                ""
            ),

        "timestamp":
            datetime.now().isoformat()
    }


    # -----------------------------------------------------
    # ROOT CAUSE
    # -----------------------------------------------------

    root_cause_result = root_cause_analysis(
        bug_data
    )


    # -----------------------------------------------------
    # DUPLICATE DETECTION
    # -----------------------------------------------------

    duplicate_result = detect_duplicates(
        bug_data
    )


    # -----------------------------------------------------
    # REMEDIATION
    # -----------------------------------------------------

    remediation_result = generate_remediation(

        bug_data,

        root_cause_result,

        duplicate_result
    )


    # -----------------------------------------------------
    # ADD FINAL ANALYSIS TO BUG DATA
    # -----------------------------------------------------

    bug_data["duplicate_status"] = (
        duplicate_result.get(
            "status",
            "Unknown"
        )
    )

    bug_data["duplicate_explanation"] = (
        duplicate_result.get(
            "explanation",
            ""
        )
    )

    bug_data["root_cause"] = (
        root_cause_result.get(
            "root_cause",
            "Unknown"
        )
    )

    bug_data["root_cause_confidence"] = (
        root_cause_result.get(
            "confidence",
            0
        )
    )

    bug_data["root_cause_evidence_type"] = (
        root_cause_result.get(
            "evidence_type",
            "Unknown"
        )
    )

    bug_data["resolution"] = (
        remediation_result.get(
            "recommended_fix",
            "Unknown"
        )
    )

    bug_data["resolution_confidence"] = (
        remediation_result.get(
            "confidence",
            0
        )
    )

    bug_data["resolution_evidence_type"] = (
        remediation_result.get(
            "evidence_type",
            "Unknown"
        )
    )


    # -----------------------------------------------------
    # SAVE COMPLETE BUG RECORD
    # -----------------------------------------------------

    save_submitted_bug(
        bug_data
    )


    # -----------------------------------------------------
    # STRUCTURED REPORT
    # -----------------------------------------------------

    diagnosis_report = create_diagnosis_report(

        bug_data,

        triage_result,

        log_result,

        root_cause_result,

        duplicate_result,

        remediation_result
    )


    # -----------------------------------------------------
    # FINAL RESPONSE
    # -----------------------------------------------------

    return jsonify({

        "success":
            True,

        "agent":
            "Multi-Agent Orchestrator",

        "pipeline": [

            "Bug Submission",

            "Triage Agent",

            "Log Analysis Agent",

            "Root Cause Agent",

            "Duplicate Detection Agent",

            "Remediation Agent",

            "Structured Diagnosis Report"
        ],

        "triage_analysis":
            triage_result,

        "log_analysis":
            log_result,

        "root_cause_analysis":
            root_cause_result,

        "duplicate_detection":
            duplicate_result,

        "remediation":
            remediation_result,

        "diagnosis_report":
            diagnosis_report
    })


# =========================================================
# ANALYTICS API
# =========================================================

@app.route(
    "/api/analytics",
    methods=["GET"]
)
def analytics():

    try:

        filters = {

            "component":
                request.args.get(
                    "component"
                ),

            "severity":
                request.args.get(
                    "severity"
                ),

            "priority":
                request.args.get(
                    "priority"
                ),

            "exception_type":
                request.args.get(
                    "exception_type"
                ),

            "start_date":
                request.args.get(
                    "start_date"
                ),

            "end_date":
                request.args.get(
                    "end_date"
                )
        }

        result = generate_analytics(
            filters
        )

        return jsonify({

            "success":
                True,

            "analytics":
                result

        })

    except Exception as e:

        return jsonify({

            "success":
                False,

            "error":
                str(e)

        }), 500


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return jsonify({

        "message":
            "Intelligent Bug Diagnosis Platform Backend is running",

        "status":
            "running",

        "architecture":
            "Multi-Agent Bug Diagnosis Pipeline"
    })


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )