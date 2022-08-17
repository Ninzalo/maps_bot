import osmnx as ox
import networkx as nx
import folium

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

import os
import datetime


ox.config(log_console=False, use_cache=True)
locator = Nominatim(user_agent = "myapp")

start_time = datetime.datetime.now()
# define the start and end locations in latlng
start_location = "6 Пулковская улица Москва"
end_location = "20 Кронштадтский бульвар Москва"

try:
    # stores the start and end points as geopy.point.Point objects
    start_latlng = locator.geocode(start_location)
    start_lat, start_lon = float(start_latlng.latitude), float(start_latlng.longitude)
    location_test = locator.reverse(f'{start_lat}, {start_lon}')
    print(start_lat, start_lon)
    print(location_test.address)
    end_latlng = locator.geocode(end_location)
    end_lat, end_lon = float(end_latlng.latitude), float(end_latlng.longitude)

    # print(f'Distance - {geodesic((start_lon, start_lat), (end_lon, end_lat)).km} km')

    place = 'Москва Россия'

    # find shortest route based on the mode of travel
    mode = 'walk' # 'drive', 'bike', 'walk'

    optimizer = 'length' # 'length','time'

    if not os.path.exists(f'graph_{place}.osm'):
        graph = ox.graph_from_place(place, network_type = mode)

        ox.save_graphml(graph, filepath=f'graph_{place}.osm')

    graph = ox.load_graphml(filepath=f'graph_{place}.osm')

    orig_node = ox.nearest_nodes(graph, start_lon, start_lat)

    dest_node = ox.nearest_nodes(graph, end_lon, end_lat)

    # find the shortest path
    shortest_route = nx.shortest_path(graph, orig_node, dest_node,
                                      weight=optimizer)


    start_marker = folium.Marker(
                location = (start_lat, start_lon),
                popup = start_location,
                icon = folium.Icon(color='green'))

    end_marker = folium.Marker(
                location = (end_lat, end_lon),
                popup = end_location,
                icon = folium.Icon(color='red'))

    shortest_route_map = ox.plot_route_folium(graph, shortest_route, 
                                              tiles='openstreetmap')
    # add the circle marker to the map
    start_marker.add_to(shortest_route_map)
    end_marker.add_to(shortest_route_map)

    # save the map file
    shortest_route_map.save(f'myapp.html')
except Exception as _ex:
    print(_ex)
    pass

print(f'Elapsed time - {datetime.datetime.now() - start_time}')
