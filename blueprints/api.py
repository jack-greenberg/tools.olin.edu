from flask import Blueprint, jsonify, request
import json
from werkzeug.utils import secure_filename
from flask.views import MethodView
from flask_jwt_extended import fresh_jwt_required, get_jwt_claims, get_jwt_identity
from datetime import datetime, timezone
import os
from modules.db import User, Tool, ToolCategory, db

api = Blueprint('api', __name__, url_prefix='/api')

# def pull_jwt_data(rq):
#     token = None
#     if 'x-access-tokens' in request.headers:
#          token = request.headers['x-access-tokens']
#
#     if not token:
#          return jsonify({'message': 'a valid token is missing'})
#
#     try:
#         data = get_jwt_claims
#         #  current_user = Users.query.filter_by(public_id=data['public_id']).first()
#     except:
#         return jsonify({'message': 'token is invalid'})

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

class ToolAPI(MethodView):
    def get(self, tool):
        if tool == None:
            query = Tool.query.all()
            tool_list = [
                {
                    'id': tool.id,
                    'name': tool.name,
                    'category': {
                        'id': tool.category.id,
                        'name': tool.category.name,
                    },
                    'shortname': tool.shortname
                }
            for tool in query]

            return jsonify(tool_list)
        else:
            _tool = Tool.query.filter_by(shortname=tool).first_or_404()
            return jsonify(_tool)

    def post(self):
        try:
            _category = ToolCategory.query.filter_by(name=request.form['category']).first()
            if _category == None:
                _category = ToolCategory(name=request.form['category'])
                db.session.add(_category)

            tool = Tool(name=request.form['name'], shortname=request.form['shortname'], category=_category)

            db.session.add(tool)
            db.session.commit()
            return jsonify("Inserted: <Tool name=\"%s\" category=\"%s\"" % (request.form['name'], request.form['category'])), 201
        except KeyError:
            return jsonify()

    def put(self, tool):
        pass

    def delete(self, tool):
        pass

register_api(api, TrainingAPI, 'training_api', '/trainings/', pk='tool', pk_type='string')
register_api(api, ToolAPI, 'tool_api', '/tools/', pk='tool', pk_type='string')
