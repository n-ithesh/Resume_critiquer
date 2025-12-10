# Resume Critiquer

A simple Streamlit web application that analyzes your resume (PDF or text) and provides structured, actionable feedback using the OpenAI Chat Completions API.

The app is designed to help you quickly identify strengths, weaknesses, and opportunities for improvement in your resume, with optional tailoring to a specific job role.

## Features

- Upload resume as **PDF** or **plain text (.txt)**.
- Automatically extracts text from uploaded PDF files using **PyPDF2**.
- Sends resume content to the **OpenAI** API for critique.
- Accepts an optional **target job role** to customize the feedback.
- Displays structured feedback directly in the browser via **Streamlit**.

## Tech stack

- **Language:** Python (requires Python 3.13 or later)
- **Web framework:** Streamlit
- **AI provider:** OpenAI (Chat Completions API)
- **PDF processing:** PyPDF2
- **Environment management:** python-dotenv

Dependencies are declared in `pyproject.toml` under `[project].dependencies`.

## Prerequisites

- Python `>= 3.13` installed and available on your PATH.
- An **OpenAI API key** with access to the `gpt-3.5-turbo` model (or compatible chat model).

## Installation & setup

All commands below assume you are in the project root directory: `Resume_critique`.

### 1. Clone or download the repository

If you haven't already, clone this project (or download it as a ZIP and extract it):

```bash path=null start=null
git clone <your-repo-url>
cd Resume_critique
```

### 2. Create and activate a virtual environment

You can use any virtual environment tool you prefer. Example with the built-in `venv` module:

```bash path=null start=null
python -m venv .venv
# On Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# On macOS/Linux (bash/zsh)
source .venv/bin/activate
```

### 3. Install dependencies

Install the required Python packages listed in `pyproject.toml`:

```bash path=null start=null
python -m pip install --upgrade pip
python -m pip install streamlit openai pypdf2 python-dotenv
```

(If you later add more dependencies to `pyproject.toml`, be sure to install them similarly.)

### 4. Configure environment variables

The app expects an `OPENAI_API_KEY` environment variable. The simplest way to provide it is by creating a `.env` file in the project root (alongside `main.py`) and letting `python-dotenv` load it.

Create a file named `.env` with the following content:

```bash path=null start=null
OPENAI_API_KEY=your_openai_api_key_here
```

> Do not commit your real API key to version control.

## Running the application

With the virtual environment activated and dependencies installed, run:

```bash path=null start=null
streamlit run main.py
```

This will start a local development server and open the app in your default browser (or provide a URL you can open manually).

## Using the app

1. **Upload your resume**
   - Click on the file uploader and select a **PDF** or **TXT** file.
2. **Specify job role (optional)**
   - Enter the job role you are applying for (e.g., "Data Analyst", "Software Engineer").
   - If left blank, the model will provide general resume feedback.
3. **Analyze**
   - Click the **"Analyze Resume"** button.
   - The app will:
     - Extract text from the file (using `PyPDF2` for PDFs or direct decoding for text files).
     - Validate that the extracted content is non-empty.
     - Build a prompt that instructs the model to critique:
       - Content clarity and impact
       - Skills presentation
       - Experience descriptions
       - Improvements tailored to the given job role (if provided)
     - Call the OpenAI Chat Completions API (`gpt-3.5-turbo`).
4. **View feedback**
   - The response from the model is rendered in a structured markdown format under **"Resume Analysis and Feedback:"**.

If any error occurs (e.g., invalid file, API error), a message will be shown in the interface.

## Project structure

Key files:

- `main.py`  
  Streamlit app entrypoint. Handles UI, file upload, text extraction, prompt construction, and OpenAI API calls.

- `pyproject.toml`  
  Project metadata (name, version, description) and core dependencies, including `streamlit`, `openai`, `pypdf2`, and `python-dotenv`.

- `WARP.md`  
  Guidance file for Warp (warp.dev) agents working in this repository.

## Implementation details

### `main.py`

High-level flow:

1. **Imports & configuration**
   - Imports `streamlit as st`, `os`, `PyPDF2`, `io`, `OpenAI` from `openai`, and `load_dotenv` from `dotenv`.
   - Calls `load_dotenv()` to load environment variables from `.env`.
   - Sets Streamlit page configuration (title, icon, layout).

2. **UI definition**
   - Page title and description via `st.title` and `st.markdown`.
   - `st.file_uploader` for PDF/TXT uploads.
   - `st.text_input` for the user to specify a target job role.
   - `st.button("Analyze Resume")` as the trigger for analysis.

3. **Text extraction helpers**
   - `extract_text_from_pdf(file)` loops over all pages using `PyPDF2.PdfReader` and concatenates extracted text.
   - `extract_text_from_txt(uploaded_file)`:
     - For PDFs, wraps the uploaded file in `io.BytesIO` and calls `extract_text_from_pdf`.
     - For text files, reads bytes and decodes as UTF-8.

4. **Calling the OpenAI API**
   - On button press (and if a file is present), the app:
     - Extracts resume text.
     - Ensures the text is non-empty, otherwise shows an error and stops.
     - Constructs a prompt describing how the model should critique the resume, including the job role if provided.
     - Creates an `OpenAI` client using `OPENAI_API_KEY` from the environment.
     - Calls `client.chat.completions.create` with:
       - `model="gpt-3.5-turbo"`
       - A system message defining the model's role as a helpful resume critique assistant.
       - A user message containing the constructed prompt and the resume text.
     - Renders the returned `response.choices[0].message.content` as markdown.
   - Errors during processing are caught and shown via `st.error`.

> Note: At present, `main.py` contains two similar `try/except` blocks that both perform resume extraction, prompt construction, and OpenAI calls. This works but is redundant; future refactoring could consolidate this into a single well-structured function.

## Extending the project

Ideas for future enhancements:

- Add a more detailed UI layout (sidebars, sections for strengths/weaknesses, scoring, etc.).
- Support additional file formats (e.g., `.docx`) by adding a document conversion layer.
- Allow exporting feedback as a downloadable text or PDF report.
- Add parameters in the UI for choosing different models or adjusting `temperature` / `max_tokens`.
- Introduce automated tests (e.g., with `pytest`) for:
  - Text extraction functions.
  - Prompt construction given various job roles and inputs.

Once you add tests or tooling (linting, type checking), consider updating this README with the recommended commands (e.g., `pytest`, `ruff`, `mypy`, etc.).