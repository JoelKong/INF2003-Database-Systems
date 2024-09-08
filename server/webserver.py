# make sure install all these bs then add to requirements.txt file
from flask import Flask, request, jsonify
from flask_cors import CORS


# Set up CORS for flask and react
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])


# POST route to compute algorithm
@app.route('/api/v1/whateverpathyouwant', methods=['GET'])
def get_adopted_pets():
    # Get front end data
    data = request.get_json() # if need any data from the front end just an example
    start = data.get('start')
    hotels = data.get('selectedHotels')
    efficiencyType = data.get('efficiencyType')
    departureTime = data.get('departureTime')
    algorithmType = data.get('algorithm')


    # return bck to front end use jsonify
    # if not forward_route or not return_route:
    #     return jsonify({"error": "No route found"}), 500

    # # Return to front end
    # response = {
    #     "geojson_forward_route": geojson_forward_route,
    #     "geojson_return_route": geojson_return_route,
    #     "start": start,
    #     "hotels": hotels,
    #     "dashboardData": {"runtimeTaken": round(runtime, 5), "timeTaken": time_taken_hr_min, "totalCost": round(total_cost, 2), "ERPPassed": erp_passed, "forwardRouteRoads": forward_route_roads, "returnRouteRoads": return_route_roads},
    # }
    # return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)