from flask import Blueprint, render_template, request, url_for, session, redirect, jsonify
from functools import wraps
from flask_jwt_extended import fresh_jwt_required, jwt_required, create_access_token, get_jwt_identity, jwt_refresh_token_required, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from werkzeug.security import check_password_hash, generate_password_hash, safe_str_cmp
import bcrypt
import json
from modules.db import User, Tool, db

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (request.method == 'GET'):
            try:
                if not session['username']:
                    return redirect(url_for('public.login', redirect=request.path))
            except KeyError:
                return redirect(url_for('public.login', redirect=request.path))
            return f(*args, **kwargs)
    return decorated_function

public = Blueprint('public', __name__, template_folder='../templates/public', static_folder='../static/')

@public.route('/')
def index():
    return render_template('index.j2')

@public.route('/users')
def users():
    return render_template('users.j2')

@public.route('/users/<u>')
def single_user(u):
    user = User.query.filter_by(username=u).first_or_404()
    return render_template('user.j2', user=user)

@public.route('/tools')
def tools():
    # fetch list of tools from database
    tool_object = {}
    tool_list = Tool.query.all()
    for tool in tool_list:
        try:
            tool_object[tool.category.name].append(tool)
        except KeyError:
            tool_object[tool.category.name] = [tool]
    return render_template('tools.j2', tool_object=tool_object)

@public.route('/tools/<tool>')
def single_tool(tool):
    tool = Tool.query.filter_by(shortname=tool).first_or_404()
    return render_template('tool.j2', tool=tool)

@public.route('/trainings')
def trainings():
    return render_template('trainings.j2')

@public.route('/api/token-refresh/', methods=['POST']) # refresh the token
@jwt_refresh_token_required # refresh token is needed to do this
def refresh():
    new_token = create_access_token(identity=get_jwt_identity(), fresh=True)
    response = jsonify({'access_token': new_token})
    return response

@public.route('/login', methods=['GET', 'POST'])
def login():

    # If the user is already logged in, send them to the admin page
    try:
        assert session['username']
        return redirect(url_for('public.index'))
    except (AssertionError, KeyError):
        pass

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            remember_me = request.args['remember'] # check to see if the user wants to stay logged in for 30 days
        except:
            remember_me = False

        request_path = request.args['next'] # Get the redirect path
        if request_path == 'None':
            request_path = ''

        """
        send login request

        if password is correct:
            session.clear()
            if (remember_me):
                session['username'] = username
            else:
                session.pop('username', None)

            access_token = create_access_token(identity=username, fresh=True)
            refresh_token = create_refresh_token(identity=username)

            return jsonify(access_token=access_token, refresh_token=refresh_token, redirect=request_path), 200
        else:
            return jsonify("Wrong password"), 400
        """

        """
        try:
            storedHash = db.users.find_one({'username': username}, {'hash': 1, "_id": 0})['hash']
        except TypeError:
            storedHash = None

        if not storedHash:
            # If there is no storedHash, there is no user by that name
            return jsonify("No user found"), 400

        if (bcrypt.checkpw(password.encode(), storedHash.encode())): # check the submitted password against the stored hash
            session.clear()
            if (remember_me):
                session['username'] = username
            else:
                session.pop('username', None)

            # Create access_ and refresh_ tokens for the authenticated user
            access_token = create_access_token(identity=username, fresh=True)
            refresh_token = create_refresh_token(identity=username)

            # response = redirect(request_path) if request_path else redirect(url_for('admin_root'))

            return jsonify(access_token=access_token, refresh_token=refresh_token, redirect=request_path), 200
        else:
            return jsonify("Wrong password"), 400
    """

    return render_template('login.j2')

@public.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('public.index'))
