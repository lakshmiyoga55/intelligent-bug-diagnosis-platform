# Intelligent Bug Diagnosis Platform

An AI-assisted platform for intelligent bug diagnosis and fix recommendation assistance. The platform is designed to help developers analyze software bugs, identify possible root causes, detect similar historical defects, and explore potential remediation steps.

## Project Overview

The Intelligent Bug Diagnosis Platform aims to simplify the software debugging process by combining bug analysis, historical defect knowledge, duplicate detection, and remediation assistance in one interface.

This project is developed as part of the **Infosys Springboard Virtual Internship 7.0, Batch 3 (2026–2027)**.

## Key Features

- **Bug Triage:** Classifies reported bugs by severity and priority.
- **Root Cause Analysis:** Helps identify possible causes of software defects.
- **Duplicate Bug Detection:** Finds potentially similar bugs from available historical records.
- **Fix Recommendation Assistance:** Suggests possible remediation steps for identified issues.
- **Log Analysis:** Supports examination of log information during debugging.
- **Analytics Dashboard:** Helps review and filter submitted bug records.
- **Knowledge Base:** Uses historical defect information to support diagnosis.

## Technology Stack

- **Frontend:** React.js
- **Backend:** Python, Flask
- **Data and Knowledge Base:** JSON-based defect records and supporting retrieval components
- **AI Assistance:** AI/LLM integration, depending on API configuration

## Project Architecture

The application follows a frontend–backend architecture. The React frontend communicates with the Flask backend, which processes bug submissions and coordinates the available diagnosis, duplicate detection, knowledge retrieval, and remediation components.

Refer to [`Architecture.pdf`](Architecture.pdf) for the project architecture and [`TECH STACK.pdf`](TECH%20STACK.pdf) for the technology stack details.

## Getting Started

### Prerequisites

- Python 3.13 or another compatible Python version
- Node.js and npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/lakshmiyoga55/intelligent-bug-diagnosis-platform.git
cd intelligent-bug-diagnosis-platform
```

### 2. Set up the backend

Open a terminal in the project root.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies using the dependency file provided in the `backend` directory. For example, if `backend/requirements.txt` exists:

```powershell
pip install -r backend/requirements.txt
```

Configure any required environment variables using a local `.env` file or your environment settings. Never commit API keys or secrets to GitHub.

Start the backend using the project's configured Flask entry point. If `backend/app.py` is the entry point:

```powershell
cd backend
python app.py
```

### 3. Set up the frontend

Open a separate terminal in the project root.

```powershell
cd frontend
npm install
npm start
```

The React development server commonly runs at `http://localhost:3000`. The backend commonly runs at `http://127.0.0.1:5000`, subject to the project configuration.

**Note:** Verify dependency filenames, environment variables, API settings, and startup commands against the current source code before using these instructions.

## Testing

Run the tests and checks available in the project before using the platform. Verify bug submission, severity and priority classification, duplicate detection, diagnosis results, remediation suggestions, and analytics.

## Security

- Keep API keys and credentials in environment variables or a local `.env` file.
- Do not commit `.env`, virtual environments, or dependency folders.
- Use `.env.example` for documenting required environment variable names without including secret values.

## Future Enhancements

- Improve diagnosis accuracy and recommendation quality.
- Expand the historical defect knowledge base.
- Add more automated tests and evaluation metrics.
- Improve deployment, monitoring, and user experience.

## Project Documents

- [Architecture](Architecture.pdf)
- [Technology Stack](TECH%20STACK.pdf)

## Contributors

Developed as part of the Infosys Springboard Virtual Internship project.

## License

The license for this project should be specified in the repository's `LICENSE` file.
