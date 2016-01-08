import msql
import json
from flask import Flask, url_for, request,render_template, jsonify

app = Flask(__name__)

#GLOBAL PARAMS
HOST = "localhost"
USER = "root"
PASS = "root"
DBNAME = "lab12"
MS = msql.MySQLreq([HOST,USER,PASS,DBNAME])

@app.route("/")
def index():
	return render_template("index.html")
@app.route("/answer")
def answer():
	return render_template("answer.html")

@app.route("/error_reg")
def error_reg():
	return render_template("error_reg.html")		

@app.route("/registration")	
def registration():
	return render_template("registration.html")

@app.route("/reg_worker", methods=['POST'])
def reg_worker():
	data = request.data
	jdata = json.loads(data)
	#print("------------------------>",jdata['name'])
	#Query = "INSERT INTO `clients` (`name`,`pass`,`country`,`city`) VALUES(\'"+ request.form['login'] +"\',\'" + request.form['pass'] +  "\',\'" + request.form['country'] +	"\',\'" + request.form['city'] + "\');"
	Query = "INSERT INTO `clients` (`name`,`pass`,`country`,`city`) VALUES(\'"+ jdata['name'] +"\',\'" + jdata['pass'] +  "\',\'" + jdata['country'] +	"\',\'" + jdata['city'] + "\');"
	
	#print(Query)
	MS.setData(Query)
	return "OK"


#RESTfull 
@app.route("/login_validation/<login>")
def login_validation(login):
	print("working")
	Query = "SELECT * FROM clients WHERE name =\'" + login + "\';"

	if len(MS.getData(Query)) == 0:
		print("empty")
		return jsonify({'answer': 0})
	print("full")	
	return jsonify({'answer': 1})
@app.route("/country_tip/<country_name>")
def country_tip(country_name):
	Query = "SELECT * FROM CountryTable WHERE country LIKE \'"+ country_name +"%\'"
	country_list = MS.getData(Query)
	new_list = []
	for i in country_list:
		new_list.append(i[1])
	print(new_list)	

	return jsonify({'c':new_list})	

@app.route("/city_tip/<city_name>")
def city_tip(city_name):
	Query = "SELECT * FROM CityTable WHERE city_name LIKE \'"+ city_name +"%\'"
	city_list = MS.getData(Query)
	new_list = []
	for i in city_list:
		new_list.append(i[1])
	print(new_list)	

	return jsonify({'c':new_list})



#END RESTfull	

@app.route("/worker", methods=['POST'])
def worker():
	categ = []
	#print("START...")
	mainfield,calendar,price,comment = (False,False,False,False)   # according to clients request 
	if len(request.form['ffield']) != 0:						   # func makes a request to MySQL database 
		mainfield = True
		
	if request.form['calendar']:
		calendar = True
		
	if len(request.form['price_min']) != 0 and len(request.form['price_max']) != 0:
		price = True
		
	if request.form.getlist('category[]'):
		categ = True
	
	if len(request.form['comment']) != 0:
		comment = True
	
	#print("Comment: ",request.form['comment'])	
	reqstr = requestMaker(mainfield,calendar,price,comment,categ) # str - string with db request	
	result_list = MS.getData(reqstr)
	if len(result_list) == 0:
		return render_template("error.html")

		
	
	return render_template("res.html", fieldres = result_list)



def requestMaker(f=False,cal=False,pr=False,comment=False,categ=False): # create request for db;   1) f - main field
	req = "SELECT * FROM stuff_info WHERE"								#						   2) cal - date
	if f:																#						   3) pr - price
		req += " LOCATE('" + request.form['ffield'] + "',name) AND"		#						   4) categ - category
	if cal:
		req += " date = '" + request.form['calendar'] + "' AND"			#						   5) comment - description
	if pr:
		req += " (price <= " + request.form['price_max'] + " AND price >= " + request.form['price_min'] + ") AND"
	if categ:
		for i in request.form.getlist('category[]'):
			req += " category = '" + i + "' OR"
	if comment:
		req += " (LOCATE('" + request.form['comment'] + "',shortinf) OR LOCATE('" + request.form['comment'] + "',fullinf)) AND"
	return req[:-3] 





if __name__ == "__main__":
	app.run(debug=True)


