from groq import Groq
import json
import os
import re
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

# Using llama-3.3-70b-versatile for extraction
MODEL_NAME = "llama-3.3-70b-versatile"

def extract_structured_data(inspection_text, thermal_text):
    prompt = f"""
You are a strict information extraction engine for a diagnostic system.

Your task is to extract structured data from two inputs:
1. Inspection Report
2. Thermal Report

CRITICAL RULES (must follow):
* DO NOT summarize or combine information
* DO NOT infer or guess anything
* Extract ONLY what is explicitly present
* Keep Inspection and Thermal data strictly separate
* Maintain traceability of every point
* If any data is missing, return "Not Available"
* If a section is not mentioned, still include it with "Not Available"
* Output must be clean, valid JSON (no explanations)

AREAS to extract (fixed):
* engine
* brakes
* tires
* chain

For EACH area, extract:
inspection:
* observations (exact text or cleaned phrase)
* condition (if mentioned)
* notes (if any)

thermal:
* temperature (if available)
* observation (e.g., heat buildup, anomaly)
* notes (if any)

Also extract:
meta:
* vehicle (if available)
* date (if available)

OUTPUT FORMAT:
{{
  "meta": {{
    "vehicle": "",
    "date": ""
  }},
  "engine": {{
    "inspection": {{
      "observations": "",
      "condition": "",
      "notes": ""
    }},
    "thermal": {{
      "temperature": "",
      "observation": "",
      "notes": ""
    }}
  }},
  "brakes": {{}},
  "tires": {{}},
  "chain": {{}}
}}

IMPORTANT:
* If no thermal data for an area → fill thermal fields with "Not Available"
* If no inspection data → fill inspection fields with "Not Available"
* Keep values short and factual
* Do not merge inspection and thermal content

INPUT:
Inspection Report:
{inspection_text[:12000]}

Thermal Report:
{thermal_text[:12000]}

Now return ONLY the JSON output.
"""

    max_retries = 2
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )
            
            try:
                content = response.choices[0].message.content
                json_match = re.search(r'\{(?:[^{}]|(?(?=\{).*))\}', content, re.DOTALL)
                if not json_match:
                    # Generic fallback if the whole object matches
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                
                if json_match:
                    return json.loads(json_match.group())
                return {}
            except Exception as e:
                print("JSON ERROR:", e)
                return {}
        except Exception as e:
            if "429" in str(e) or "ResourceExhausted" in str(e):
                if attempt < max_retries - 1:
                    print(f"Quota exceeded. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print("Max retries reached. Please wait or use a different API key.")
                    return {"Error": "API Quota Exceeded"}
            else:
                print(f"API ERROR: {e}")
                return {}