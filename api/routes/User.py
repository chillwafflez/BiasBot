from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from models.Classes import User_Server, Idol_Server, Idol, User
from db import session

user_api = Blueprint('user_api', __name__)

@user_api.route("/users/<int:user_id>", methods=['GET'])
def check_user_exists(user_id):
    user_exists = session.query(User).filter_by(id=user_id).first() is not None
    if (user_exists):
        return jsonify({"user_id": user_id, "message": "User already in database"}), 200
    else:
        return jsonify({"user_id": user_id, "message": "User is not in database"}), 200
    
@user_api.route("/users", methods=['POST'])
def add_user():
    user_id = request.json['user_id']
    username = request.json['username']

    try:
        user_exists = session.query(User).filter_by(id=user_id).first() is not None
        if (user_exists):
            return jsonify({"user_id": user_id, "message": "User already in database", "created": True}), 200

        new_user = User(id=user_id, username=username)
        session.add(new_user)
        session.commit()

        created_user = session.query(User).filter_by(id=user_id).first()
        if created_user:
            return jsonify({"message": "User was successfully added into database!", "created": True}), 200
        else:
            return jsonify({"message": "Unable to add user into database", "created": False}), 400
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
@user_api.route("/users/rolls", methods=['GET'])
def check_rolls():
    user_id = request.args.get('userID')
    username = request.args.get('username')
    server_id = request.args.get('serverID')

    try:
        user_server = session.query(User_Server).filter_by(user_id=user_id, server_id=server_id).first()
        created = ""
        if (user_server):
            created = "user_account record already exists"
            if (user_server.rolls > 0):
                user_server.rolls -= 1
                session.commit()
                return jsonify({"has_rolls": True,"remaining": user_server.rolls})
            else:
                return jsonify({"has_rolls": False, "remaining": 0})
        else:
            print("User_Server dont exist (in query for user/rolls), creating them rn")
            new_user_server = User_Server(user_id=user_id, server_id=server_id, server_profile_name=username, collection_name=f"{username}'s collection!", rolls=8)
            session.add(new_user_server)
            session.commit()
            created = "user_account record just created!"
            return jsonify({"has_rolls": True,"remaining": new_user_server.rolls, 'created': created})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500


@user_api.route("/users/claimed", methods=['GET'])
def check_can_claim():
    user_id = request.args.get('userID')
    server_id = request.args.get('serverID')

    try:
        user_server = session.query(User_Server).filter_by(user_id=user_id, server_id=server_id).first()
        if (user_server.can_claim):
            return jsonify({"can_claim": True})
        else:
            return jsonify({"can_claim": False})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

@user_api.route("/users/claimed", methods=['POST'])
def add_claimed():
    user_id = request.json['user_id']
    username = request.json['username']
    server_id = request.json['server_id']
    idol_id = request.json['idol_id']
    print(f"Received user_id = {user_id} | idol_id = {idol_id} | server_id = {server_id}")

    try:
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

        # claim idol for this user_server
        user_server = session.query(User_Server).filter_by(user_id=user_id, server_id=server_id).first()
        new_claimed = Idol_Server(idol_id=idol_id, user_server_id=user_server.id, server_id=server_id, status="Claimed")
        session.add(new_claimed)
        session.commit()
        print(f"Added new claimed")

        # update user_server record to be unable to claim now
        user_server.can_claim = False
        # session.query(User_Server).filter(user_id=user_id, server_id=server_id).update({User_Server.can_claim: False})
        session.commit()

        return jsonify({'user_id': user_id,
                        'idol_id': idol_id,
                        'server_id': server_id,
                        'created': created}), 200
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

@user_api.route("/users/collection", methods=['GET'])       # exp url: http://127.0.0.1:5000/users/collection?userID=2&serverID=70
def get_collection():
    user_id = request.args.get('userID')
    server_id = request.args.get('serverID')

    try:
        user_server_id = session.query(User_Server).filter_by(user_id=user_id, server_id=server_id).first().id      # current user_server id
        idol_records = session.query(Idol_Server.idol_id).filter_by(user_server_id=user_server_id).all()            # get all idol_server records with user_server id (claimed)
        idol_ids = [record[0] for record in idol_records]

        collection = []
        for id in idol_ids:
            idol_data = {}
            idol_record = session.query(Idol).filter_by(id=id).first()
            idol_data["id"] = idol_record.id
            idol_data["stage_name"] = idol_record.stage_name
            idol_data["group"] = idol_record.idol_group

            collection.append(idol_data)

        return jsonify(collection)
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
@user_api.route("/users/rolls/reset", methods=['POST'])
def reset_rolls():
    try:
        session.query(User_Server).update({User_Server.rolls: 8})
        session.commit()
        return jsonify({"resetted_rolls": True})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"resetted_rolls": True, "error": str(e)}), 500

@user_api.route("/users/claims/reset", methods=['POST'])
def reset_claims():
    try:
        session.query(User_Server).update({User_Server.can_claim: True})
        session.commit()
        return jsonify({"resetted_claims": True})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"resetted_claims": True, "error": str(e)}), 500