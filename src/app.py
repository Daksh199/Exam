from flask import Flask, request, Response, jsonify
from data_model import WeatherDataModel, WeatherStatsDataModel
from flasgger import Swagger, swag_from

app = Flask(__name__)

swagger = Swagger(app)

@app.route("/")
def home():
    return "Weather App"


def pagination(data, start, limit):
    if len(data) > start:
        return data[start:start + limit]
    else:
        return data


@app.route("/api/weather", methods=['GET'])
def weather():
 
    args = request.args
    date = args.get('date')
    stationid = args.get('stationid')
    start = args.get('start', 0)
    limit = args.get('limit', 20)
    if stationid is None or date is None:
        return jsonify(status='Failure',results='Missing date or stationid parameter')

    weather_dm = WeatherDataModel()
    response = weather_dm.get_data(query=[stationid, date]).to_dict(orient='records')
    return jsonify(status='ok', results=pagination(response, start, limit),start=start,limit=limit)


@app.route("/api/weather/stats", methods=['GET'])
def stats():
   
    args = request.args
    stationid = args.get('stationid')
    start = args.get('start', 0)
    limit = args.get('limit', 20)
    if stationid is None:
        return jsonify(status='Failure',results='Missing year or stationid parameter')

    weatherstats_dm = WeatherStatsDataModel()
    response = weatherstats_dm.get_data(query=[stationid]).to_dict(orient='records')

    return jsonify(status='ok', results=pagination(response, start, limit),start=start,limit=limit)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
