import json

from pyproj import Proj, itransform
import requests


def convert_coordinates(coordinates, source_crs, target_crs, swap_coordinates=False):
    if swap_coordinates:
        coordinates = [[coord[1], coord[0]] for coord in coordinates]
    source_crs = Proj(projparams=source_crs)
    target_crs = Proj(projparams=target_crs)
    result = list(itransform(source_crs, target_crs, coordinates))
    return [list(coord) for coord in result]


def encode_geojson_string(geojson_string):
    geojson_string.replace('\"', '%22')
    geojson_string.replace(',', '%2C')
    geojson_string.replace(' ', '%3A')
    return geojson_string


def get_elevation_profile(geometry):
    url = 'https://api3.geo.admin.ch/rest/services/profile.json'
    response = requests.post(url, data=json.dumps(geometry))
    return json.loads(response.content.decode('utf-8'))


def find_steep_slopes(profile, step_size=100, slope=30):
    start_point = profile.pop(0)
    current_altitude = start_point['alts']['COMB']
    current_distance = 0
    coordinates = []

    for p in profile:
        distance = p['dist']
        altitude = p['alts']['COMB']
        delta_distance = distance - current_distance
        if delta_distance > step_size:
            delta_altidute = altitude - current_altitude
            delta_slope = abs(delta_altidute / delta_distance * 100)
            if delta_slope > slope:
                coordinates.append(convert_coordinates([[p['easting'], p['northing']]],
                                                       'epsg:2056',
                                                       'epsg:4326')[0])
            current_altitude = altitude
            current_distance = distance
    return {"is_dangerous": True if coordinates else False,
            "coordinates": coordinates}
