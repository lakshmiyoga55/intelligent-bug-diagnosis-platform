import { useState } from 'react';
import './BugSubmission.css';

function BugSubmission({ onBack, onAnalyze }) {

  const [bugTitle, setBugTitle] = useState('');
  const [programmingLanguage, setProgrammingLanguage] = useState('');
  const [bugDescription, setBugDescription] = useState('');
  const [stackTrace, setStackTrace] = useState('');
  const [errorLogs, setErrorLogs] = useState('');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {

    setError('');

    if (!bugTitle.trim()) {
      setError('Bug title is required');
      return;
    }

    if (!programmingLanguage) {
      setError('Please select a programming language');
      return;
    }

    if (!bugDescription.trim()) {
      setError('Bug description is required');
      return;
    }

    setLoading(true);

    try {

      const response = await fetch(
        'http://127.0.0.1:5000/api/diagnose',
        {
          method: 'POST',

          headers: {
            'Content-Type': 'application/json'
          },

          body: JSON.stringify({
            bug_title: bugTitle,
            programming_language: programmingLanguage,
            bug_description: bugDescription,
            stack_trace: stackTrace,
            error_log: errorLogs
          })
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.error || 'Diagnosis failed'
        );
      }

      onAnalyze(data);

    } catch (err) {

      console.error(err);

      setError(
        'Unable to connect to AI backend. Please make sure Flask server is running.'
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <div className="bug-page">

      {/* Header */}
      <div className="bug-header">

        <div className="header-content">

          <button
            className="back-btn"
            onClick={onBack}
          >
            ← Back to Home
          </button>

          <div className="header-title">

            <p className="page-label">
              BUG ANALYSIS
            </p>

            <h1>
              Submit a Bug
            </h1>

            <p>
              Provide the details of the issue to receive an intelligent
              diagnosis and fix recommendation.
            </p>

          </div>

        </div>

      </div>

      {/* Form */}
      <div className="bug-form-container">

        <div className="form-intro">

          <h2>
            Bug Information
          </h2>

          <p>
            Enter the basic information about the software issue.
          </p>

        </div>

        <div className="bug-form">

          {/* Bug Title */}
          <div className="form-group">

            <label>
              Bug Title
              <span>*</span>
            </label>

            <input
              type="text"
              value={bugTitle}
              onChange={(e) =>
                setBugTitle(e.target.value)
              }
              placeholder="e.g. NullPointerException in Login Module"
            />

          </div>

          {/* Programming Language */}
          <div className="form-group">

            <label>
              Programming Language
              <span>*</span>
            </label>

            <select
              value={programmingLanguage}
              onChange={(e) =>
                setProgrammingLanguage(e.target.value)
              }
            >

              <option value="" disabled>
                Select programming language
              </option>

              <option>Java</option>
              <option>Python</option>
              <option>JavaScript</option>
              <option>C++</option>
              <option>C</option>

            </select>

          </div>

          {/* Description */}
          <div className="form-group full-width">

            <label>
              Bug Description
              <span>*</span>
            </label>

            <textarea
              rows="5"
              value={bugDescription}
              onChange={(e) =>
                setBugDescription(e.target.value)
              }
              placeholder="Describe what happened, when the error occurs, and what you expected to happen..."
            />

          </div>

          {/* Technical Details */}
          <div className="form-section-title">

            <div>

              <h2>
                Technical Details
              </h2>

              <p>
                Add the technical information related to the error.
              </p>

            </div>

          </div>

          {/* Stack Trace */}
          <div className="form-group full-width">

            <label>
              Stack Trace
            </label>

            <textarea
              className="code-input"
              rows="7"
              value={stackTrace}
              onChange={(e) =>
                setStackTrace(e.target.value)
              }
              placeholder="Paste the complete stack trace here..."
            />

            <small>
              Include the complete error stack trace if available.
            </small>

          </div>

          {/* Error Logs */}
          <div className="form-group full-width">

            <label>
              Error Logs
            </label>

            <textarea
              className="code-input"
              rows="7"
              value={errorLogs}
              onChange={(e) =>
                setErrorLogs(e.target.value)
              }
              placeholder="Paste relevant application or system logs here..."
            />

            <small>
              Logs can help identify the root cause of the issue.
            </small>

          </div>

          {/* Project Files */}
          <div className="form-section-title">

            <div>

              <h2>
                Project Files
              </h2>

              <p>
                Upload relevant files to improve diagnosis accuracy.
              </p>

            </div>

          </div>

          <div className="form-group full-width">

            <label>
              Upload Project File
            </label>

            <div className="upload-box">

              <div className="upload-icon">
                ↑
              </div>

              <h3>
                Upload your project or error file
              </h3>

              <p>
                Drag and drop your file here or choose a file
              </p>

              <span>
                Supported: .zip, .java, .py, .js, .txt, .log
              </span>

              <input type="file" />

            </div>

          </div>

          {/* Error Message */}
          {error && (
            <div
              style={{
                color: '#dc2626',
                background: '#fee2e2',
                padding: '12px',
                borderRadius: '8px',
                marginTop: '10px'
              }}
            >
              {error}
            </div>
          )}

          {/* Actions */}
          <div className="form-actions">

            <button
              className="cancel-btn"
              onClick={onBack}
              disabled={loading}
            >
              Cancel
            </button>

            <button
              className="submit-btn"
              onClick={handleAnalyze}
              disabled={loading}
            >

              {loading
                ? 'Analyzing...'
                : 'Analyze Bug'
              }

              {!loading && (
                <span>
                  →
                </span>
              )}

            </button>

          </div>

        </div>

      </div>

    </div>
  );
}

export default BugSubmission;