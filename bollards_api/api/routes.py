
import json
from os import name

from flask_cors import CORS

from bollards_api.models import Bollard
from flask import Blueprint, jsonify

from bollards_api.api.utils import get_neighbours_by_number

api = Blueprint('api', __name__, url_prefix='/api/v1')

CORS(api)

@api.route('/bollards/list')
def bollards_list():
    bollards = Bollard.query.all()
    resp = []
    for bollard in bollards:
        resp.append({
            "id": bollard.id,
            "b_number": bollard.b_number,
            "b_letter": bollard.b_letter,
            "b_name": bollard.b_name,
            "image_icon": bollard.image_icon

        })
    return jsonify(resp)


@api.route('/bollards/markers')
def bollards_markers():
    bollards = Bollard.query.all()
    resp = []
    for bollard in bollards:
        resp.append({
            "id": bollard.id,
            "b_number": bollard.b_number,
            "b_letter": bollard.b_letter,
            "b_name": bollard.b_name,
            "b_type": bollard.b_type,
            "image_icon": bollard.image_icon,
            "b_lat": str(bollard.b_lat),
            "b_lng": str(bollard.b_lng)
        })
    return jsonify(resp)


@api.route('/bollards/details/<int:bollard_id>')
def bollards_details(bollard_id):
    bollard = Bollard.query.filter_by(id=bollard_id).first_or_404()
    images = []
    for img in bollard.images:
        images.append(img.uri)
    neighbours = get_neighbours_by_number(bollard)
        
    return jsonify({
        'id': bollard.id,
        'b_number': bollard.b_number,
        'b_letter': bollard.b_letter,
        'b_type': bollard.b_type,
        'b_name': bollard.b_name,
        'comment': bollard.comment,
        'b_lat': str(bollard.b_lat),
        'b_lng': str(bollard.b_lng),
        'image_icon': bollard.image_icon,
        'images': images,
        'neighbours': neighbours
    })

