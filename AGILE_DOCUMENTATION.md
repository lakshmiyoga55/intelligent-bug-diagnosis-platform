# Agile Project Documentation

## Project Information

| Item | Details |
|---|---|
| Project title | Creation of Intelligent Bug Diagnosis Platform with Fix Recommendation Assistance |
| Application name | Intelligent Bug Diagnosis Platform |
| Internship | Infosys Springboard Virtual Internship 7.0, Batch 3 (2026–2027) |
| Repository | https://github.com/lakshmiyoga55/intelligent-bug-diagnosis-platform |
| Development approach | Iterative Agile approach using milestone-based increments |
| Document purpose | Describe project planning, implementation increments, testing approach, and project review |

## 1. Project Overview

The Intelligent Bug Diagnosis Platform helps users submit software bug details and receive structured diagnostic assistance. The workflow includes bug triage, log analysis, retrieval of similar historical defects, root-cause analysis, duplicate detection, remediation suggestions, and analytics.

The platform uses a React-based frontend and a Python Flask backend. Its diagnosis workflow uses a historical defect knowledge base and embedding-based semantic retrieval, with LLM integration where configured and available.

## 2. Project Objectives

- Provide a simple interface for submitting bug descriptions and related technical details.
- Classify bugs by severity and priority.
- Analyze error logs and exception information.
- Retrieve relevant historical defects to support root-cause analysis.
- Identify potentially duplicate defects.
- Present recommended remediation steps and structured diagnosis results.
- Provide analytics to help review submitted bugs and defect trends.
- Maintain project documentation and a repository suitable for review and demonstration.

## 3. Agile Approach

The project was developed in small increments aligned with internship milestones. Each increment focused on a set of features, followed by integration, review, and refinement.

The workflow:
1. Review milestone requirements.
2. Break requirements into smaller tasks.
3. Implement frontend, backend, or knowledge-base changes.
4. Integrate changes with the existing application.
5. Test affected functionality and record issues.
6. Update technical documentation and prepare a demonstration.
7. Review feedback and plan the next increment.

> This document describes the milestone-based approach. Update team-specific details, meeting records, and actual completion statuses if your mentor or team has additional records.

## 4. Product Backlog

| ID | Feature / user need | Priority | Acceptance criteria |
|---|---|---|---|
| PB-01 | Bug submission | High | User can enter bug details and submit them to the backend. |
| PB-02 | Bug triage | High | Diagnosis includes severity and priority classifications where required inputs are available. |
| PB-03 | Log analysis | High | Submitted logs can be examined and relevant findings returned. |
| PB-04 | Historical defect knowledge base | High | Historical defect records can be loaded and used by the retrieval workflow. |
| PB-05 | Root-cause assistance | High | Results include root-cause findings supported by available defect/context information. |
| PB-06 | Duplicate detection | High | Results list potentially similar historical bugs when matches are found. |
| PB-07 | Remediation recommendations | High | Results present suggested fixes or resolution guidance when available. |
| PB-08 | Structured diagnosis result | High | Diagnosis information is displayed in a readable result view. |
| PB-09 | Analytics | Medium | Users can review aggregated bug information and apply supported filters. |
| PB-10 | Documentation and delivery | High | Repository includes setup guidance, technical documentation, license information, and demo materials as required. |

## 5. Milestone / Sprint Plan

The internship work was organized around the milestones below. Dates are included only where known; confirm any additional dates with team records before submission.

### Milestone 1 — Knowledge Base and Initial Foundation
**Target date recorded:** 28 August 2026

**Focus**
- Establish the project foundation and knowledge-base structure.
- Prepare historical defect data for retrieval.
- Validate the initial knowledge-base workflow.
- Set up the basic application structure and documentation.

**Expected output**
- Initial project structure.
- Historical defect knowledge-base files.
- Initial validation and setup documentation.

### Milestone 2 — Bug Triage and Log Analysis

**Focus**
- Add severity classification: Critical, High, Medium, and Low.
- Add priority classification: P0, P1, P2, and P3.
- Integrate log analysis into the diagnosis workflow.
- Present triage and log findings in the application.

**Expected output**
- Triage results with severity and priority.
- Log-analysis findings.
- Updated integration and demonstration flow.

### Milestone 3 — Diagnosis Agents and Findings
**Target date recorded:** 24 September 2026

**Focus**
- Add root-cause analysis using historical knowledge-base/retrieval context.
- Add duplicate bug detection.
- Add remediation assistance.
- Display findings in a structured diagnosis result.

**Expected output**
- Root-cause findings.
- Potential duplicate records and similarity information.
- Remediation recommendations.
- Structured diagnosis output.

### Milestone 4 — Analytics, Knowledge-Base Growth, and End-to-End Review
**Target date recorded:** 7 October 2026

**Focus**
- Add or refine analytics and supported filters.
- Support knowledge-base growth and review of defect records.
- Run end-to-end checks across the frontend and backend.
- Update technical documentation and prepare the project demonstration.

**Expected output**
- Analytics functionality and filter support, as implemented.
- Updated knowledge-base workflow.
- End-to-end test records.
- Technical documentation and demo preparation.

## 6. Roles and Responsibilities

Use the actual names and responsibilities agreed by your team before final submission.

| Role | Responsibility |
|---|---|
| Project team / developers | Implement features, integrate components, test changes, maintain source control, and prepare documentation. |
| Project coordinator (if assigned) | Track milestone progress, coordinate tasks, and consolidate the presentation. |
| Mentor | Provide guidance, review progress, and clarify project expectations. |
| Presenter / demo owner (if assigned) | Explain the workflow and demonstrate the application. |

Do not list a person as responsible for a task unless that responsibility matches the team's actual work.

## 7. Development Workflow and Tools

- **Source control:** Git and GitHub.
- **Frontend:** React.js.
- **Backend:** Python and Flask.
- **Knowledge base:** JSON-based historical defect records and vector-store data.
- **Semantic retrieval:** Sentence Transformers embeddings with vector similarity comparison.
- **Testing:** Python test scripts and manual frontend-to-backend checks.
- **Documentation:** Markdown project documents and presentation material.

The LLM-assisted workflow may depend on a configured API key and available provider quota. If the external LLM service is unavailable, the demonstration should clearly distinguish that limitation from the platform's other functionality.

## 8. Testing Strategy

Testing should be carried out at multiple levels. Record the actual outcome, date, and evidence for each test before marking it as passed.

| Test ID | Test scenario | Expected result | Actual result / status |
|---|---|---|---|
| TC-01 | Open the frontend | Main interface loads without a blocking error. | To be recorded |
| TC-02 | Start the Flask backend | Backend starts and exposes its configured API endpoints. | To be recorded |
| TC-03 | Submit a valid bug report | Backend accepts the input and returns a diagnosis response. | To be recorded |
| TC-04 | Submit a report with missing fields | Input is handled safely with a clear response or validation message. | To be recorded |
| TC-05 | Classify bug severity and priority | Appropriate classification is included when sufficient information is available. | To be recorded |
| TC-06 | Analyze error logs | Relevant log findings are returned for supported inputs. | To be recorded |
| TC-07 | Retrieve similar historical defects | Similarity-ranked historical records are returned when matches exist. | To be recorded |
| TC-08 | Detect possible duplicates | Candidate duplicate bugs are listed when matches are found. | To be recorded |
| TC-09 | Generate remediation guidance | Available fix recommendations are displayed with the diagnosis. | To be recorded |
| TC-10 | Review analytics and filters | Analytics data and supported filters behave as expected. | To be recorded |
| TC-11 | End-to-end workflow | A submitted bug can move through the implemented diagnosis workflow and display its result. | To be recorded |

**Testing note:** Do not change “To be recorded” to “Passed” unless the test has actually been executed and its result verified.

## 9. Risks and Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| External LLM API quota or availability | LLM-generated findings may fail even when the application is running. | Check API configuration and quota; prepare sample inputs and clearly disclose any unavailable external service during the demo. |
| Python package or platform-policy issues | Backend startup or embedding-model loading may be blocked on a particular machine. | Verify the environment, record the error, and request an approved fix from the device administrator where a security policy is involved. Do not bypass security controls. |
| Incomplete or inconsistent historical data | Retrieval results may be weak or irrelevant. | Validate records and improve data quality as part of knowledge-base maintenance. |
| Frontend/backend integration errors | The user may not receive a diagnosis result. | Test API connectivity and the complete workflow before the presentation. |
| Time constraints near submission | Documentation or demo preparation may be incomplete. | Prioritize required deliverables and track remaining tasks against the mentor's instructions. |

## 10. Review and Retrospective

At the end of each milestone, the team should review:
- Which planned features were completed.
- Which tests were executed and their outcomes.
- Issues or blockers encountered.
- Feedback received from the mentor or team.
- Changes needed for the next milestone.
- Documentation and demo readiness.

### Retrospective record

Complete this section using the team's actual review notes.
- **What went well:** To be completed by the team.
- **Challenges faced:** To be completed by the team.
- **Improvements for the next iteration:** To be completed by the team.
- **Mentor/team feedback:** To be completed by the team.

## 11. Final Deliverables Checklist

- [ ] GitHub repository link shared with the mentor.
- [ ] Agile documentation added to the repository.
- [ ] MIT License added, after confirming the project/team has permission to license the submitted work under MIT.
- [ ] Deployment completed and deployment URL tested.
- [ ] End-to-end tests executed and actual results recorded.
- [ ] Team presentation prepared.
- [ ] Live or recorded project demonstration prepared.
- [ ] Repository setup instructions and known limitations reviewed.

## 12. Repository

Project repository: https://github.com/lakshmiyoga55/intelligent-bug-diagnosis-platform

---

**Document maintenance:** Update this file whenever milestone outcomes, test results, team roles, or delivery status are confirmed. This document should reflect the work actually completed.
