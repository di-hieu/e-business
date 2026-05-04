# System Architecture Documentation

## 1. Overview

This system is designed as a client-server chatbot application with a clear separation of concerns:
*   **Frontend:** Handled by a modern JavaScript framework (React) and focuses on the user interface, message handling, and API interaction.
*   **Backend:** Handled by Python 2, providing the core business logic, NLP processing, and state management for the chat session.
*   **Documentation:** This folder (`docs`) houses all architectural blueprints, design decisions, and operational procedures.

## 2. Directory Structure

```
.
├── backend/         # Python 2 core logic
├── frontend/        # React client-side components (SPA)
├── docs/            # Documentation artifacts
└── ... (other configs)
```

## 3. Technology Stack

*   **Frontend:** React, CSS Modules/CSS-in-JS.
*   **Backend:** Python 2.x (Crucial: All code must adhere to Python 2 syntax).
*   **Communication:** REST API (JSON format) endpoint expected at `/api/chat`.

## 4. Feature Flow

1.  User types message on the Frontend.
2.  The Frontend calls the Backend API (`POST /api/chat`).
3.  The Backend (Python 2) processes the message:
    a. Retrieves chat history/context.
    b. Applies business rules/logic.
    c. Generates a response text.
4.  The Backend sends the JSON response back to the Frontend.
5.  The Frontend updates the chat history and displays the response.

## 5. Development Rules for Cline

1.  **Documentation First:** Any major feature addition, architectural change, or refactoring *must* first result in an update to the relevant document in the `docs/` folder before code implementation begins.
2.  **Feature Tree Structure:** All new features must be scoped to either the `backend/` or `frontend/` directory and clearly documented.
3.  **Python 2 Adherence:** All changes to `backend/` must be validated for Python 2 compatibility (e.g., `print` statement usage, string handling).