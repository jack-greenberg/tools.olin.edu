#  from flask import Blueprint
#  from functools import wraps

from .api import API
from .public import public

blueprints = [API, public]

# class Router(Blueprint):
#     def __init__(self):
#         pass
#
#     def route(self, url, **kwargs):
#         route_fn = super().route
#         @wraps(route_fn)
#         def _route(url, **kwargs):
#             try:
#                 return route_fn(url, **kwargs)
#             except Exception as e:
#                 return
#
#         return _route
#
# def route(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#
