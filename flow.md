# Application Flow: Frontend to Backend

This document describes the flow of data and actions from the user's interaction in the browser (frontend) to the backend processing in the RadExtract application.

---

## 1. User Interaction (Frontend)
- The user selects a sample report or enters/pastes a custom radiology report in the input textarea on the web page (`index.html`).
- The user clicks the **Process** button to start structuring the report.

## 2. JavaScript Event Handling
- The frontend JavaScript (`static/script.js`) listens for the click event on the **Process** button.
- When clicked, it collects the input text from the textarea and any selected options (e.g., model, cache toggle).
- The script sends an HTTP POST request (usually via `fetch` or `XMLHttpRequest`) to the backend API endpoint (commonly `/structure_report` or similar).

## 3. Backend API Endpoint (Flask/Python)
- The backend is a Python Flask app (see `app.py`).
- The endpoint (e.g., `/structure_report`) receives the POST request with the report text and options as JSON payload.
- The backend validates and sanitizes the input (see `sanitize.py`).

## 4. Report Processing
- The backend calls the main processing logic (see `structure_report.py`).
- Depending on options, it may use a cache (`cache_manager.py`) or run a model (e.g., Gemini, LangExtract) to extract structured data from the report.
- The backend generates structured output (findings, impressions, etc.) as JSON.

## 5. Response to Frontend
- The backend returns the structured data as a JSON response.
- The frontend JavaScript receives the response and updates the Output area in the UI, displaying the structured findings and any additional data.

---

## Summary Diagram

```
User Input (textarea/button)
        ↓
Frontend JS (script.js)
        ↓ (POST)
Backend Flask API (app.py)
        ↓
Sanitization/Processing (sanitize.py, structure_report.py)
        ↓
Model/Cache (Gemini, cache_manager.py)
        ↓
Structured Output (JSON)
        ↓
Frontend JS updates Output UI
```

---

## Key Files
- `templates/index.html` — Main HTML UI
- `static/script.js` — Frontend logic and API calls
- `app.py` — Flask backend, API endpoints
- `structure_report.py` — Main report structuring logic
- `cache_manager.py` — Handles caching of results
- `sanitize.py` — Input cleaning

---

## UI to Backend Function Call Details

### 1. UI Event Handling (Frontend)
- The **Process** button in the UI is linked to a JavaScript event listener (see `static/script.js`).
- When clicked, the event handler function (e.g., `onProcessClick` or similar) is triggered.
- This function:
  - Reads the value from the input textarea (`#input-text`).
  - Collects any selected options (model, cache, toggles).
  - Disables the button and shows a loading spinner/overlay.

### 2. API Call from Frontend
- The event handler uses `fetch` (or `XMLHttpRequest`) to send a POST request to the backend endpoint (e.g., `/structure_report`).
- The request body is JSON, e.g.:
  ```json
  {
    "report_text": "...user input...",
    "model": "gemini-2.5-flash",
    "use_cache": true
  }
  ```
- The request includes appropriate headers (`Content-Type: application/json`).

### 3. Backend Endpoint Handling
- Flask receives the POST at `/structure_report` (see `app.py`).
- The endpoint function (e.g., `structure_report_endpoint`) does:
  - Parses the JSON payload.
  - Calls `sanitize.py` to clean the input.
  - Calls `structure_report.py` to process the report (may use `cache_manager.py` if cache is enabled).
  - The main function in `structure_report.py` (e.g., `structure_report()`) runs the extraction logic, possibly calling an external model or library.
  - The result is a Python dict with structured findings, impressions, etc.

### 4. Backend Response
- The Flask endpoint returns a JSON response with the structured data.
- Example response:
  ```json
  {
    "findings": [...],
    "impressions": [...],
    "raw_json": {...},
    ...
  }
  ```

### 5. UI Updates Output
- The frontend JS receives the response in the `.then()` or `await` block.
- It parses the JSON and updates the Output area:
  - Populates the findings, impressions, and other fields in the UI.
  - Handles errors or empty results gracefully.
  - Re-enables the Process button and hides the loading spinner.

---

## Example Function Call Flow

1. User clicks **Process**
2. JS: `fetch('/structure_report', { method: 'POST', body: ... })`
3. Flask: `@app.route('/structure_report', methods=['POST'])`
4. Python: `structure_report()` (calls model/cache)
5. Flask: `return jsonify(result)`
6. JS: `response.json()` → update UI

---

This flow ensures that every UI action is mapped to a backend function call, with clear data transfer and error handling at each step.
