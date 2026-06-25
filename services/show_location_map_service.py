import folium
from flask import request

def show_location_map_service():
    ## Pulls events from normalized DB and puts them into a interactive map.
    ## NOTE = The logic here and in the HTML file is written by me,
    ## however AI was used for the HTML part and the parts surrounding the logic that creates the map.
    lat = request.args.get('lat')
    lng = request.args.get('lon')
    event_title = request.args.get('title')

    custom_popup = folium.Popup(
        html=f"<b>{event_title}</b>",
        max_width=450)

    m = folium.Map(location=[float(lat), float(lng)], zoom_start=11, tiles='CartoDB.Positron')
    (folium.Marker(location=[float(lat), float(lng)],
                  tooltip='Click for more info',
                  popup=custom_popup,
                  icon=folium.Icon(color="red")
                   ) .add_to(m))

    return m._repr_html_()