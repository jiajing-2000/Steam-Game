from flask import Flask, jsonify, render_template
import networkx as nx
import pickle
from networkx.readwrite import json_graph

app = Flask(__name__)


def load_graph(path):
    with open(path, "rb") as f:
        G = pickle.load(f)
    return G


def process_graph(G):
    # only keep the node with type = game, developer, genre, platform
    data = json_graph.node_link_data(G)
    return jsonify(data)


G = load_graph("data/graph.pickle")
G_small = load_graph("data/graph_small.pickle")


@app.route("/")
def index():
    # This route will serve your index.html file
    return render_template("index.html")


@app.route("/graph_small")
def get_graph_data_small():
    return process_graph(G_small)


# API endpoint to get graph data (adjust as needed for your data structure)
@app.route("/graph")
def get_graph_data():
    return process_graph(G)


@app.route("/graph/genre")
def get_all_genre():
    genre_nodes = [node for node in G.nodes if G.nodes[node]["type"] == "genre"]
    return jsonify(genre_nodes)


@app.route("/graph/<node_id>/genre")
def get_genre_data(node_id):
    node_id = int(node_id)
    try:
        # Check if the specified node_id exists in the graph
        if G.has_node(node_id):
            # Get all genre nodes connected to the specified game node
            genre_nodes = [
                node for node in G.neighbors(node_id) if G.nodes[node]["type"] == "genre"
            ]

            # Return the genre names as JSON
            return jsonify({"genres": genre_nodes})
        else:
            return jsonify({"error": "Node not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/graph/<node_id>/similar-genres")
def get_similar_genres(node_id):
    node_id = int(node_id)

    similar_games = set()
    for node in G.neighbors(node_id):
        if G.nodes[node]["type"] in ["developer", "genre", "platform"]:
            similar_games.update(G.neighbors(node))

    # Count genres of similar games
    genre_count = {}
    for game_id in similar_games:
        if G.nodes[game_id]["type"] == "game":
            for node in G.neighbors(game_id):
                if G.nodes[node]["type"] == "genre":
                    genre_count[node] = genre_count.get(node, 0) + 1
    return jsonify(genre_count)


@app.route("/graph/<node_id>/developer-connections")
def show_developer_connections(node_id):
    node_id = int(node_id)
    developer_node = None
    for node in G.neighbors(node_id):
        if G.nodes[node]["type"] == "developer":
            developer_node = node
            break

    if developer_node is None:
        return jsonify({"error": "Developer not found for the given game"}), 404

    # Create a subgraph for the developer and all connected games
    connected_games = [n for n in G.neighbors(developer_node) if G.nodes[n]["type"] == "game"]
    subgraph_nodes = [developer_node] + connected_games
    subgraph = G.subgraph(subgraph_nodes)
    data = json_graph.node_link_data(subgraph)
    return jsonify(data)


@app.route("/graph/<node_id>/platform-availability")
def get_platform_availability(node_id):
    # Show a bar chart displaying the availability of similar games across different platforms

    # Check if the node exists
    if node_id not in G:
        return jsonify({"error": "Node not found"}), 404


@app.route("/graph/<genre>/popular_games")
def get_popular_games(genre):
    print(genre)
    if genre not in G:
        return jsonify({"error": "Genre not found"}), 404

    # Get all games of the specified genre
    games = [n for n in G.neighbors(genre) if G.nodes[n]["type"] == "game"]

    # Get the top 10 most popular games
    games = sorted(games, key=lambda n: G.nodes[n]["num_reviews"], reverse=True)[:10]

    # return jsonify({"games": games})
    return jsonify([G.nodes[game] for game in games])


@app.route("/graph/<genre>/time_evolution")
def get_evolution(genre):
    if genre not in G:
        return jsonify({"error": "Genre not found"}), 404

    # Find all games of the given genre
    genre_games = []
    for node in G.nodes:
        if G.nodes[node]["type"] == "game":
            for neighbor in G.neighbors(node):
                if G.nodes[neighbor]["type"] == "genre" and genre.lower() in neighbor.lower():
                    genre_games.append(node)

    year_count = {}
    for game_id in genre_games:
        year = G.nodes[game_id]["release_date"].split("-")[0]
        year_count[year] = year_count.get(year, 0) + 1

    year_count = dict(sorted(year_count.items(), key=lambda item: item[0]))
    return jsonify(year_count)


@app.route("/graph/<developer>/game_portfolio")
def show_game_portfolio(developer):
    # Find all games of the given developer
    developer_games = []
    for node in G.nodes:
        if G.nodes[node]["type"] == "game":
            for neighbor in G.neighbors(node):
                if (
                    G.nodes[neighbor]["type"] == "developer"
                    and developer.lower() in neighbor.lower()
                ):
                    developer_games.append(G.nodes[node])

    return jsonify(developer_games)


@app.route("/graph/<developer>/genre_expertise")
def show_genre_expertise(developer):
    # Find all games of the given developer
    developer_games = []
    for node in G.nodes:
        if G.nodes[node]["type"] == "game":
            for neighbor in G.neighbors(node):
                if (
                    G.nodes[neighbor]["type"] == "developer"
                    and developer.lower() in neighbor.lower()
                ):
                    developer_games.append(node)

    # Count genres of games developed by this developer
    genre_count = {}
    for game_id in developer_games:
        for node in G.neighbors(game_id):
            if G.nodes[node]["type"] == "genre":
                genre_count[node] = genre_count.get(node, 0) + 1

    # Sort by count with descending order
    genre_count = dict(sorted(genre_count.items(), key=lambda item: item[1], reverse=True))

    return jsonify(genre_count)


@app.route("/graph/<platform>/popular_genres")
def show_popular_genres(platform):
    # Find all games of the given platform
    platform_games = []
    for node in G.nodes:
        if G.nodes[node]["type"] == "game":
            for neighbor in G.neighbors(node):
                if G.nodes[neighbor]["type"] == "platform" and platform.lower() in neighbor.lower():
                    platform_games.append(node)

    # Count genres of games on this platform
    genre_count = {}
    for game_id in platform_games:
        for node in G.neighbors(game_id):
            if G.nodes[node]["type"] == "genre":
                genre_count[node] = genre_count.get(node, 0) + 1

    # Sort by count with descending order
    genre_count = dict(sorted(genre_count.items(), key=lambda item: item[1], reverse=True))

    return jsonify(genre_count)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
