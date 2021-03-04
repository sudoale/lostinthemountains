import json

from pyreproj import Reprojector
import requests


def convert_coordinates(coordinates, source_crs, target_crs):
    transform = Reprojector().get_transformation_function(from_srs=source_crs, to_srs=target_crs)
    return [list(transform(coord[1], coord[0])) for coord in coordinates]

def encode_geojson_string(geojson_string):
    geojson_string.replace('\"', '%22')
    geojson_string.replace(',', '%2C')
    geojson_string.replace(' ', '%3A')
    return geojson_string


def get_elevation_profile(geometry):
    base_url = 'https://api3.geo.admin.ch/rest/services/profile.json?geom='
    json_string = json.dumps(geometry)
    json_string = encode_geojson_string(json_string)
    response = requests.get(base_url + json_string)
    return json.loads(response.content.decode('utf-8'))
