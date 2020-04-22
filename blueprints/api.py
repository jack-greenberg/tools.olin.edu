from flask import Blueprint, jsonify, request
import json
from werkzeug.utils import secure_filename
from flask.views import MethodView
from flask_jwt_extended import fresh_jwt_required, get_jwt_claims, get_jwt_identity
from datetime import datetime, timezone
import os
from modules.db import User, Tool, db

api = Blueprint('api', __name__, url_prefix='/api')

def pull_jwt_data(rq):
    token = None
    if 'x-access-tokens' in request.headers:
         token = request.headers['x-access-tokens']

    if not token:
         return jsonify({'message': 'a valid token is missing'})

    try:
        data = get_jwt_claims
        #  current_user = Users.query.filter_by(public_id=data['public_id']).first()
    except:
        return jsonify({'message': 'token is invalid'})

def register_api(blueprint, view, endpoint, url, pk='id', pk_type='string'):
    view_func = view.as_view(endpoint)
    blueprint.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET',])
    blueprint.add_url_rule(url, view_func=view_func, methods=['POST',])
    blueprint.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func, methods=['POST', 'GET', 'PUT', 'DELETE'])

class TrainingAPI(MethodView):
    decorators = [fresh_jwt_required]
    def get(self, tool, user):
        jwt_data = get_jwt_identity()
        claims = get_jwt_claims()

        return None

    def post(self, tool, user):
        pass

    def put(self, tool, user):
        pass

    def delete(self, tool, user):
        pass

class LogAPI(MethodView):
    decorators = [fresh_jwt_required]
    pass

register_api(api, TrainingAPI, 'site_api', '/siteData/', pk='tool', pk_type='string')
