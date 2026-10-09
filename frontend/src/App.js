import React, { useEffect, useState } from "react";
import "./App.css";

const BACKEND_URL = "http://127.0.0.1:5000";

function App() {
  const [page, setPage] = useState("home");
  const [diagnosisResult, setDiagnosisResult] = useState(null);

  const [darkMode, setDarkMode] = useState(() => {
    const savedTheme = localStorage.getItem("bug-platform-theme");
    return savedTheme === "dark";
  });

  useEffect(() => {
    document.body.classList.toggle("dark-mode", darkMode);
    localStorage.setItem(
      "bug-platform-theme",
      darkMode ? "dark" : "light"
    );
  }, [darkMode]);

  const goToSubmit = () => {
    setPage("submit");
  };

  const goHome = () => {
    setPage("home");
  };

  const handleDiagnosisResult = (result) => {
    setDiagnosisResult(result);
    setPage("result");
  };

  return (
    <div className={`app ${darkMode ? "dark-theme" : "light-theme"}`}>
      {/* ================= NAVBAR ================= */}

      <nav className="navbar">
        <div className="nav-logo" onClick={goHome}>
          Intelligent Bug Diagnosis Platform
        </div>

        <div className="nav-links">
          <button onClick={goHome}>Home</button>

          <button onClick={() => setPage("features")}>
            Features
          </button>

          <button onClick={() => setPage("about")}>
            About
          </button>

          <button onClick={() => setPage("analytics")}>
            Analytics
          </button>

          <button
            className="theme-toggle"
            onClick={() => setDarkMode((previous) => !previous)}
            title={
              darkMode
                ? "Switch to Light Mode"
                : "Switch to Dark Mode"
            }
          >
            {darkMode ? "☀️ Light" : "🌙 Dark"}
          </button>

          <button
            className="nav-submit"
            onClick={goToSubmit}
          >
            Submit Bug
          </button>
        </div>
      </nav>

      {/* ================= PAGES ================= */}

      {page === "home" && (
        <HomePage
          onSubmit={goToSubmit}
          onFeatures={() => setPage("features")}
        />
      )}

      {page === "features" && <FeaturesPage />}

      {page === "about" && <AboutPage />}

      {page === "analytics" && <AnalyticsPage />}

      {page === "submit" && (
        <BugSubmissionPage
          onBack={goHome}
          onResult={handleDiagnosisResult}
        />
      )}

      {page === "result" && (
        <DiagnosisResult
          result={diagnosisResult}
          onBack={goToSubmit}
        />
      )}

      <Footer />
    </div>
  );
}


/* =================================================
   HOME PAGE
================================================= */

function HomePage({ onSubmit, onFeatures }) {
  return (
    <>
      <section className="hero">
        <div className="hero-content">
          <span className="hero-badge">
            AI-POWERED SOFTWARE DEBUGGING
          </span>

          <h1>
            Intelligent Bug
            <br />
            Diagnosis Platform
          </h1>

          <p>
            Automatically analyze software bugs using
            a multi-agent AI diagnosis workflow.
          </p>

          <div className="hero-buttons">
            <button
              className="primary-btn"
              onClick={onSubmit}
            >
              Submit a Bug →
            </button>

            <button
              className="secondary-btn"
              onClick={onFeatures}
            >
              Explore Features
            </button>
          </div>
        </div>
      </section>

      <section className="home-section">
        <h2>How It Works</h2>

        <p className="section-subtitle">
          From bug submission to actionable fix recommendations.
        </p>

        <div className="workflow-grid">
          <WorkflowCard
            number="01"
            title="Bug Submission"
            description="Submit bug descriptions, stack traces, error logs and bug reports."
          />

          <WorkflowCard
            number="02"
            title="Triage Agent"
            description="Classifies severity, priority and affected software component."
          />

          <WorkflowCard
            number="03"
            title="Log Analysis"
            description="Extracts exception type, error message and failure point."
          />

          <WorkflowCard
            number="04"
            title="Root Cause"
            description="Uses historical evidence to identify the probable root cause."
          />

          <WorkflowCard
            number="05"
            title="Duplicate Detection"
            description="Finds similar historical bugs and determines duplicate status."
          />

          <WorkflowCard
            number="06"
            title="Remediation"
            description="Provides actionable recommendations using historical resolutions."
          />
        </div>
      </section>
    </>
  );
}


/* =================================================
   WORKFLOW CARD
================================================= */

function WorkflowCard({
  number,
  title,
  description
}) {
  return (
    <div className="workflow-card">
      <div className="workflow-number">
        {number}
      </div>

      <h3>{title}</h3>

      <p>{description}</p>
    </div>
  );
}


/* =================================================
   FEATURES PAGE
================================================= */

function FeaturesPage() {
  const features = [
    {
      icon: "🐞",
      title: "Bug Submission",
      description:
        "Submit bug descriptions, stack traces, error logs and supported bug report files."
    },
    {
      icon: "🎯",
      title: "Triage Agent",
      description:
        "Automatically determine severity, priority and affected component."
    },
    {
      icon: "📋",
      title: "Log Analysis",
      description:
        "Extract exception details, failure points and affected code paths."
    },
    {
      icon: "🔍",
      title: "Root Cause Analysis",
      description:
        "Use historical defect evidence to identify probable root causes."
    },
    {
      icon: "🔄",
      title: "Duplicate Detection",
      description:
        "Compare the current bug against historical defects."
    },
    {
      icon: "🛠️",
      title: "Remediation",
      description:
        "Generate actionable fix recommendations using historical resolutions."
    }
  ];

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Platform Features</h1>

        <p>
          A multi-agent workflow for structured
          software defect diagnosis.
        </p>
      </div>

      <div className="features-grid">
        {features.map((feature, index) => (
          <div
            className="feature-card"
            key={index}
          >
            <div className="feature-icon">
              {feature.icon}
            </div>

            <h3>{feature.title}</h3>

            <p>{feature.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}


/* =================================================
   ABOUT PAGE
================================================= */

function AboutPage() {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1>About the Platform</h1>

        <p>
          Intelligent software defect diagnosis using
          a multi-agent architecture.
        </p>
      </div>

      <div className="about-card">
        <h2>
          Intelligent Bug Diagnosis Platform
        </h2>

        <p>
          This platform analyzes software defects through
          multiple specialized agents. Each agent performs
          a specific diagnosis task and passes structured
          information to the next stage.
        </p>

        <p>
          Historical defect information is used to identify
          similar bugs, probable root causes and previously
          used resolutions.
        </p>

        <div className="architecture-box">
          <h3>Architecture Flow</h3>

          <div className="architecture-flow">
            <span>Bug Submission</span>
            <span>→</span>
            <span>Triage</span>
            <span>→</span>
            <span>Log Analysis</span>
            <span>→</span>
            <span>Root Cause</span>
            <span>→</span>
            <span>Duplicate Detection</span>
            <span>→</span>
            <span>Remediation</span>
          </div>
        </div>
      </div>
    </div>
  );
}


/* =================================================
   BUG SUBMISSION PAGE
================================================= */

function BugSubmissionPage({
  onBack,
  onResult
}) {
  const [formData, setFormData] = useState({
    bug_title: "",
    programming_language: "Java",
    bug_description: "",
    stack_trace: "",
    error_logs: ""
  });

  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (event) => {
    const {
      name,
      value
    } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value
    }));
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    setSelectedFile(file);

    const reader = new FileReader();

    reader.onload = (e) => {
      const content = e.target.result;
      const fileName = file.name.toLowerCase();

      if (
        fileName.endsWith(".stacktrace") ||
        fileName.endsWith(".trace")
      ) {
        setFormData((previous) => ({
          ...previous,
          stack_trace: content
        }));
      } else if (
        fileName.endsWith(".log")
      ) {
        setFormData((previous) => ({
          ...previous,
          error_logs: content
        }));
      } else {
        setFormData((previous) => ({
          ...previous,
          bug_description: content
        }));
      }
    };

    reader.readAsText(file);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");

    if (!formData.bug_title.trim()) {
      setError("Please enter the bug title.");
      return;
    }

    if (!formData.bug_description.trim()) {
      setError("Please enter the bug description.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        `${BACKEND_URL}/api/diagnose`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(formData)
        }
      );

      if (!response.ok) {
        let message =
          `Server error: ${response.status}`;

        try {
          const errorData =
            await response.json();

          if (errorData.error) {
            message = errorData.error;
          }

          if (errorData.message) {
            message = errorData.message;
          }
        } catch {
          // Ignore JSON parsing error
        }

        throw new Error(message);
      }

      const data =
        await response.json();

      if (data.success === false) {
        throw new Error(
          data.message ||
          data.error ||
          "Diagnosis failed."
        );
      }

      onResult(data);

    } catch (err) {
      console.error(
        "Diagnosis request failed:",
        err
      );

      if (
        err instanceof TypeError &&
        err.message === "Failed to fetch"
      ) {
        setError(
          "Cannot connect to the backend. Please make sure Flask is running at http://127.0.0.1:5000"
        );
      } else {
        setError(
          err.message ||
          "Unable to process the diagnosis."
        );
      }

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bug-page">
      <div className="bug-container">
        <div className="bug-header">
          <h1>
            Submit a Bug for Diagnosis
          </h1>

          <p>
            Provide the bug details below to run the
            complete multi-agent diagnosis workflow.
          </p>
        </div>

        <form
          className="bug-form"
          onSubmit={handleSubmit}
        >
          {error && (
            <div className="form-error">
              ❌ {error}
            </div>
          )}

          <div className="form-group">
            <label>Bug Title *</label>

            <input
              type="text"
              name="bug_title"
              value={formData.bug_title}
              onChange={handleChange}
              placeholder="Enter bug title"
            />
          </div>

          <div className="form-group">
            <label>
              Programming Language *
            </label>

            <select
              name="programming_language"
              value={formData.programming_language}
              onChange={handleChange}
            >
              <option value="Java">Java</option>
              <option value="Python">Python</option>
              <option value="JavaScript">JavaScript</option>
              <option value="C++">C++</option>
              <option value="C#">C#</option>
            </select>
          </div>

          <div className="form-group">
            <label>
              Upload Bug Report / Error Log
            </label>

            <div className="file-upload-box">
              <label
                className="file-upload-label"
                htmlFor="bug-file"
              >
                📁 Choose Bug / Log File
              </label>

              <input
                id="bug-file"
                type="file"
                accept=".txt,.log,.stacktrace,.trace"
                onChange={handleFileChange}
              />

              <p>
                Supported files:
                .txt, .log, .stacktrace, .trace
              </p>

              {selectedFile && (
                <div className="upload-success">
                  ✓ {selectedFile.name}
                </div>
              )}
            </div>
          </div>

          <div className="form-group">
            <label>Bug Description *</label>

            <textarea
              name="bug_description"
              value={formData.bug_description}
              onChange={handleChange}
              placeholder="Describe the bug..."
            />
          </div>

          <div className="form-group">
            <label>Stack Trace</label>

            <textarea
              name="stack_trace"
              value={formData.stack_trace}
              onChange={handleChange}
              placeholder="Paste stack trace here..."
            />
          </div>

          <div className="form-group">
            <label>Error Logs</label>

            <textarea
              name="error_logs"
              value={formData.error_logs}
              onChange={handleChange}
              placeholder="Paste error logs here..."
            />
          </div>

          <div className="bug-actions">
            <button
              type="button"
              className="back-btn"
              onClick={onBack}
              disabled={loading}
            >
              ← Back
            </button>

            <button
              type="submit"
              className="submit-btn"
              disabled={loading}
            >
              {loading
                ? "Analyzing..."
                : "Submit Bug →"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}


/* =================================================
   DIAGNOSIS RESULT
================================================= */

function DiagnosisResult({
  result,
  onBack
}) {
  if (!result) {
    return (
      <div className="result-page">
        <div className="result-container">
          <div className="result-empty">
            <h2>No Diagnosis Result</h2>

            <p>
              Please submit a bug to generate
              the diagnosis report.
            </p>

            <button
              className="submit-btn"
              onClick={onBack}
            >
              Submit a Bug
            </button>
          </div>
        </div>
      </div>
    );
  }

  const report =
    result.diagnosis_report ||
    result;

  const bug =
    report.bug ||
    result.bug ||
    {};

  const triage =
    report.triage ||
    result.triage_analysis ||
    result.triage ||
    {};

  const log =
    report.log_analysis ||
    result.log_analysis ||
    {};

  const rootCause =
    report.root_cause ||
    result.root_cause_analysis ||
    result.root_cause ||
    {};

  const duplicate =
    report.duplicate_detection ||
    result.duplicate_detection ||
    {};

  const remediation =
    report.remediation ||
    result.remediation ||
    {};

  return (
    <div className="result-page">
      <div className="result-container">

        <div className="result-header">
          <div>
            <span className="result-badge">
              AI DIAGNOSIS REPORT
            </span>

            <h1>Bug Diagnosis Result</h1>

            <p>
              Structured analysis generated by
              the multi-agent diagnosis pipeline.
            </p>
          </div>

          <button
            className="back-btn"
            onClick={onBack}
          >
            ← Submit Another Bug
          </button>
        </div>


        {/* BUG */}

        <section className="result-section">
          <div className="result-section-title">
            <span className="section-icon">
              🐞
            </span>

            <div>
              <h2>Bug Details</h2>

              <p>
                Original submitted bug information
              </p>
            </div>
          </div>

          <div className="result-grid">
            <div className="result-item">
              <span>Bug Title</span>

              <strong>
                {bug.bug_title || "Not provided"}
              </strong>
            </div>

            <div className="result-item">
              <span>Programming Language</span>

              <strong>
                {bug.programming_language || "Unknown"}
              </strong>
            </div>

            <div className="result-item result-wide">
              <span>Description</span>

              <p>
                {bug.description ||
                  bug.bug_description ||
                  "No description"}
              </p>
            </div>
          </div>
        </section>


        {/* TRIAGE */}

        <section className="result-section">
          <div className="result-section-title">
            <span className="section-icon">
              🎯
            </span>

            <div>
              <h2>Triage Analysis</h2>

              <p>
                Severity, priority and component
              </p>
            </div>
          </div>

          <div className="analysis-cards">
            <div className="analysis-card">
              <span className="analysis-label">
                Severity
              </span>

              <strong className="analysis-value severity-value">
                {triage.severity || "Unknown"}
              </strong>
            </div>

            <div className="analysis-card">
              <span className="analysis-label">
                Priority
              </span>

              <strong className="analysis-value">
                {triage.priority || "Unknown"}
              </strong>
            </div>

            <div className="analysis-card">
              <span className="analysis-label">
                Component
              </span>

              <strong className="analysis-value">
                {triage.affected_component || "Unknown"}
              </strong>
            </div>

            <div className="analysis-card">
              <span className="analysis-label">
                Confidence
              </span>

              <strong className="analysis-value confidence-value">
                {formatConfidence(triage.confidence)}
              </strong>
            </div>
          </div>

          {triage.reasoning && (
            <div className="reasoning-box">
              <h3>🧠 Reasoning</h3>

              <p>{triage.reasoning}</p>
            </div>
          )}
        </section>


        {/* LOG ANALYSIS */}

        <section className="result-section">
          <div className="result-section-title">
            <span className="section-icon">
              📋
            </span>

            <div>
              <h2>Log Analysis</h2>

              <p>
                Exception and stack trace analysis
              </p>
            </div>
          </div>

          <div className="result-grid">
            <ResultItem
              label="Exception Type"
              value={log.exception_type}
            />

            <ResultItem
              label="Error Message"
              value={log.error_message}
            />

            <ResultItem
              label="File"
              value={log.file}
            />

            <ResultItem
              label="Class"
              value={log.class}
            />

            <ResultItem
              label="Method"
              value={log.method}
            />

            <ResultItem
              label="Line"
              value={log.line}
            />

            <ResultItem
              label="Failure Point"
              value={log.failure_point}
              wide
            />

            <ResultItem
              label="Affected Code Path"
              value={log.affected_code_path}
              wide
            />
          </div>
        </section>


        {/* ROOT CAUSE */}

        <section className="result-section">
          <div className="result-section-title">
            <span className="section-icon">
              🔍
            </span>

            <div>
              <h2>Root Cause Analysis</h2>

              <p>
                Probable root cause from available evidence
              </p>
            </div>
          </div>

          <div className="result-highlight">
            <span>Probable Root Cause</span>

            <h3>
              {rootCause.root_cause ||
                rootCause.conclusion ||
                "Insufficient Evidence"}
            </h3>
          </div>

          {rootCause.reasoning && (
            <div className="reasoning-box">
              <h3>🧠 Reasoning</h3>

              <p>{rootCause.reasoning}</p>
            </div>
          )}
        </section>


        {/* DUPLICATE */}

        <section className="result-section">
          <div className="result-section-title">
            <span className="section-icon">
              🔄
            </span>

            <div>
              <h2>Duplicate Detection</h2>

              <p>
                Historical defect similarity analysis
              </p>
            </div>
          </div>

          <div className="duplicate-summary">
            <span>Status</span>

            <div className="duplicate-status">
              {duplicate.status || "New"}
            </div>
          </div>

          {duplicate.matches &&
            duplicate.matches.length > 0 && (
              <div className="evidence-box">
                <h3>
                  Matching Historical Bugs
                </h3>

                {duplicate.matches.map(
                  (match, index) => (
                    <div
                      className="evidence-item"
                      key={index}
                    >
                      <div>
                        <span>Bug ID</span>

                        <strong>
                          {match.bug_id}
                        </strong>
                      </div>

                      <div>
                        <span>Status</span>

                        <strong>
                          {match.status}
                        </strong>
                      </div>

                      <div>
                        <span>Similarity</span>

                        <strong>
                          {formatSimilarity(
                            match.similarity_score
                          )}
                        </strong>
                      </div>

                      <div>
                        <span>Resolution</span>

                        <p>
                          {match.resolution ||
                            "No resolution"}
                        </p>
                      </div>
                    </div>
                  )
                )}
              </div>
            )}
        </section>


        {/* REMEDIATION */}

        <section className="result-section">
          <div className="result-section-title">
            <span className="section-icon">
              🛠️
            </span>

            <div>
              <h2>
                Remediation Recommendation
              </h2>

              <p>
                Recommended corrective action
              </p>
            </div>
          </div>

          <div className="fix-box">
            <span>Recommended Fix</span>

            <p>
              {remediation.recommended_fix ||
                "Insufficient Evidence"}
            </p>
          </div>

          <div className="confidence-box">
            <span>Confidence</span>

            <strong>
              {formatConfidence(
                remediation.confidence
              )}
            </strong>
          </div>
        </section>


        {/* PIPELINE */}

        <section className="result-section">
          <div className="result-section-title">
            <span className="section-icon">
              ⚙️
            </span>

            <div>
              <h2>Diagnosis Pipeline</h2>

              <p>
                Multi-agent processing workflow
              </p>
            </div>
          </div>

          <div className="pipeline">
            {[
              "Bug Submission",
              "Triage Agent",
              "Log Analysis",
              "Root Cause",
              "Duplicate Detection",
              "Remediation",
              "Structured Report"
            ].map((step, index, array) => (
              <React.Fragment key={step}>
                <div className="pipeline-step">
                  <div className="pipeline-number">
                    {index + 1}
                  </div>

                  <span>{step}</span>
                </div>

                {index < array.length - 1 && (
                  <div className="pipeline-arrow">
                    →
                  </div>
                )}
              </React.Fragment>
            ))}
          </div>
        </section>

      </div>
    </div>
  );
}


/* =================================================
   RESULT ITEM
================================================= */

function ResultItem({
  label,
  value,
  wide = false
}) {
  return (
    <div
      className={
        wide
          ? "result-item result-wide"
          : "result-item"
      }
    >
      <span>{label}</span>

      <strong>
        {value || "Unknown"}
      </strong>
    </div>
  );
}


/* =================================================
   CONFIDENCE
================================================= */

function formatConfidence(value) {
  if (
    value === undefined ||
    value === null ||
    value === ""
  ) {
    return "N/A";
  }

  const number = Number(value);

  if (number <= 1) {
    return `${Math.round(number * 100)}%`;
  }

  return `${Math.round(number)}%`;
}


/* =================================================
   SIMILARITY
================================================= */

function formatSimilarity(value) {
  if (
    value === undefined ||
    value === null ||
    value === ""
  ) {
    return "N/A";
  }

  const number = Number(value);

  if (number <= 1) {
    return `${Math.round(number * 100)}%`;
  }

  return `${Math.round(number)}%`;
}


/* =================================================
   ANALYTICS PAGE
================================================= */

function AnalyticsPage() {
  const [analytics, setAnalytics] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [filters, setFilters] = useState({
    component: "",
    severity: "",
    priority: "",
    exception_type: "",
    start_date: "",
    end_date: ""
  });

  const loadAnalytics = async (
    currentFilters = filters
  ) => {
    setLoading(true);
    setError("");

    try {
      const params =
        new URLSearchParams();

      Object.entries(currentFilters).forEach(
        ([key, value]) => {
          if (value) {
            params.set(key, value);
          }
        }
      );

      const query =
        params.toString();

      const url = query
        ? `${BACKEND_URL}/api/analytics?${query}`
        : `${BACKEND_URL}/api/analytics`;

      const response =
        await fetch(url);

      if (!response.ok) {
        throw new Error(
          "Analytics request failed"
        );
      }

      const data =
        await response.json();

      console.log(
        "Analytics API Response:",
        data
      );

      setAnalytics(
        data.analytics || {}
      );

    } catch (error) {
      console.error(
        "Analytics error:",
        error
      );

      setError(
        "Unable to load analytics data."
      );

    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  const handleFilterChange = (
    event
  ) => {
    const {
      name,
      value
    } = event.target;

    setFilters((previous) => ({
      ...previous,
      [name]: value
    }));
  };

  const applyFilters = () => {
    loadAnalytics(filters);
  };

  const clearFilters = () => {
    const emptyFilters = {
      component: "",
      severity: "",
      priority: "",
      exception_type: "",
      start_date: "",
      end_date: ""
    };

    setFilters(emptyFilters);
    loadAnalytics(emptyFilters);
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="page-header">
          <h1>Analytics</h1>

          <p>
            Loading analytics...
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-container">
        <div className="page-header">
          <h1>Analytics</h1>

          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Bug Analytics</h1>

        <p>
          Analyze recurring defect patterns,
          severity and resolution trends.
        </p>
      </div>


      {/* FILTERS */}

      <div className="analytics-section analytics-filter-section">
        <h2>Analytics Filters</h2>

        <div className="analytics-filter-grid">

          <div className="form-group">
            <label>Component</label>

            <select
              name="component"
              value={filters.component}
              onChange={handleFilterChange}
            >
              <option value="">
                All Components
              </option>

              {(
                analytics?.available_filters
                  ?.components || []
              ).map((component) => (
                <option
                  key={component}
                  value={component}
                >
                  {component}
                </option>
              ))}
            </select>
          </div>


          <div className="form-group">
            <label>Severity</label>

            <select
              name="severity"
              value={filters.severity}
              onChange={handleFilterChange}
            >
              <option value="">
                All Severities
              </option>

              {(
                analytics?.available_filters
                  ?.severities || []
              ).map((severity) => (
                <option
                  key={severity}
                  value={severity}
                >
                  {severity}
                </option>
              ))}
            </select>
          </div>


          <div className="form-group">
            <label>Priority</label>

            <select
              name="priority"
              value={filters.priority}
              onChange={handleFilterChange}
            >
              <option value="">
                All Priorities
              </option>

              {(
                analytics?.available_filters
                  ?.priorities || []
              ).map((priority) => (
                <option
                  key={priority}
                  value={priority}
                >
                  {priority}
                </option>
              ))}
            </select>
          </div>


          <div className="form-group">
            <label>Exception Type</label>

            <select
              name="exception_type"
              value={filters.exception_type}
              onChange={handleFilterChange}
            >
              <option value="">
                All Exception Types
              </option>

              {(
                analytics?.available_filters
                  ?.exception_types || []
              ).map((exceptionType) => (
                <option
                  key={exceptionType}
                  value={exceptionType}
                >
                  {exceptionType}
                </option>
              ))}
            </select>
          </div>


          <div className="form-group">
            <label>Start Date</label>

            <input
              type="date"
              name="start_date"
              value={filters.start_date}
              onChange={handleFilterChange}
            />
          </div>


          <div className="form-group">
            <label>End Date</label>

            <input
              type="date"
              name="end_date"
              value={filters.end_date}
              onChange={handleFilterChange}
            />
          </div>

        </div>


        <div className="analytics-filter-actions">
          <button
            className="submit-btn"
            onClick={applyFilters}
          >
            Apply Filters
          </button>

          <button
            className="back-btn"
            onClick={clearFilters}
          >
            Clear Filters
          </button>
        </div>
      </div>


      {/* SUMMARY */}

      {analytics && (
        <>
          <div className="analytics-summary">
            <AnalyticsCard
              title="Total Bugs"
              value={analytics.total_bugs || 0}
            />

            <AnalyticsCard
              title="Historical Bugs"
              value={analytics.historical_bugs || 0}
            />

            <AnalyticsCard
              title="Submitted Bugs"
              value={analytics.submitted_bugs || 0}
            />

            <AnalyticsCard
              title="Affected Component"
              value={
                Array.isArray(
                  analytics.most_affected_component
                )
                  ? analytics.most_affected_component[0]
                  : analytics.most_affected_component ||
                    "Unknown"
              }
            />
          </div>


          <div className="analytics-section">
            <h2>Exception Frequency</h2>

            <AnalyticsList
              data={analytics.exception_frequency}
            />
          </div>


          <div className="analytics-section">
            <h2>Severity Frequency</h2>

            <AnalyticsList
              data={analytics.severity_frequency}
            />
          </div>


          <div className="analytics-section">
            <h2>Component Frequency</h2>

            <AnalyticsList
              data={analytics.component_frequency}
            />
          </div>


          <div className="analytics-section">
            <h2>Priority Frequency</h2>

            <AnalyticsList
              data={analytics.priority_frequency}
            />
          </div>


          <div className="analytics-section">
            <h2>Duplicate Status</h2>

            <AnalyticsList
              data={analytics.duplicate_status_frequency}
            />
          </div>


          <div className="analytics-section">
            <h2>Root Cause Frequency</h2>

            <AnalyticsList
              data={analytics.root_cause_frequency}
            />
          </div>


          <div className="analytics-section">
            <h2>Resolution Frequency</h2>

            <AnalyticsList
              data={analytics.resolution_frequency}
            />
          </div>


          {/* SEMANTIC CLUSTERS */}

          <div className="analytics-section">
            <h2>Semantic Clusters</h2>

            {analytics.semantic_clusters &&
            analytics.semantic_clusters.length > 0 ? (
              <div className="analytics-list">
                {analytics.semantic_clusters.map(
                  (cluster) => (
                    <div
                      className="analytics-row semantic-cluster-row"
                      key={cluster.cluster_id}
                    >
                      <div>
                        <strong>
                          {cluster.cluster_id} -{" "}
                          {cluster.theme}
                        </strong>

                        <p>
                          {cluster.description}
                        </p>

                        <p>
                          Bug IDs:{" "}
                          {cluster.bug_ids &&
                          cluster.bug_ids.length > 0
                            ? cluster.bug_ids.join(", ")
                            : "None"}
                        </p>

                        <p>
                          Average Similarity:{" "}
                          {cluster.average_similarity}%
                        </p>
                      </div>
                    </div>
                  )
                )}
              </div>
            ) : (
              <p>
                No semantic clusters available.
              </p>
            )}
          </div>


          <div className="analytics-section">
            <h2>Time-Based Analysis</h2>

            <AnalyticsList
              data={analytics.time_analysis}
            />
          </div>
        </>
      )}
    </div>
  );
}


/* =================================================
   ANALYTICS CARD
================================================= */

function AnalyticsCard({
  title,
  value
}) {
  return (
    <div className="analytics-card">
      <h3>{title}</h3>

      <strong>{value}</strong>
    </div>
  );
}


/* =================================================
   ANALYTICS LIST
================================================= */

function AnalyticsList({
  data
}) {
  if (
    !data ||
    Object.keys(data).length === 0
  ) {
    return (
      <p>No data available.</p>
    );
  }

  return (
    <div className="analytics-list">
      {Object.entries(data).map(
        ([key, value]) => (
          <div
            className="analytics-row"
            key={key}
          >
            <span>{key}</span>

            <strong>
              {Array.isArray(value)
                ? value[1]
                : value}
            </strong>
          </div>
        )
      )}
    </div>
  );
}


/* =================================================
   FOOTER
================================================= */

function Footer() {
  return (
    <footer className="footer">
      <h3>
        ◆ Intelligent Bug Diagnosis Platform
      </h3>

      <p>
        Infosys Springboard Internship Project
      </p>

      <p>
        Multi-Agent AI Software Defect Diagnosis
      </p>
    </footer>
  );
}


export default App;