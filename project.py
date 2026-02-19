import os
from googleapiclient.discovery import build
import google.generativeai as genai

# --- 1. Configuration ---
# Use the keys you generated in Google AI Studio and Google Cloud Console
GEMINI_API_KEY = "AIzaSyC3CD25DRQ9ITQJGNfRL1KkWS4y0iIe7GY" 
GOOGLE_API_KEY = "YOUR_GOOGLE_CLOUD_KEY"
SEARCH_ENGINE_ID = "41b8bca57c1154cdb"

# --- 2. Search Tool ---
def search_medicine_info(medicine_name: str):
    """Searches Google for medicine details, side effects, and alternatives."""
    try:
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        query = f"{medicine_name} medical uses and side effects"
        res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=3).execute()
        
        items = res.get('items', [])
        if not items:
            return "No information found."

        return "\n\n".join([f"Source: {i['title']}\n{i['snippet']}" for i in items])
    except Exception as e:
        return f"Search Error: {str(e)}"

# --- 3. Initialize AI ---
genai.configure(api_key=GEMINI_API_KEY)

# We wrap the function in a list for the tools parameter
model = genai.GenerativeModel(
    model_name='gemini-flash-latest',
    tools=[search_medicine_info]
)

# --- 4. Main Loop ---
def main():
    # This 'automatic' mode handles the search and summary for you!
    chat = model.start_chat(enable_automatic_function_calling=True)
    
    print("\n--- Medical AI Agent Ready ---")
    print("Type a medicine (e.g., Aspirin) or 'exit' to quit.")

    while True:
        user_input = input("\nMedicine Name: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            break
        if not user_input:
            continue

        try:
            print("Searching and thinking...")
            response = chat.send_message(user_input)
            print(f"\nAssistant: {response.text}")
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()