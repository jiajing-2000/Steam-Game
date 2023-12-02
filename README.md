# Interactive Game Graph

## Description

This project aims to analyze and visualize game data using a graph-based approach. Each game, genre, developer, and platform is represented as a node, and relationships between them are represented as edges. The project provides interactive visualizations for each type of node.

## Methods

### Node Creation

1. **Games**: Each game is represented as a node with attributes such as Title, Price, Description, Developer, Review Summary, Release Date, Platforms, Required Age, and System Requirements.
2. **Genres**: Each genre is represented as a node.
3. **Developers**: Each developer is represented as a node.
4. **Platforms**: Each platform (e.g., Windows, Mac, Linux) is represented as a node.

### Edge Creation

1. **Game-Genre Edges**: Connect games to their genres.
2. **Game-Developer Edges**: Connect games to their developers.
3. **Game-Platform Edges**: Connect games to the platforms they are available on.

### Graph Construction

The graph is constructed using the `networkx` library in Python.

## Data Interaction and Visualization

The data is presented through a web interface, with front-end visualizations using `D3.js` and server-side graph operations using `networkx`.

### Game Node Interaction

When a user selects a game node:

1. **Genre Distribution**: A pie chart of the distribution of genres of similar games is displayed.
2. **Developer Connection**: A subgraph showing how this game is connected to other games through shared developers is displayed.

### Genre Node Interaction

When a user selects a genre node:

1. **Popular Games**: The top N popular games in this genre are listed.
2. **Genre Evolution Over Time**: A line graph showing the number of games in this genre released each year is displayed.

### Developer Node Interaction

When a user selects a developer node:

1. **Game Portfolio**: All the games developed by this developer, along with key information, are displayed.
2. **Genre Expertise**: A pie chart of the genre distribution of games developed by this developer is displayed.

### Platform Node Interaction

When a user selects a platform node:

1. **Popular Genres**: A bar chart of the most popular genres on this platform is displayed.

## Usage

```bash
python app.py
```

Then navigate to http://localhost:5000 in your browser.

## Project Structure

- app.py: This is the main Python file that runs the Flask application.
- templates/index.html: This is the HTML file that the Flask application renders.