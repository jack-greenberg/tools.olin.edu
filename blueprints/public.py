from flask import Blueprint, render_template, request, url_for, session, redirect, jsonify
from functools import wraps

public = Blueprint('public', __name__, template_folder='../templates/public', static_folder='../static/public', static_url_path='/static/public')

@public.route('/')
def public_index():
	return "Hello, world!"
