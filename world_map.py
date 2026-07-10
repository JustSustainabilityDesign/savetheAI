#!/usr/bin/env python
# coding: utf-8

import glob
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
from folium.plugins import MarkerCluster

geolocator = Nominatim(user_agent="location_mapper", timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
location_dict = {}
location = ""
permalink = ""
title = ""
m = folium.Map(location=[20, 0], zoom_start=1.8)
marker_cluster = MarkerCluster(
    options={
        'showCoverageOnHover': False, 
        'disableClusteringAtZoom': 10   
    }
).add_to(m)


with open("locations.md", 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()  
        if line.startswith('Location: '):  
            location = line.split(': ')[1]

        location_dict[location] = geocode(location)
        print(location_dict[location])

        geocoded_location = geocode(location)
        if geocoded_location:
                latitude = geocoded_location.latitude
                longitude = geocoded_location.longitude
                print(latitude, longitude)

        folium.Marker(
                    location=[latitude, longitude],
                    popup=location
                ).add_to(marker_cluster)


m.save("location_map.html")

