import json
import requests

# Your local Flask endpoint URL
url = "http://127.0.0.1:5000/normalize_ingest_seerist"
file_path = "../synthetic_seerist_events.json"

print(f"📖 Opening local file: {file_path}...")

try:
    # 1. Open and load the JSON dataset file
    with open(file_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    # 2. Extract the events list array from the wrapper object
    event_list = dataset.get("events", [])
    total_events = len(event_list)

    print(f"🚀 Found {total_events} events. Beginning sequential transmission to Flask server...\n")
    counter = 0

    # 3. Loop through every single event item in the file array
    for idx, event in enumerate(event_list, start=1):

        event_id = event.get("event_id", "UNKNOWN")
        title = event.get("title", "No Title")

        # Stream the progress updates to console
        print(f"[{idx}/{total_events}] Sending ID: {event_id} -> \"{title}\"")

        # Fire the single raw event payload to the Flask API
        response = requests.post(url, json=event)

        # Verify the database pipeline accepted it safely


        if response.status_code not in [200, 201]:
            print(f"  ❌ Error on Event #{idx}! Status code: {response.status_code}")
            print(f"  Response text: {response.text}\n")
            break  # Stop execution if an injection crash occurs so you can inspect it
        counter += 1
        print(counter)

    else:
        print("\n✨ All 1,000 events successfully loaded from file, normalized, and stored in both databases!")

except FileNotFoundError:
    print(f"\n❌ File Not Found! Make sure '{file_path}' is saved in the exact same directory as this test script.")
except json.JSONDecodeError:
    print(
        f"\n❌ JSON Syntax Error! Check if your '{file_path}' file has a missing brace or cut-off entry at the bottom.")