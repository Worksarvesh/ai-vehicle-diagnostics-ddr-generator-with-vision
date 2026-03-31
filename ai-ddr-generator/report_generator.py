from groq import Groq
import os
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

MODEL_NAME = "llama-3.3-70b-versatile"

def generate_report(merged_json, image_metadata):
    prompt = f"""You are an AI system that generates a structured DDR (Detailed Diagnostic Report).

Input:

1. Merged diagnostic JSON (already processed)
2. Image metadata extracted from reports (with page mapping)

Your task:
Generate a final DDR report with proper structure AND correctly placed images.

CRITICAL RULES:

* Do NOT invent any data
* Use ONLY given merged findings
* Insert images under the correct area (engine, brakes, tires, chain)
* If image is not available for a section → write "Image Not Available"
* Keep language simple and client-friendly
* Do NOT include unnecessary technical jargon

IMAGE MAPPING LOGIC:

* If image page relates to engine → place under engine
* If unclear → do NOT assign randomly
* Only use images when reasonably relevant

OUTPUT FORMAT:

1. Property Issue Summary

2. Area-wise Observations

Engine:

* Findings: []
* Image: [image_path OR "Image Not Available"]

Brakes:

* Findings: []
* Image: [image_path OR "Image Not Available"]

Tires:

* Findings: []
* Image: [image_path OR "Image Not Available"]

Chain:

* Findings: []
* Image: [image_path OR "Image Not Available"]

3. Probable Root Cause

4. Severity Assessment (with reasoning)

5. Recommended Actions

6. Additional Notes

7. Missing or Unclear Information

IMPORTANT:

* Keep formatting clean
* Keep output readable
* Do NOT return JSON — return formatted report
* If data has an "image_path", output exactly: [RENDER_IMAGE: <image_path>]. Otherwise, output "Image Not Available"

INPUT DATA:

Merged JSON:
{merged_json}

Image Metadata:
{image_metadata}

Now generate the final DDR report.
"""

    max_retries = 2
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            if "429" in str(e) or "ResourceExhausted" in str(e):
                if attempt < max_retries - 1:
                    print(f"Quota exceeded. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print("Max retries reached. Please wait or use a different API key.")
                    return "Error: API Quota Exceeded. Please wait 1-2 hours for quota reset, use a different API key, or upgrade to paid plan at https://console.groq.com/"
            else:
                print(f"API ERROR: {e}")
                return f"Error: {str(e)}"