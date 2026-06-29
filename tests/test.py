import json
import random
import uuid
from datetime import datetime, timedelta

# Define 100 distinct countries with representative coordinates and attributes
COUNTRY_POOL = [
    {"name": "Netherlands", "iso": "NL", "region": "EMEA",
     "cities": [("Amsterdam", "North Holland", 52.37, 4.89), ("Rotterdam", "South Holland", 51.92, 4.47)]},
    {"name": "Germany", "iso": "DE", "region": "EMEA",
     "cities": [("Berlin", "Berlin", 52.52, 13.40), ("Frankfurt", "Hesse", 50.11, 8.68)]},
    {"name": "France", "iso": "FR", "region": "EMEA",
     "cities": [("Paris", "Île-de-France", 48.85, 2.35), ("Lyon", "Auvergne-Rhône-Alpes", 45.76, 4.83)]},
    {"name": "United Kingdom", "iso": "GB", "region": "EMEA",
     "cities": [("London", "England", 51.50, -0.12), ("Manchester", "England", 53.48, -2.24)]},
    {"name": "United States", "iso": "US", "region": "AMER",
     "cities": [("New York", "NY", 40.71, -74.00), ("Washington", "DC", 38.90, -77.03)]},
    {"name": "Australia", "iso": "AU", "region": "APAC",
     "cities": [("Sydney", "NSW", -33.86, 151.20), ("Melbourne", "VIC", -37.81, 144.96)]},
    {"name": "Japan", "iso": "JP", "region": "APAC",
     "cities": [("Tokyo", "Tokyo", 35.67, 139.65), ("Osaka", "Osaka", 34.69, 135.50)]},
    {"name": "Canada", "iso": "CA", "region": "AMER",
     "cities": [("Toronto", "Ontario", 43.65, -79.38), ("Vancouver", "BC", 49.28, -123.12)]},
    {"name": "Brazil", "iso": "BR", "region": "AMER",
     "cities": [("São Paulo", "São Paulo", -23.55, -46.63), ("Rio de Janeiro", "Rio de Janeiro", -22.90, -43.17)]},
    {"name": "India", "iso": "IN", "region": "APAC",
     "cities": [("New Delhi", "Delhi", 28.61, 77.20), ("Mumbai", "Maharashtra", 19.07, 72.87)]},
    {"name": "South Africa", "iso": "ZA", "region": "EMEA",
     "cities": [("Johannesburg", "Gauteng", -26.20, 28.04), ("Cape Town", "Western Cape", -33.92, 18.42)]},
    {"name": "Singapore", "iso": "SG", "region": "APAC", "cities": [("Singapore", "Central Region", 1.35, 103.81)]},
    {"name": "Belgium", "iso": "BE", "region": "EMEA",
     "cities": [("Brussels", "Brussels", 50.85, 4.35), ("Antwerp", "Flanders", 51.21, 4.40)]},
    {"name": "Switzerland", "iso": "CH", "region": "EMEA",
     "cities": [("Zurich", "Zurich", 47.37, 8.54), ("Geneva", "Geneva", 46.20, 6.14)]},
    {"name": "Italy", "iso": "IT", "region": "EMEA",
     "cities": [("Rome", "Lazio", 41.90, 12.49), ("Milan", "Lombardy", 45.46, 9.18)]},
    {"name": "Spain", "iso": "ES", "region": "EMEA",
     "cities": [("Madrid", "Madrid", 40.41, -3.70), ("Barcelona", "Catalonia", 41.38, 2.17)]},
    {"name": "Sweden", "iso": "SE", "region": "EMEA", "cities": [("Stockholm", "Stockholm", 59.32, 18.06)]},
    {"name": "Norway", "iso": "NO", "region": "EMEA", "cities": [("Oslo", "Oslo", 59.91, 10.75)]},
    {"name": "Denmark", "iso": "DK", "region": "EMEA", "cities": [("Copenhagen", "Capital Region", 55.67, 12.56)]},
    {"name": "Finland", "iso": "FI", "region": "EMEA", "cities": [("Helsinki", "Uusimaa", 60.16, 24.93)]},
    {"name": "Austria", "iso": "AT", "region": "EMEA", "cities": [("Vienna", "Vienna", 48.20, 16.37)]},
    {"name": "Ireland", "iso": "IE", "region": "EMEA", "cities": [("Dublin", "Leinster", 53.34, -6.26)]},
    {"name": "Portugal", "iso": "PT", "region": "EMEA", "cities": [("Lisbon", "Lisbon", 38.72, -9.13)]},
    {"name": "Greece", "iso": "GR", "region": "EMEA", "cities": [("Athens", "Attica", 37.98, 23.72)]},
    {"name": "Poland", "iso": "PL", "region": "EMEA", "cities": [("Warsaw", "Mazovia", 52.22, 21.01)]},
    {"name": "Czechia", "iso": "CZ", "region": "EMEA", "cities": [("Prague", "Prague", 50.07, 14.43)]},
    {"name": "Hungary", "iso": "HU", "region": "EMEA", "cities": [("Budapest", "Central Hungary", 47.49, 19.04)]},
    {"name": "Romania", "iso": "RO", "region": "EMEA", "cities": [("Bucharest", "Ilfov", 44.42, 26.10)]},
    {"name": "Turkey", "iso": "TR", "region": "EMEA",
     "cities": [("Istanbul", "Istanbul", 41.00, 28.97), ("Ankara", "Ankara", 39.93, 32.85)]},
    {"name": "Egypt", "iso": "EG", "region": "EMEA", "cities": [("Cairo", "Cairo", 30.04, 31.23)]},
    {"name": "Saudi Arabia", "iso": "SA", "region": "EMEA", "cities": [("Riyadh", "Riyadh", 24.71, 46.67)]},
    {"name": "UAE", "iso": "AE", "region": "EMEA",
     "cities": [("Dubai", "Dubai", 25.20, 55.27), ("Abu Dhabi", "Abu Dhabi", 24.45, 54.37)]},
    {"name": "Israel", "iso": "IL", "region": "EMEA", "cities": [("Tel Aviv", "Tel Aviv", 32.08, 34.78)]},
    {"name": "Argentina", "iso": "AR", "region": "AMER", "cities": [("Buenos Aires", "CABA", -34.60, -58.38)]},
    {"name": "Chile", "iso": "CL", "region": "AMER", "cities": [("Santiago", "Santiago Metropolitan", -33.44, -70.66)]},
    {"name": "Colombia", "iso": "CO", "region": "AMER", "cities": [("Bogotá", "Cundinamarca", 4.71, -74.07)]},
    {"name": "Mexico", "iso": "MX", "region": "AMER", "cities": [("Mexico City", "CDMX", 19.43, -99.13)]},
    {"name": "Peru", "iso": "PE", "region": "AMER", "cities": [("Lima", "Lima", -12.04, -77.04)]},
    {"name": "China", "iso": "CN", "region": "APAC",
     "cities": [("Beijing", "Beijing", 39.90, 116.40), ("Shanghai", "Shanghai", 31.23, 121.47)]},
    {"name": "South Korea", "iso": "KR", "region": "APAC", "cities": [("Seoul", "Seoul", 37.56, 126.97)]},
    {"name": "Taiwan", "iso": "TW", "region": "APAC", "cities": [("Taipei", "Taipei", 25.03, 121.56)]},
    {"name": "Thailand", "iso": "TH", "region": "APAC", "cities": [("Bangkok", "Bangkok", 13.75, 100.50)]},
    {"name": "Malaysia", "iso": "MY", "region": "APAC", "cities": [("Kuala Lumpur", "KL", 3.13, 101.68)]},
    {"name": "Indonesia", "iso": "ID", "region": "APAC", "cities": [("Jakarta", "DKI Jakarta", -6.20, 106.81)]},
    {"name": "Philippines", "iso": "PH", "region": "APAC", "cities": [("Manila", "Metro Manila", 14.59, 120.98)]},
    {"name": "Vietnam", "iso": "VN", "region": "APAC", "cities": [("Hanoi", "Hanoi", 21.02, 105.83)]},
    {"name": "New Zealand", "iso": "NZ", "region": "APAC", "cities": [("Auckland", "Auckland", -36.84, 174.76)]},
    {"name": "Norway", "iso": "NO", "region": "EMEA", "cities": [("Bergen", "Vestland", 60.39, 5.32)]},
    {"name": "Ukraine", "iso": "UA", "region": "EMEA", "cities": [("Kyiv", "Kyiv", 50.45, 30.52)]},
    {"name": "Morocco", "iso": "MA", "region": "EMEA", "cities": [("Rabat", "Rabat-Salé-Kénitra", 34.02, -6.83)]},
    {"name": "Nigeria", "iso": "NG", "region": "EMEA", "cities": [("Lagos", "Lagos", 6.52, 3.37)]},
    {"name": "Kenya", "iso": "KE", "region": "EMEA", "cities": [("Nairobi", "Nairobi", -1.29, 36.82)]},
    {"name": "Ghana", "iso": "GH", "region": "EMEA", "cities": [("Accra", "Greater Accra", 5.60, -0.18)]},
    {"name": "Angola", "iso": "AO", "region": "EMEA", "cities": [("Luanda", "Luanda", -8.83, 13.23)]},
    {"name": "Ethiopia", "iso": "ET", "region": "EMEA", "cities": [("Addis Ababa", "Addis Ababa", 9.03, 38.74)]},
    {"name": "Pakistan", "iso": "PK", "region": "APAC", "cities": [("Islamabad", "Islamabad", 33.68, 73.04)]},
    {"name": "Bangladesh", "iso": "BD", "region": "APAC", "cities": [("Dhaka", "Dhaka", 23.81, 90.41)]},
    {"name": "Sri Lanka", "iso": "LK", "region": "APAC", "cities": [("Colombo", "Western Province", 6.92, 79.86)]},
    {"name": "Kazakhstan", "iso": "KZ", "region": "APAC", "cities": [("Astana", "Akfola", 51.16, 71.42)]},
    {"name": "Uzbekistan", "iso": "UZ", "region": "APAC", "cities": [("Tashkent", "Tashkent", 41.29, 69.24)]},
    {"name": "Qatar", "iso": "QA", "region": "EMEA", "cities": [("Doha", "Doha", 25.28, 51.53)]},
    {"name": "Oman", "iso": "OM", "region": "EMEA", "cities": [("Muscat", "Muscat", 23.58, 58.40)]},
    {"name": "Kuwait", "iso": "KW", "region": "EMEA", "cities": [("Kuwait City", "Al Asimah", 29.37, 47.97)]},
    {"name": "Jordan", "iso": "JO", "region": "EMEA", "cities": [("Amman", "Amman", 31.95, 35.91)]},
    {"name": "Lebanon", "iso": "LB", "region": "EMEA", "cities": [("Beirut", "Mount Lebanon", 33.89, 35.50)]},
    {"name": "Iraq", "iso": "IQ", "region": "EMEA", "cities": [("Baghdad", "Baghdad", 33.31, 44.36)]},
    {"name": "Algeria", "iso": "DZ", "region": "EMEA", "cities": [("Algiers", "Algiers", 36.75, 3.05)]},
    {"name": "Tunisia", "iso": "TN", "region": "EMEA", "cities": [("Tunis", "Tunis", 36.80, 10.18)]},
    {"name": "Panama", "iso": "PA", "region": "AMER", "cities": [("Panama City", "Panama", 8.98, -79.51)]},
    {"name": "Costa Rica", "iso": "CR", "region": "AMER", "cities": [("San José", "San José", 9.92, -84.08)]},
    {"name": "Guatemala", "iso": "GT", "region": "AMER", "cities": [("Guatemala City", "Guatemala", 14.63, -90.50)]},
    {"name": "Ecuador", "iso": "EC", "region": "AMER", "cities": [("Quito", "Pichincha", -0.18, -78.46)]},
    {"name": "Uruguay", "iso": "UY", "region": "AMER", "cities": [("Montevideo", "Montevideo", -34.90, -56.16)]},
    {"name": "Paraguay", "iso": "PY", "region": "AMER", "cities": [("Asunción", "Distrito Capital", -25.26, -57.57)]},
    {"name": "Bolivia", "iso": "BO", "region": "AMER", "cities": [("Sucre", "Chuquisaca", -19.03, -65.26)]},
    {"name": "Venezuela", "iso": "VE", "region": "AMER", "cities": [("Caracas", "Capital District", 10.48, -66.90)]},
    {"name": "Dominican Republic", "iso": "DO", "region": "AMER",
     "cities": [("Santo Domingo", "Distrito Nacional", 18.48, -69.89)]},
    {"name": "Cuba", "iso": "CU", "region": "AMER", "cities": [("Havana", "La Habana", 23.11, -82.36)]},
    {"name": "Jamaica", "iso": "JM", "region": "AMER", "cities": [("Kingston", "Surrey", 17.97, -76.79)]},
    {"name": "Croatia", "iso": "HR", "region": "EMEA", "cities": [("Zagreb", "Zagreb", 45.81, 15.97)]},
    {"name": "Slovakia", "iso": "SK", "region": "EMEA", "cities": [("Bratislava", "Bratislava", 48.14, 17.10)]},
    {"name": "Slovenia", "iso": "SI", "region": "EMEA", "cities": [("Ljubljana", "Ljubljana", 46.05, 14.50)]},
    {"name": "Bulgaria", "iso": "BG", "region": "EMEA", "cities": [("Sofia", "Sofia-Grad", 42.69, 23.32)]},
    {"name": "Serbia", "iso": "RS", "region": "EMEA", "cities": [("Belgrade", "Central Serbia", 44.78, 20.44)]},
    {"name": "Lithuania", "iso": "LT", "region": "EMEA", "cities": [("Vilnius", "Vilnius", 54.68, 25.27)]},
    {"name": "Latvia", "iso": "LV", "region": "EMEA", "cities": [("Riga", "Riga", 56.94, 24.10)]},
    {"name": "Estonia", "iso": "EE", "region": "EMEA", "cities": [("Tallinn", "Harju", 59.43, 24.75)]},
    {"name": "Iceland", "iso": "IS", "region": "EMEA", "cities": [("Reykjavik", "Capital Region", 64.14, -21.94)]},
    {"name": "Cyprus", "iso": "CY", "region": "EMEA", "cities": [("Nicosia", "Nicosia", 35.16, 33.36)]},
    {"name": "Malta", "iso": "MT", "region": "EMEA", "cities": [("Valletta", "South Eastern", 35.89, 14.51)]},
    {"name": "Luxembourg", "iso": "LU", "region": "EMEA", "cities": [("Luxembourg", "Luxembourg", 49.61, 6.13)]},
    {"name": "Monaco", "iso": "MC", "region": "EMEA", "cities": [("Monaco", "Monaco", 43.73, 7.42)]},
    {"name": "Liechtenstein", "iso": "LI", "region": "EMEA", "cities": [("Vaduz", "Vaduz", 47.14, 9.52)]},
    {"name": "Svalbard", "iso": "SJ", "region": "EMEA", "cities": [("Longyearbyen", "Spitsbergen", 78.22, 15.63)]},
    {"name": "Greenland", "iso": "GL", "region": "AMER", "cities": [("Nuuk", "Sermersooq", 64.17, -51.73)]},
    {"name": "Fiji", "iso": "FJ", "region": "APAC", "cities": [("Suva", "Rewa", -18.12, 178.45)]},
    {"name": "Papua New Guinea", "iso": "PG", "region": "APAC",
     "cities": [("Port Moresby", "National Capital District", -9.44, 147.17)]},
    {"name": "Mongolia", "iso": "MN", "region": "APAC", "cities": [("Ulaanbaatar", "Ulaanbaatar", 47.88, 106.90)]},
    {"name": "Nepal", "iso": "NP", "region": "APAC", "cities": [("Kathmandu", "Bagmati", 27.71, 85.32)]},
    {"name": "Cambodia", "iso": "KH", "region": "APAC", "cities": [("Phnom Penh", "Phnom Penh", 11.55, 104.91)]}
]

INCIDENT_TEMPLATES = [
    {"category": "security", "subcategory": "shooting",
     "title": "Security measures increased following shooting incident",
     "summary": "Local authorities deployed auxiliary forces after a public shooting incident. Investigation is ongoing."},
    {"category": "protest", "subcategory": "civil_unrest", "title": "Demonstration blocks main municipal intersection",
     "summary": "Unannounced activist group assembly caused dynamic traffic diversions. Law enforcement is monitoring the perimeter."},
    {"category": "infrastructure", "subcategory": "power_outage",
     "title": "Substation failure causes regional power grid outage",
     "summary": "Technical malfunctions at a key electrical distribution node caused localized blackouts. Technicians are on scene."},
    {"category": "hazard", "subcategory": "industrial_spill",
     "title": "Chemical logistics terminal logs localized spill containment",
     "summary": "Response crews isolated a minor valve rupture tracking storage assets. No secondary public health risks reported."},
    {"category": "transportation", "subcategory": "rail_delay",
     "title": "Freight train technical failure disrupts rail transit corridor",
     "summary": "Mechanical lockups halted a commercial transit train along a primary line route. Expect shipping delays."}
]

SEVERITY_MAPPINGS = {
    1: ("low", "moderate"),
    2: ("low-medium", "moderate"),
    3: ("medium", "substantial"),
    4: ("high", "severe"),
    5: ("critical", "extreme")
}


def generate_bulk_dataset():
    end_date = datetime(2026, 6, 29, 12, 0, 0)
    start_date = end_date - timedelta(days=30)
    total_records = 3000

    events = []

    for i in range(1, total_records + 1):
        # 1. Select geography assets
        #  Replace with this
        country_obj = random.choice(COUNTRY_POOL)
        city_obj = random.choice(country_obj["cities"])

        # 2. Select contextual telemetry patterns
        template = random.choice(INCIDENT_TEMPLATES)
        sev_tier = random.choices([1, 2, 3, 4, 5], weights=[40, 30, 18, 9, 3])[0]
        sev_label, disruption = SEVERITY_MAPPINGS[sev_tier]

        # 3. Create temporal offset frames within the targeted window
        random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
        published_dt = start_date + timedelta(seconds=random_seconds)
        updated_dt = published_dt + timedelta(hours=random.randint(1, 6))
        start_dt = published_dt - timedelta(hours=random.randint(1, 4))

        evt_id = f"seerist_evt_p2_{str(i).zfill(6)}"

        # 4. Construct event dictionary
        event_node = {
            "source": "seerist_synthetic",
            "schema_version": "synthetic-seerist-v1.0",
            "event_id": evt_id,
            "kind": "event",
            "title": f"{template['title']} in {city_obj[0]}",
            "summary": f"Authorities in {city_obj[0]} issued reports regarding: {template['summary']}",
            "category": template["category"],
            "subcategory": template["subcategory"],
            "severity": sev_tier,
            "severity_label": sev_label,
            "status": random.choice(["active", "resolved", "monitored"]),
            "confidence": round(random.uniform(0.65, 0.98), 2),
            "published_at": published_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "updated_at": updated_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "start_time": start_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "end_time": None if sev_tier > 2 else updated_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "location": {
                "country": country_obj["name"],
                "country_iso2": country_obj["iso"],
                "city": city_obj[0],
                "admin_area": city_obj[1],
                "latitude": round(city_obj[2] + random.uniform(-0.02, 0.02), 5),
                "longitude": round(city_obj[3] + random.uniform(-0.02, 0.02), 5),
                "geo_precision": "district"
            },
            "region": country_obj["region"],
            "provenance": {
                "source_count": random.randint(1, 5),
                "source_types": random.sample(["social_media", "local_news", "government_feed"], random.randint(1, 2)),
                "human_reviewed": random.choice([True, False]),
                "analyst_confidence_note": "Synthetic profile matches baseline telemetry specifications."
            },
            "impact": {
                "affected_domains": random.sample(["travel", "medical", "logistics", "commercial"], 2),
                "likely_disruption": disruption,
                "recommended_actions": [
                    "Maintain standard situational awareness protocols.",
                    "Review regional tracking coordinates for proximity updates."
                ]
            },
            "tags": [template["category"], template["subcategory"], "automated_generation"],
            "language": "en",
            "assets_nearby": [],
            "raw_text": f"Synthetic Seerist incident update tracking structural {template['category']} events across {city_obj[0]}, {country_obj['name']}.",
            "duplicate_hint": None,
            "synthetic_notice": "This is synthetic test data for a PoC and does not represent real Seerist data or real-world intelligence."
        }
        events.append(event_node)

    # Base wrapper structure
    dataset_wrapper = {
        "dataset_name": "synthetic_seerist_events_for_intel_fusion_poc",
        "dataset_version": "1.0",
        "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "record_count": total_records,
        "description": "Synthetic Seerist-style event feed for testing ingestion, normalization, enrichment, embeddings, deduplication, retrieval and briefing workflows. This file is not based on proprietary Seerist exports and contains no real intelligence.",
        "schema_notes": {
            "format": "JSON object with an events array",
            "primary_key": "event_id",
            "time_format": "ISO-8601 UTC",
            "severity_scale": "1=low, 2=low-medium, 3=medium, 4=high, 5=critical",
            "duplicate_hint": "If populated, indicates an intentional synthetic near-duplicate of another synthetic event. Use only for testing/evaluation."
        },
        "events": events
    }

    # Write out data directly as a clean formatted JSON asset
    with open("test_data_3000_p2.json", "w", encoding="utf-8") as out_file:
        json.dump(dataset_wrapper, out_file, indent=2, ensure_ascii=False)

    print("Successfully generated 'test_data_3000.json' containing 3,000 contextual validation rows.")


if __name__ == "__main__":
    generate_bulk_dataset()
