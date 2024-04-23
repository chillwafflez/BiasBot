from routes.db import select_query, select_all_query
from flask import Flask, jsonify, Blueprint, request
from flask_restful import Api, Resource

idol_api = Blueprint('drama_api', __name__)
api = Api(idol_api)

# fetch idol by id
@idol_api.route("/idols/<int:idol_id>", methods=['GET'])
def get_idol_by_id(idol_id):

    sql = f"SELECT * FROM idol WHERE id = {idol_id};"
    results = select_all_query(sql)

    if results:
        return jsonify(results)
    else:
        return "bruh"

# get idol by stage name
@idol_api.route("/idols/<string:stage_name>", methods=['GET'])
def get_idol_by_stage_name(stage_name):

    sql = f"SELECT * FROM idol WHERE stage_name = {stage_name};"
    results = select_all_query(sql)

    if results:
        return jsonify(results)
    else:
        return "bruh"

# get idols of a group
@idol_api.route("/idols/<string:group_name>", methods=['GET'])
def get_group(group_name):

    sql = f"SELECT * FROM idol WHERE group = {group_name};"
    results = select_all_query(sql)

    if results:
        return jsonify(results)
    else:
        return "bruh"

# get all claimed idols
@idol_api.route("/idols/claimed", methods=['GET'])
def get_claimed(group_name):

    sql = f"SELECT * FROM idol WHERE group = {group_name};"
    results = select_all_query(sql)

    if results:
        return jsonify(results)
    else:
        return "bruh"

# get all claimed male idols
@idol_api.route("/idols/claimed/male", methods=['GET'])
def get_claimed_males(group_name):

    sql = f"SELECT * FROM idol WHERE group = {group_name};"
    results = select_all_query(sql)

    if results:
        return jsonify(results)
    else:
        return "bruh"

# get all claimed female idols
@idol_api.route("/idols/claimed/female", methods=['GET'])
def get_claimed_females(group_name):

    sql = f"SELECT * FROM idol WHERE group = {group_name};"
    results = select_all_query(sql)

    if results:
        return jsonify(results)
    else:
        return "bruh"