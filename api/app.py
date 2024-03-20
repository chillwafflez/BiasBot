from flask import Flask, Response
from flask_restful import Api

app = Flask(__name__)
# app.register_blueprint(drama_api)

@app.route("/", methods=['GET'])
def home():
    return Response("home index", 200)


if __name__ == '__main__':
    app.run(debug=True)