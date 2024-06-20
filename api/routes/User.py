from flask import request, jsonify, Blueprint
from models.User import User
from db import session
from sqlalchemy import insert, func

user_api = Blueprint('user_api', __name__)

@user_api.route("/users/claimed", methods=['POST'])
def add_claimed():
    id = request.json['id']
    stage_name = request.json['stage_name']
    print(f"Received id = {id} | stage name = {stage_name}")
    return jsonify({'id': id,
                   'stage_name': stage_name})