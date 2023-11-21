from flask import Blueprint, request, jsonify
import json
from controllers.verb_controller import get_verb, favorite_verb
from helpers.token_validation import validate_token
from helpers.error_message import *

verb = Blueprint("verb", __name__)

@verb.route("/v0/verbs/", methods=["GET"])
def getVerb():
    try:
        token = validate_token()

        if token == 400:
            return jsonify(CONST_MISSING_TOKEN_ERROR), 400
        if token == 401:
            return jsonify(CONST_INVALID_TOKEN_ERROR), 401
            
        data = json.loads(request.data)
        if 'verb' not in data:
            return jsonify(CONST_VERB_NEEDED_ERROR), 400

        response_data = get_verb(data).json

        return jsonify(response_data)
    except Exception:
        return jsonify({'error': 'Something happened when trying to get the verb.'}), 500

@verb.route("/v0/verbs/favorites/", methods=["POST"])
def favoriteVerb():
    try:
        token = validate_token()

        if token == 400:
            return jsonify(CONST_MISSING_TOKEN_ERROR), token
        if token == 401:
            return jsonify(CONST_INVALID_TOKEN_ERROR), token
            
        data = json.loads(request.data)

        if 'verb' not in data:
            return jsonify(CONST_VERB_NEEDED_ERROR), 400

        favorite_verb_result = favorite_verb(data, token)

        return favorite_verb_result

    except Exception as error:
        print(error)
        return jsonify({'error': 'Something happened when trying to favorite the verb.'}), 500
