from flask import Flask, request,render_template, jsonify
from arango import ArangoClient
app = Flask(__name__)

# Replace with your ArangoDB connection details
client = ArangoClient(hosts=["https://YourArangoAppIp:Port"])

# Login with username and password (replace with your credentials)
db = client.db("databasename",username="user", password="password")


@app.route('/', methods = ['GET'])
def index():
        return render_template('graph.html')
# Define the AQL query


@app.route('/Search', methods = ['GET'])
def Search():
    place1 = "places/" + request.args.get('place1')
    place2 = "places/" + request.args.get('place2')

    query = """
            FOR vertex, edge
            IN OUTBOUND SHORTEST_PATH @place1 TO @place2
            GRAPH 'myGraph'
            OPTIONS {weightAttribute: 'travelTime'}
                return {vertex, edge}
            """
    bind_vars = {
        'place1': place1,
        'place2': place2
    }
    
    # Execute the query on the database
    cursor = db.aql.execute(query, bind_vars=bind_vars)
    data = [document for document in cursor]
    return jsonify(data)
    # # Get the shortest path as a list of vertex keys
    # for document in cursor:
    #     vertex = document['vertex']
    #     edge = document['edge']


if __name__ == "__main__":
    app.run(debug=True)