from flask import jsonify, Blueprint
from models.Classes import Idol
from db import session
from sqlalchemy import func

idol_api = Blueprint('drama_api', __name__)

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