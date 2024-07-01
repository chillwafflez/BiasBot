from flask import jsonify, Blueprint, request
from models.Classes import Server
from db import session

server_api = Blueprint('server_api', __name__)

@server_api.route("/servers", methods=['POST'])
def add_server():
    server_id = request.json['server_id']
    server_name = request.json['name']

    try:
        new_server = Server(id=server_id, name=server_name)
        session.add(new_server)
        session.commit()

        response = {
            "status": "Server successfully added to database", 
            "server_id": server_id,
            "server_name": server_name
        }
        return jsonify(response), 201
    except Exception as e:
        response = {
            "status": "Error adding server to database", 
            "exception": e
        }  
        return jsonify(response), 400
    
    
@server_api.route("/servers/<int:server_id>", methods=['DELETE'])
def delete_server(server_id):
    selected_server = session.query(Server).filter_by(id=server_id).first()

    if selected_server:
        session.delete(selected_server)
        session.commit()
        response = {
            "status": "Server successfully deleted from database", 
            "server_id": server_id
        }
        return jsonify(response), 200
    else:
        response = {
            "status": "Server doesn't exist in database", 
            "server_id": server_id
        }
        return jsonify(response), 404