import pandas as pd
import numpy as np
import networkx as nx
import ast
import json

# Load data from CSV
df = pd.read_csv("data/steam_cleaned_200.csv")

# Create a new graph
G = nx.Graph()

# Add nodes and edges based on the CSV data
for index, row in df.iterrows():
    game_id = row["ID"]
    game_name = row["name"]
    developer = row["developers"]
    genres = row["genre"].split(",")
    platforms = ast.literal_eval(row["platform"])
    num_reviews = row["num_reviews"]
    positive_review_rate = row["positive_review_rate"]

    # Add game node
    G.add_node(
        game_id,
        type="game",
        name=game_name,
        price=row["price"],
        release_date=row["release_date"],
        developer=developer,
        genres=genres,
        platforms=platforms,
        num_reviews=num_reviews,
        positive_review_rate=positive_review_rate,
    )

    # Add developer node and edge
    G.add_node(developer, type="developer")
    G.add_edge(game_id, developer)

    # Add genre nodes and edges
    for genre in genres:
        G.add_node(genre, type="genre")
        G.add_edge(game_id, genre)

    # Add platform nodes and edges
    for platform in platforms:
        G.add_node(platform, type="platform")
        G.add_edge(game_id, platform)

# Now graph G is constructed with nodes and edges

# Save the graph into a json file
graph_data = nx.readwrite.json_graph.node_link_data(G)
with open("data/graph.json", "w", encoding="latin-1") as json_file:
    json.dump(graph_data, json_file)
