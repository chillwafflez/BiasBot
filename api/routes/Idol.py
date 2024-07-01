from flask import jsonify, Blueprint, request
from models.Classes import Idol, Idol_Server, User_Server, User
from db import session
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

idol_api = Blueprint('drama_api', __name__)

@idol_api.route("/idols/info", methods=['GET'])
def search_idol():
    post_body = request.args.get('query')
    cleaned_search_term = post_body.strip().lower()

    def process_results(results):
        idols = []
        for idol in results:
            idol_data = {}
            idol_data["id"] = idol.id
            idol_data["stage_name"] = idol.stage_name
            idol_data["full_name"] = idol.full_name
            idol_data['korean_name'] = idol.korean_name
            idol_data["group"] = idol.idol_group
            idol_data['country'] = idol.country
            idol_data['gender'] = idol.gender

            idols.append(idol_data)
        return jsonify({'results': idols, 'found': True})

    try:
        print("Searching by stage name...")
        stage_name_results = session.query(Idol).filter(func.lower(Idol.stage_name) == cleaned_search_term).all()
        print(f"length of stage results: {len(stage_name_results)}")

        if len(stage_name_results) > 0:
            results = process_results(stage_name_results)
            return results
        
        print("Searching by full name...")
        full_name_results = session.query(Idol).filter(func.lower(Idol.full_name) == cleaned_search_term).all()
        print(f"length of full name results: {len(full_name_results)}")
        if len(full_name_results) > 0:
            results = process_results(full_name_results)
            return results
        
        return jsonify({"found": False}), 404

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

@idol_api.route("/idols/<int:id>", methods=['GET'])
def get_idol(id):
    idol = session.query(Idol).filter_by(id=id).first()
    image_url = idol.image_urls[0].url

    return jsonify({
        'id': idol.id,
        'stage_name': idol.stage_name,
        'full_name': idol.full_name,
        'korean_name': idol.korean_name,
        'group': idol.idol_group,
        'country': idol.country,
        'gender': idol.gender,
        'picture_url': image_url})

@idol_api.route("/idols/random-idol/<string:gender>", methods=['GET'])
def get_random_idol(gender):
    try:
        if gender == 'female':
            idol = session.query(Idol).filter(Idol.gender == "Female").order_by(func.random()).first()
        elif gender == 'male':
            idol = session.query(Idol).filter(Idol.gender == "Male").order_by(func.random()).first()
        else:
            idol = session.query(Idol).order_by(func.random()).first()
        image_url = idol.image_urls[0].url

        return jsonify({
            'id': idol.id,
            'stage_name': idol.stage_name,
            'full_name': idol.full_name,
            'korean_name': idol.korean_name,
            'group': idol.idol_group,
            'country': idol.country,
            'gender': idol.gender,
            'picture_url': image_url})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

@idol_api.route("/idols/", methods=['GET'])     # exp url: http://127.0.0.1:5000/idols/?idolID=11&serverID=70
def get_status():
    idol_id = request.args.get('idolID')
    server_id = request.args.get('serverID')

    try:
        idol_server_record = session.query(Idol_Server).filter_by(idol_id=idol_id, server_id=server_id).first()
        if (idol_server_record):  
            user = session.query(User).join(User_Server).filter(User_Server.id == idol_server_record.user_server_id).first()
            print(f"This idol has been claimed in this server by {user.username}")

            response = {
                "claimed": True, 
                "user_id": user.id,
                "username": user.username
            }
            return jsonify(response), 200
        else:
            print("Idol has not been claimed yet in this server")
            return jsonify({"claimed": False}), 200
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
@idol_api.route("/idols/female-idols", methods=['GET'])
def all_female_idols():
    results = session.query(Idol).filter(Idol.gender == "Female").all()
    all_female = convert_idols_to_dict(results)

    return jsonify(all_female)

@idol_api.route("/idols/male-idols", methods=['GET'])
def all_male_idols():
    results = session.query(Idol).filter(Idol.gender == "Male").all()
    all_males = convert_idols_to_dict(results)

    return jsonify(all_males)

@idol_api.route("/idols/groups/<string:group>", methods=['GET'])
def get_group(group):
    results = session.query(Idol).filter(Idol.idol_group == group).all()
    idols = convert_idols_to_dict(results)

    return jsonify(idols)


# utils
def convert_idols_to_dict(results):
    idols = []
    for idol in results:
        idol_dict = {}
        idol_dict['id'] = idol.id
        idol_dict['stage_name'] = idol.stage_name
        idol_dict['full_name'] = idol.full_name
        idol_dict['korean_name'] = idol.korean_name
        idol_dict['group'] = idol.idol_group
        idol_dict['country'] = idol.country
        idol_dict['gender'] = idol.gender
        idols.append(idol_dict)
    return idols