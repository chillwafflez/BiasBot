from routes.db import select_query, select_all_query
from flask import Flask, jsonify, Blueprint, request
from flask_restful import Api, Resource

user_api = Blueprint('drama_api', __name__)
api = Api(user_api)

# get collection of user
@user_api.route("/user_server/collection/", methods=['GET'])
def get_collection(idol_id, user_server_id, server_id):

    sql = f"SELECT * FROM idol AND status FROM idol_server JOIN something something between "
    results = select_all_query(sql)

    if results:
        return jsonify(results)
    else:
        return "bruh"

# get collection name of user
@user_api.route("/user_server/collection_name", methods=['GET'])
def get_collection_name(user_id, server_id):

    sql = f"SELECT collection_name FROM user_server WHERE user_id = {user_id} AND server_id = {server_id}"
    results = select_all_query(sql)

    if results:
        return jsonify(results)
    else:
        return "bruh"
    
# get female idols of collection of user


# get male idols of collection of user
