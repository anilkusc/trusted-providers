import getData
import json
import trustedProviders
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    trustFactor=request.args['factor']
    startDate=request.args['start']
    endDate=request.args['end']
    predictionObject=request.args['pp']
    predictionObjectID=request.args['ppid']
    providers=request.args.getlist("provider")
    accuracyRates=trustedProviders.calculate(trustFactor,startDate,endDate,predictionObjectID,predictionObject,*providers)
    json={}
    i=0
    for accuracyRate in accuracyRates:
        json[providers[i]] = accuracyRate
        i=i+1

    return jsonify(json)
app.run()
