from src.lostinthemountains.utils.helpers import convert_coordinates
from src.lostinthemountains.utils.helpers import get_elevation_profile
from src.lostinthemountains.utils.helpers import find_steep_slopes

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/validate', methods=['POST'])
def validate():
    request_data = request.json
    geom = request_data['geom']
    geom['coordinates'] = convert_coordinates(geom['coordinates'], 'epsg:4326', 'epsg:2056', swap_coordinates=True)
    profile = get_elevation_profile(geom)
    return jsonify(find_steep_slopes(profile))


if __name__ == '__main__':
    app.run(debug=True)
