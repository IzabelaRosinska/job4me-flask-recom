import os

from flask import request, jsonify


def verify_api_key():
    if provided_api_key := request.headers.get('API-Key'):
        if provided_api_key == os.environ['API_KEY']:
            return None
        return jsonify(data="Wrong API key."), 401
    return jsonify(data="API key not provided."), 401


def api_key_recommend(func):
    def wrapper_recommend(*args, **kwargs):
        return error if (error := verify_api_key()) else func(*args, **kwargs)

    return wrapper_recommend


def api_key_update_offer(func):
    def wrapper_update_offer(*args, **kwargs):
        return error if (error := verify_api_key()) else func(*args, **kwargs)

    return wrapper_update_offer


def api_key_update_employee(func):
    def wrapper_update_employee(*args, **kwargs):
        return error if (error := verify_api_key()) else func(*args, **kwargs)

    return wrapper_update_employee


def api_key_update_offers_embeddings(func):
    def wrapper_update_offers_embeddings(*args, **kwargs):
        return error if (error := verify_api_key()) else func(*args, **kwargs)

    return wrapper_update_offers_embeddings


def api_key_update_employees_embeddings(func):
    def wrapper_update_employees_embeddings(*args, **kwargs):
        return error if (error := verify_api_key()) else func(*args, **kwargs)

    return wrapper_update_employees_embeddings


def api_key_remove_offer(func):
    def wrapper_remove_offer(*args, **kwargs):
        return error if (error := verify_api_key()) else func(*args, **kwargs)

    return wrapper_remove_offer


def api_key_remove_employee(func):
    def wrapper_remove_employee(*args, **kwargs):
        return error if (error := verify_api_key()) else func(*args, **kwargs)

    return wrapper_remove_employee
