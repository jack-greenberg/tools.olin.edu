from flask import Blueprint, render_template, request, url_for, session, redirect, jsonify
from functools import wraps

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

public = Blueprint('public', __name__, template_folder='../templates/public', static_folder='../static/public', static_url_path='/static/public')

@public.route('/')
def public_index():
	return render_template('index.j2')

@public.route('/login')
def public_login():
	return render_template('login.j2')

@public.route('/users')
def users():
    return render_template('users.j2')

@public.route('/users/<user>')
# @login_required
def single_user(user):
    return render_template('user.j2', user=user)

@public.route('/tools')
def tools():
    return render_template('tools.j2')

@public.route('/tools/<tool>')
def single_tool(tool):
    return render_template('tool.j2', tool=tool)
