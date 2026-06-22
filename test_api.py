import requests

# Your local Flask endpoint URL
url = "http://127.0.0.1:5000/normalize_ingest_seerist"

# The raw Seerist synthetic payload
mock_payload = {
  "source": "seerist_synthetic",
  "schema_version": "synthetic-seerist-v1.0",
  "event_id": "seerist_evt_10001",
  "kind": "event",
  "title": "Ransomware Attack Disrupts Frankfurt Logistics Hub",
  "summary": "A significant ransomware variant has locked critical operational databases at a major freight distribution center in Frankfurt, causing notable container sorting delays.",
  "category": "cybersecurity",
  "subcategory": "ransomware",
  "severity": 3,
  "severity_label": "high",
  "status": "active",
  "confidence": 0.91,
  "published_at": "2026-06-22T10:15:30.124552Z",
  "updated_at": "2026-06-22T12:45:12.893441Z",
  "start_time": "2026-06-22T08:00:00.000000Z",
  "end_time": None,
  "location": {
    "country": "Germany",
    "country_iso2": "DE",
    "city": "Frankfurt",
    "admin_area": "Hesse",
    "latitude": 50.11092,
    "longitude": 8.68213,
    "geo_precision": "city"
  },
  "region": "EMEA",
  "provenance": {
    "source_count": 3,
    "source_types": [
      "local_news",
      "infosec_feed"
    ],
    "human_reviewed": True,
    "analyst_confidence_note": "Incident confirmed by multiple independent cybersecurity firms and local corporate press releases."
  },
  "impact": {
    "affected_domains": [
      "supply_chain",
      "technology"
    ],
    "likely_disruption": "severe",
    "recommended_actions": [
      "Isolate affected network segments immediately.",
      "Deploy fallback manual processing for critical freight routing.",
      "Monitor secondary supply chain partners for potential lateral migration.",
      "Engage corporate incident response teams."
    ]
  },
  "tags": [
    "cybersecurity",
    "ransomware",
    "supply_chain",
    "infrastructure"
  ],
  "language": "en",
  "assets_nearby": [],
  "raw_text": "Synthetic Seerist-style intelligence event. A significant ransomware variant has locked critical operational databases at a major freight distribution center in Frankfurt, causing notable container sorting delays. Severity is assessed as high. Recommended actions: Isolate affected network segments immediately. Deploy fallback manual processing for critical freight routing. Monitor secondary supply chain partners for potential lateral migration. Engage corporate incident response teams.",
  "duplicate_hint": None,
  "synthetic_notice": "This is synthetic test data for a PoC and does not represent real Seerist data or real-world intelligence."
}

print("🚀 Firing payload to local Flask server...")
response = requests.post(url, json=mock_payload)

# Check the results
if response.status_code == 201:
    print("\n🎉 Success! Server responded with:")
    print(response.json())
else:
    print(f"\n❌ Error! Status code: {response.status_code}")
    print(response.text)