# Jitera Log Analysis Agent (POC)

A prototype AI agent designed to streamline development workflows at Jitera.
It utilizes the Google Gemini API to automatically parse server logs, identify root causes, and structure actionable insights into JSON.

## Key Features

- **Self-Healing Model Detection** Implements a robust REST API client that automatically detects available Gemini models (e.g., `gemini-2.5-flash`, `gemini-pro`) at runtime. This prevents crashes caused by SDK version mismatches or API deprecations, ensuring high availability.

- **Structured JSON Output** Outputs pure JSON data optimized for integration with issue tracking systems (Jira) or communication tools (Slack), rather than unstructured text.

- **Automated Root Cause Analysis** Capable of analyzing complex stack traces (e.g., Rust/Python hybrid errors) to pinpoint technical bottlenecks.

## Usage

1. **Get API Key** Obtain an API key from Google AI Studio.

2. **Configuration** Set your `GOOGLE_API_KEY` in your environment variables or update the placeholder in `main.py` for local testing.

3. **Run** ```bash
   python main.py
