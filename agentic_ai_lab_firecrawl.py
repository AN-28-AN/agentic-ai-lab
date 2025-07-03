# agentic_ai_lab_firecrawl.py
# Agentic AI Lab: Using Firecrawl API + Offline LLM + Actionable Agent (PDF generation)

import ollama
import requests
from fpdf import FPDF

# ========== CONFIGURATION ==========
FIRECRAWL_API_KEY = 'fc-5c35e16f5b4e49efa818446cdd453d20'  # Replace with your actual Firecrawl API key
FIRECRAWL_URL = 'https://api.firecrawl.dev/v1/scrape'
MODEL_NAME = 'mistral'  # Adjust as needed (must be installed in Ollama)

# ========== DATA COLLECTION FROM WEB ==========
def collect_data_from_url(url):
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {FIRECRAWL_API_KEY}'
    }
    json_data = {
        'url': url
    }
    
    try:
        response = requests.post(FIRECRAWL_URL, headers=headers, json=json_data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return ""
    except Exception as e:
        print(f"Request error: {e}")
        return ""
    
    try:
        data = response.json()
    except Exception:
        print("Non-JSON response:", response.text)
        raise
    
    if not data.get('text'):
        print("Full API response:", data)
    
    # Try to get 'text', then 'data.markdown', else empty string
    return data.get('text') or data.get('data', {}).get('markdown', '')

# ========== PROCESS USING OFFLINE LLM ==========
def process_with_llm(content):
    print("\nProcessing content with offline LLM...")
    
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{
            'role': 'user',
            'content': (
                "Please summarize and extract key actionable insights from the following content "
                "for a cybersecurity student:\n\n" + content
            )
        }]
    )
    
    return response['message']['content']

# ========== GENERATE PDF REPORT ==========
def generate_pdf(content, filename="agentic_ai_summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    lines = content.split('\n')
    for line in lines:
        pdf.multi_cell(0, 10, line)
    
    pdf.output(filename)
    print(f"PDF report generated: {filename}")

# ========== MAIN EXECUTION FLOW ==========
def main():
    print("=== Agentic AI Lab: Firecrawl + Offline LLM + PDF Generator ===")
    
    try:
        url = input("Enter the URL to collect data from: ")
        scraped_text = collect_data_from_url(url)
        
        if not scraped_text:
            print("No content retrieved from the URL.")
            return
        
        summary = process_with_llm(scraped_text)
        print("\n--- LLM Processed Summary ---")
        print(summary)
        
        generate_pdf(summary)
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()