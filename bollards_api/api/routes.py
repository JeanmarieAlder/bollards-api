
import json
from os import name

from flask_cors import CORS

from bollards_api.models import Bollard
from flask import Blueprint, jsonify

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


@api.route('/bollards/paginate/<int:page>')
def bollards_paginate(page):
    bollards = Bollard.query.order_by(Bollard.b_number, 
                    Bollard.b_letter).paginate(page=page, per_page=2)
    print(dir(bollards))
    resp = []
    
    return jsonify({
        "has_next": bollards.has_next,
        "has_prev": bollards.has_prev,
        "items": str(bollards.items),
        # "iter_pages": bollards.iter_pages,
        # "next": bollards.next,
        "next_num": bollards.next_num,
        "page": bollards.page,
        "pages": bollards.pages,
        "per_page": bollards.per_page,
        # "prev": bollards.prev,
        "prev_num": bollards.prev_num,
        "query": str(bollards.query),
        "total": bollards.total
    })