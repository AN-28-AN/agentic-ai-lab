# This script tests connectivity with your local LLM
import test_ollama

try:
    response = Ollama.chat(
        model='mistral',
        messages=[{role: 'user', content: 'Explain the CIA Triad in cybersecurity.'}]
    )
    print(response['message']['content'])
except Exception as e:
    print(f"An error occured: {e}")
    print("Please ensure the Ollama application us running.")