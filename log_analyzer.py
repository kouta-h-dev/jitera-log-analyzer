import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file.
load_dotenv()

# ==========================================
# Portfolio for Jitera Internship Application
# Project: Log Analysis AI Agent (POC)
# Author: Kouta Higuchi
# Method: Self-Healing REST API (Auto-detect Model)
# ==========================================

# Retrieve the API key from environment variables.
# Using os.getenv() ensures that we do not hardcode any sensitive credentials.
API_KEY = os.getenv("GOOGLE_API_KEY")

def get_available_model(api_key):
    """
    Dynamically queries the API to find available Gemini models.
    Automatically selects the first available model that supports 'generateContent'.
    This prevents crashes caused by API version updates or model deprecation.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch model list: {response.text}")

    data = response.json()

    # Find a model that supports content generation
    for model in data.get('models', []):
        if 'generateContent' in model.get('supportedGenerationMethods', []):
            return model['name']

    raise Exception("No available Gemini models found. Please check your API key.")

def analyze_log_auto(log_content):
    # 1. Auto-detect the best available model for the current environment
    try:
        model_name = get_available_model(API_KEY)
        # In a real app, use a proper logger instead of print
        print(f"DEBUG: Using model -> {model_name}")
    except Exception as e:
        return json.dumps({"error": f"Model detection failed: {str(e)}"}, ensure_ascii=False)

    # 2. Build request with the detected model
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={API_KEY}"

    headers = {"Content-Type": "application/json"}

    # Constructing the prompt for the AI Agent
    prompt_text = f"""
    You are an expert SRE (Site Reliability Engineer) at Jitera.
    Analyze the following server log and provide actionable insights strictly in JSON format.

    ### Log Data:
    {log_content}

    ### Output Schema (JSON):
    {{
        "error_summary": "Brief summary of the error",
        "root_cause": "Technical root cause (e.g., Memory Leak, Database Timeout)",
        "criticality": "High/Medium/Low",
        "action_items": ["Specific Action 1", "Specific Action 2"]
    }}
    """

    data = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return json.dumps({"error": f"API Error: {response.text}"}, ensure_ascii=False)

    return response.json()

# ==========================================
# Main Execution Block
# ==========================================
if __name__ == "__main__":
    # Dummy log data for demonstration
    dummy_log = """
    [2025-12-10 14:00:06] ERROR: Transaction failed. Exception: PyO3 modules are not initialized.
    [2025-12-10 14:00:06] CRITICAL: Rust backend panic. Memory allocation error.
    """

    print("--- Starting Log Analysis Agent ---")

    # Correctly check if the API_KEY is loaded from environment variables.
    if not API_KEY:
        print("WARNING: API Key is not set. Please set GOOGLE_API_KEY in your .env file.")
    else:
        result = analyze_log_auto(dummy_log)

        # Display formatted result
        if isinstance(result, dict) and 'candidates' in result:
            raw_text = result['candidates'][0]['content']['parts'][0]['text']
            # Clean up potential Markdown formatting from AI response
            cleaned_text = raw_text.replace('```json', '').replace('```', '').strip()
            print(cleaned_text)
        else:
            print(result)