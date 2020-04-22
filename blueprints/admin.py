from flask import Blueprint, render_template, request, url_for, session, redirect, jsonify
from functools import wraps

admin = Blueprint('admin', __name__, template_folder='../templates/admin', url_prefix='/admin', static_folder='../static/build')

@admin.route('/')
def admin_root():
    return render_template('admin.j2')
