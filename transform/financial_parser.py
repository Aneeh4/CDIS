"""
financial_parser.py
-------------------
Extracts financial metrics (Revenue, EPS, Margins) from parsed text.
Handles regex/fuzzy matching and normalization of units (e.g., $M, %).
"""
import re, json, ast
import requests
from rapidfuzz import fuzz

def extract_metrics_with_gemini(prompt, context_text, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt + "\n\n" + context_text}]}]}
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    if 'error' in result:
        print("Gemini API Error:", result['error'])
        return None
    try:
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print("Error parsing Gemini response:", e)
        return None

def parse_financial_metrics(pdf_text, company_config, api_key):
    # 1. Call Gemini API
    metric_prompt = company_config["EARNINGS"].get("metric_prompt", "")
    gemini_result = extract_metrics_with_gemini(metric_prompt, pdf_text, api_key)
    
    if not gemini_result:
        return None

    # 2. Clean Gemini output (remove ```json ... ``` if present)
    # Remove Markdown code fences and whitespace
    cleaned_result = re.sub(r"^```(?:json)?\s*|\s*```$", "", gemini_result.strip(), flags=re.IGNORECASE | re.MULTILINE)

    try:
        # 3. Convert string to JSON
        extracted_data = json.loads(cleaned_result)
    except json.JSONDecodeError as e:
        print("JSON Parse Error:", e)
        print("Gemini output was:", cleaned_result)
        return None

    # 4. Apply CAL_ACTUAL calculations if needed
    final_output = cleaned_result

    return final_output