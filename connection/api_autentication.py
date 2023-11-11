# import os
#
# from flask import request, jsonify
#
#
# def verify_api_key():
#     return request.headers.get('API-Key') == os.environ['API_KEY']
#
#
# def api_key_recommend(func):
#     def wrapper_recommend(*args, **kwargs):
#         return func(*args, **kwargs) if verify_api_key() else jsonify(data="Wrong API key."), 401
#
#     return wrapper_recommend
#
#
# def api_key_process(func):
#     def wrapper_process(*args, **kwargs):
#         return func(*args, **kwargs) if verify_api_key() else jsonify(data="Wrong API key."), 401
#
#     return wrapper_process
