from flask import Flask, Response, request
import jsonpickle

app = Flask(__name__)

@app.route('/', methods=["POST"])
def home():
    name = request.form["name"]
    info = request.form["info"]

    response = {
        'name' : name,
        'info' : info,
        'success' : "yes"
    }

    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


app.run(host="127.0.0.1", port=5000)