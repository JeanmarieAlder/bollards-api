
import json
from os import name

from bollards_api.models import Bollard
from flask import Blueprint, jsonify

api = Blueprint('api', __name__, url_prefix='/api/v1')

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

