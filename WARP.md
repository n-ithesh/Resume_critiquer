# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project overview

This repository is a small Streamlit web app that uploads a resume (PDF or plain text), extracts its content, and sends it to the OpenAI Chat Completions API for structured feedback tailored to a target job role.

Core technologies:
- Python (configured for Python 3.13 in `pyproject.toml`)
- Streamlit for the UI
- OpenAI Python SDK for calling chat completions
- PyPDF2 for PDF text extraction
- python-dotenv for loading environment variables from a `.env` file

## Environment & dependencies

- Python version: `>=3.13` (see `pyproject.toml`).
- Dependencies are declared in `pyproject.toml` under `[project].dependencies`.
- The app expects an `OPENAI_API_KEY` environment variable, typically provided via a local `.env` file loaded by `python-dotenv`.

Suggested local setup (from the project root):

1. Create and activate a virtual environment using your preferred tool (e.g., `python -m venv .venv` and activate it).
2. Install dependencies from `pyproject.toml`:
   - `python -m pip install .`
3. Create a `.env` file alongside `main.py` with at least:
   - `OPENAI_API_KEY=your_api_key_here`

## Common commands

All commands below assume you are in the repository root (`Resume_critique`).

### Run the app

- Start the Streamlit app:
  - `streamlit run main.py`

This will launch the "Resume Critiquer" UI in the browser.

### Linting & tests

- There is currently no configured linting or test suite in this repository.
- If you add tests (e.g., using `pytest` under a `tests/` directory), prefer to document the canonical test command here (for example, `pytest` and specific test-node selection like `pytest tests/test_file.py::test_name`).

## High-level architecture

The codebase is intentionally minimal and organized around a single entrypoint file:

### `main.py`

This file defines and wires together all app behavior:

1. **Configuration & imports**
   - Imports Streamlit (`streamlit as st`), `os`, `PyPDF2`, `io`, `OpenAI` from `openai`, and `load_dotenv` from `dotenv`.
   - Calls `load_dotenv()` early so `.env` variables (such as `OPENAI_API_KEY`) are available via `os.getenv`.
   - Calls `st.set_page_config` to set the page title, icon, and layout.

2. **UI layout & user inputs**
   - Defines page title and description with `st.title` and `st.markdown`.
   - File upload widget:
     - `upload_file = st.file_uploader("Choose a PDF/TEXT file", type=["pdf", "txt"])`.
   - Job role input:
     - `job_role = st.text_input("Enter the job role you are applying for:")`.
   - Primary action button:
     - `analyze_button = st.button("Analyze Resume")`.

3. **Text extraction helpers**
   - `extract_text_from_pdf(file)`
     - Uses `PyPDF2.PdfReader` to iterate over `pages` and concatenate `page.extract_text()` results into a single string.
   - `extract_text_from_txt(uploaded_file)`
     - For non-PDF uploads, reads raw bytes and decodes as UTF-8.
     - For PDFs, wraps the uploaded file in a `BytesIO` and delegates to `extract_text_from_pdf`.

4. **Main interaction flow (analyze button handler)**
   - Triggered when `analyze_button` is pressed and a file is uploaded (`upload_file` is not `None`).
   - Pipeline (conceptually, both try/except blocks implement the same flow):
     1. Extract text from the uploaded file using `extract_text_from_txt`.
     2. Validate that the extracted content is non-empty; if empty, display an error and call `st.stop()`.
     3. Build a natural-language prompt for the OpenAI model, including:
        - The resume content.
        - Emphasis on specific critique criteria (content clarity, skills presentation, experience descriptions).
        - Tailoring to a specific job role if `job_role` is provided, or a generic instruction otherwise.
     4. Instantiate an `OpenAI` client using the `OPENAI_API_KEY` from the environment.
     5. Call `client.chat.completions.create` with:
        - `model="gpt-3.5-turbo"`.
        - A small message sequence: system role defining behavior and user role with the constructed prompt.
        - Parameters like `max_tokens` and `temperature` to control response length and creativity.
     6. Display the returned analysis as markdown under the heading "Resume Analysis and Feedback:".
     7. Wrap the entire operation in `try/except` blocks and surface any exceptions to the user via `st.error`.

   - **Note:** The file currently contains two consecutive `try/except` blocks that both:
     - Extract text,
     - Build a similar prompt,
     - Call `client.chat.completions.create`,
     - Render results.

     Future refactors should consider consolidating this duplicated logic into a single, well-structured function or flow to reduce maintenance overhead.

## How to extend the app

When adding new features, keep in mind:

- **Separation of concerns**: Given the current single-file structure, any non-trivial additions (e.g., different critique modes, history, exporting, or additional APIs) will benefit from extracting business logic into separate modules (for example, `services/openai_client.py`, `services/resume_parser.py`, or `ui/components.py`).
- **Model configuration**: If you introduce support for additional models or providers, centralize model selection and configuration rather than scattering model names through the UI logic.
- **Error handling & UX**: The current error handling is coarse-grained (`st.error` in broad `except` blocks). For more complex flows, prefer distinguishing between user-input errors (e.g., unsupported file types, bad encoding) and backend issues (e.g., API failures, rate limits).