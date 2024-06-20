from flask import Flask, Response
from routes.Idol import idol_api

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return Response("bias bot home", 200)

app.register_blueprint(idol_api)

if __name__ == '__main__':
    app.run(debug=True)