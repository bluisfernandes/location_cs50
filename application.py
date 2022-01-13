# from cs50 import SQL
import os
from flask import Flask, request, jsonify, render_template, make_response
import json
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import geojson_rdm_multipoints

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///finance.db")


# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")

n = 1000

@app.route("/")
def index():
  	return '''
		Its working!<br><br>

		<a href="/location">/location<a><br>
		<a href="/postjson">/postjson<a><br>
		<a href="/map">/map<a><br>
		<a href="/maptest?n=10000">/maptest?n=10000<a><br>
		'''

@app.route("/map", methods=['GET'])
def map():
	global n
	n = int(request.args.get('n'))
	geojson = geojson_rdm_multipoints(n)
	return render_template("map.html", site_map=True, geojson = geojson)


@app.route("/maptest", methods=['GET'])
def map_test():
	global n
	n = int(request.args.get('n'))
	geojson = geojson_rdm_multipoints(n)
	return render_template("map_test.html", site_map=True, geojson = geojson)

@app.route("/maptest1")
def map_test1():

	geojson = geojson_rdm_multipoints(10)

	return render_template("blank.html", title = f"erro: TESTE", content = geojson)

@app.route("/script.js")
def script():
	geojson = geojson_rdm_multipoints(n)
	return render_template("script.js", geojson = geojson)


@app.route('/location', methods=['POST', 'GET'])
def location():
	if request.method == "POST":
		a = request.form.get("username")

		try:
			b = json.loads(a)
			if isinstance(b, dict):
				res = make_response(jsonify(b), 200)
			else:
				res = make_response(jsonify({"message": "must be JSON, its probably numeric"}), 405)

		except:
			return make_response(jsonify({"message": "must be JSON, its probably a string"}), 405)

		return res

	return render_template("location.html")


# Used to communicate with Android APP or colab
@app.route('/postjson', methods=['POST', 'GET'])
def postjson():
	if request.method == "POST":
		a = request.get_json()

		if isinstance(a, dict):
			code, message = store_route(a)
			res = make_response(jsonify(message), code)
			print(f"__response {code}")

		else:
			formato = f"must be JSON, its a {type(a)}"
			res = make_response(jsonify({"message": formato}), 405)
			print(f"__Response error: {formato}")

		# print(type(res.get_json()))

		return res

	return '''Try to post a JSON<br>
					Example in <a href=https://colab.research.google.com/drive/1H-cBSzQcHqKl-CObhL1_tl76_76lynNX?usp=sharing>Colab<a>.'''


def store_route(json_request):

	# check if there are all keys
	try:
		print("_______________________________")
		print(json_request["id"])
		print("______________")
		print(json_request["device"])
		print("______________")
		print(json_request["points"][0])
		print("______________")
		print(json_request["info"][0])
	except:

		# return code of error and expected json
		return 403, {"message":"some parameters are missing","expected":{"id": 10, "device": "xxx", "points":[{"lat": 123.456, "long": 987.654 },{"lat": 123.457, "long": 987.655 }],"info":[{"point_id":0,"route_id":0,"sensor_light":13333.3,"timestamp":"2022-01-11T00:59:53.372"},{"point_id":1,"route_id":0,"sensor_light":13345.9,"timestamp":"2022-01-11T00:59:54.926"}]}}


	path = f'/home/runner/locationcs50/storage/{json_request["device"]}'

	if not os.path.exists(path):
			os.makedirs(path)

	name = json_request['info'][0]['timestamp']+"_"+str(len(json_request["points"]))

	with open(f'{path}/{name}.txt', 'w') as file:
			file.write(str(json_request))


	# store_id = 0
	# json_request["device"]
	# json_request["id"]
	# json_request["info"][0]["timestamp"]

	# json_request["points"]
	# json_request["info"]

# TODO: store values on sqlite
# user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
# db.execute("INSERT INTO wallet(user_id, symbol, shares, user_id_symbol) VALUES (?, ?, ?, ?)",
                      #  session['user_id'], stock['symbol'], shares, user_id_symbol)
# db.execute("UPDATE wallet SET shares = ? WHERE user_id_symbol = ? ", shares, user_id_symbol)

	return 200, json_request


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

def apology(msg, code=400):
	msg_site = "ERROR! name: " +msg + " code: " + str(code)
	return render_template("blank.html", title = f"erro: {code}", content = msg_site)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


app.run(host='0.0.0.0', port=5000, debug=False) # Run the Application (in debug mode)