def normalize_event_seerist(raw_event_seerist: dict):

    ## Normalizes an incoming seerist event into a standard format ##

    location_data = raw_event_seerist['location']

    return {

        'normalized_event_id': f"ss_normalized_{raw_event_seerist['event_id']}",  # Unique ID for the normalized event
        'original_event_id': raw_event_seerist['event_id'],  # Keep track of the original ID
        'source_name': 'seerist',
        'event_type': raw_event_seerist['category'],
        'title': raw_event_seerist['title'],
        'description': raw_event_seerist['raw_text'],
        "category": raw_event_seerist['category'],
        "severity": raw_event_seerist['severity'],
        "confidence": raw_event_seerist['confidence'],
        "time_stamp": raw_event_seerist['start_time'],
        "country": location_data.get('country', 'Unknown'),
        'region': raw_event_seerist['region'],
        'city': location_data.get('city', 'Unknown'),
        'latitude': location_data.get('latitude', 'Unknown'),
        'longitude': location_data.get('longitude', 'Unknown'),

    }
