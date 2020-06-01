from flask import Blueprint, render_template, request, url_for, session, redirect, jsonify, abort, current_app
from functools import wraps
from flask_jwt_extended import fresh_jwt_required, jwt_required, create_access_token, get_jwt_identity, jwt_refresh_token_required, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from werkzeug.security import check_password_hash, generate_password_hash, safe_str_cmp
import bcrypt
import json
from modules.db import User, Tool, db, Training
from modules.forms import LoginForm, NewTrainingForm
from authlib.integrations.flask_client import OAuth
from flask_login import current_user, login_user, logout_user
# from adal import AuthenticationContext

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

public = Blueprint('public', __name__, template_folder='../templates/public', static_folder='../static/build/')

@public.route('/')
def index():
    return redirect(url_for('public.tools'))

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
    user = User.query.filter_by(username='folin').first()
    trainings = Training.query.filter_by(trainee=user).all()
    return render_template('trainings.j2', trainings=trainings)

@public.route('/trainings/new/', methods=['GET', 'POST'])
def new_training():
    form = NewTrainingForm()
    form.tool.choices = [(tool.shortname, tool.name) for tool in Tool.query.all()]

    if request.method == 'POST':
        _tool = Tool.query.filter_by(shortname=form.tool.data).first()

        # TODO: Add user
        _user = User.query.filter_by(username="folin").first()
        training = Training(tool=_tool, trainee=_user, started=db.func.current_timestamp())
        db.session.add(training)
        db.session.flush()
        db.session.commit()

        training_id = training.id
        return redirect(url_for('public.training', training_id=training_id))


    return render_template('training_new.j2', form=form)

@public.route('/trainings/<training_id>')
def training(training_id):
    training = Training.query.filter_by(id=training_id).first_or_404()
    return render_template('training.j2', training=training)

@public.route('/api/token-refresh/', methods=['POST']) # refresh the token
@jwt_refresh_token_required # refresh token is needed to do this
def refresh():
    new_token = create_access_token(identity=get_jwt_identity(), fresh=True)
    response = jsonify({'access_token': new_token})
    return response

@public.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.tools'))

    form = LoginForm();

    if form.validate_on_submit():
        # Do oauth login stuff here
        if not login_successful:
            flash("Invalid username or password") # TODO: Need to do something with this flash
            return redirect(url_for('public.login')), 401

        user = User.query.filter_by(username=form.username.data).first()

        if user is None:
            # Do OAuth login stuff here
            pass
        else:
            # Do OAuth login stuff here
            pass

        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('public.index'))

    return render_template('login.j2')

@public.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.tools'))
