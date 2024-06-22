from flask import request, jsonify, Blueprint
from models.Classes import User_Server, Idol_Server, Idol
from db import session

user_api = Blueprint('user_api', __name__)

@user_api.route("/users/claimed", methods=['POST'])
def add_claimed():
    user_id = request.json['user_id']
    username = request.json['username']
    server_id = request.json['server_id']
    idol_id = request.json['idol_id']
    print(f"Received user_id = {user_id} | idol_id = {idol_id} | server_id = {server_id}")

    exists = session.query(User_Server).filter_by(user_id=user_id, server_id=server_id).first() is not None
    created = ""
    if (exists):
        print(f"user_account exists!: {exists}")
        created = "user_account record already exists"
    else:
        new_user_server = User_Server(user_id=user_id, server_id=server_id, server_profile_name=username, collection_name=f"{username}'s collection!")
        session.add(new_user_server)
        session.commit()
        created = "user_account record just created!"

    user_server_id = session.query(User_Server).filter_by(user_id=user_id, server_id=server_id).first().id
    new_claimed = Idol_Server(idol_id=idol_id, user_server_id=user_server_id, server_id=server_id, status="Claimed")
    session.add(new_claimed)
    session.commit()
    print(f"Added new claimed")

    return jsonify({'user_id': user_id,
                    'idol_id': idol_id,
                    'server_id': server_id,
                    'created': created})

@user_api.route("/users/collection", methods=['GET'])
def get_collection():
    user_id = request.args.get('userID')
    server_id = request.args.get('serverID')

    user_server_id = session.query(User_Server).filter_by(user_id=user_id, server_id=server_id).first().id      # current user_server id
    print(f"bruh = {user_server_id}")                           
    idol_records = session.query(Idol_Server.idol_id).filter_by(user_server_id=user_server_id).all()            # get all idol_server records with user_server id (claimed)
    idol_ids = [record[0] for record in idol_records]

    collection = []
    for id in idol_ids:
        idol_data = {}
        idol_record = session.query(Idol).filter_by(id=id).first()
        idol_data["stage_name"] = idol_record.stage_name
        idol_data["group"] = idol_record.idol_group

        collection.append(idol_data)

    return jsonify(collection)