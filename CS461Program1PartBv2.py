import csv
import random
from collections import deque
from tkinter import (
    Button,
    Label,
    OptionMenu,
    StringVar,
    BooleanVar,
    Checkbutton,
    Radiobutton,
    Canvas,
    Tk,
    filedialog,
    messagebox
)

import matplotlib.pyplot as plt
import networkx as nx

SEARCH_STEP_DELAY_SECONDS = 0.2


def read_coordinates(file_path):
    cities = {}
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 3:
                continue
            city_name = row[0].strip()
            latitude = float(row[1])
            longitude = float(row[2])
            cities[city_name] = (latitude, longitude)
    return cities


def read_adjacencies(file_path):
    adjacencies = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            city_a = parts[0]
            neighbors = parts[1:]
            adjacencies.setdefault(city_a, set())
            for city_b in neighbors:
                adjacencies.setdefault(city_b, set())
                adjacencies[city_a].add(city_b)
                adjacencies[city_b].add(city_a)
    return {city: sorted(list(neighbors)) for city, neighbors in adjacencies.items()}


def normalize_graph(cities, adjacencies):
    known = set(cities.keys())
    return {
        city: sorted([neighbor for neighbor in neighbors if neighbor in known])
        for city, neighbors in adjacencies.items()
        if city in known
    }


def build_networkx_graph(graph, cities):
    g = nx.Graph()
    for city in cities:
        g.add_node(city, pos=cities[city])
    for city, neighbors in graph.items():
        for neighbor in neighbors:
            g.add_edge(city, neighbor)
    return g


def draw_search_state(ax, g, pos, visited, frontier, current, start, goal, path=None):
    ax.clear()
    frontier_nodes = set(frontier)
    node_colors = []
    for node in g.nodes:
        if path and node in path:
            node_colors.append("orange")
        elif node == start:
            node_colors.append("limegreen")
        elif node == goal:
            node_colors.append("red")
        elif node == current:
            node_colors.append("gold")
        elif node in frontier_nodes:
            node_colors.append("deepskyblue")
        elif node in visited:
            node_colors.append("lightgray")
        else:
            node_colors.append("white")

    nx.draw_networkx_edges(g, pos, ax=ax, edge_color="silver", width=1)
    nx.draw_networkx_nodes(
        g,
        pos,
        ax=ax,
        node_color=node_colors,
        edgecolors="black",
        node_size=520,
    )
    nx.draw_networkx_labels(g, pos, ax=ax, font_size=9, font_weight="bold")

    if path and len(path) > 1:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(g, pos, ax=ax, edgelist=path_edges, edge_color="orange", width=3)

    ax.set_title("City Route Search (live)")
    ax.axis("off")
    plt.pause(SEARCH_STEP_DELAY_SECONDS)


def bfs(graph, start_city, goal_city, on_step=None):
    if start_city == goal_city:
        if on_step:
            on_step(set(), [], start_city, [start_city])
        return [start_city]

    visited = {start_city}
    queue = deque([[start_city]])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if on_step:
            on_step(set(visited), [p[-1] for p in queue], node, None)

        for neighbor in graph.get(node, []):
            if neighbor in visited:
                continue
            new_path = path + [neighbor]
            if neighbor == goal_city:
                if on_step:
                    on_step(set(visited) | {neighbor}, [p[-1] for p in queue], neighbor, new_path)
                return new_path
            visited.add(neighbor)
            queue.append(new_path)
    return None


def dfs(graph, start_city, goal_city, on_step=None):
    if start_city == goal_city:
        if on_step:
            on_step(set(), [], start_city, [start_city])
        return [start_city]

    stack = [[start_city]]
    visited = set()

    while stack:
        path = stack.pop()
        node = path[-1]
        if node in visited:
            continue

        visited.add(node)
        if on_step:
            on_step(set(visited), [p[-1] for p in stack], node, None)

        if node == goal_city:
            if on_step:
                on_step(set(visited), [p[-1] for p in stack], node, path)
            return path

        neighbors = list(graph.get(node, []))
        neighbors.reverse()
        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append(path + [neighbor])
    return None


def run_and_animate_search(graph, cities, search_method, start_city, goal_city):
    g = build_networkx_graph(graph, cities)
    pos = nx.get_node_attributes(g, "pos")
    fig, ax = plt.subplots(figsize=(12, 12))
    plt.ion()

    def on_step(visited, frontier, current, maybe_path):
        draw_search_state(
            ax=ax,
            g=g,
            pos=pos,
            visited=visited,
            frontier=frontier,
            current=current,
            start=start_city,
            goal=goal_city,
            path=maybe_path,
        )

    if search_method == "DFS":
        path = dfs(graph, start_city, goal_city, on_step=on_step)
    else:
        path = bfs(graph, start_city, goal_city, on_step=on_step)

    final_visited = set(graph.keys()) if path is None else set(path)
    draw_search_state(
        ax=ax,
        g=g,
        pos=pos,
        visited=final_visited,
        frontier=[],
        current=goal_city if path else None,
        start=start_city,
        goal=goal_city,
        path=path,
    )
    plt.ioff()
    plt.show()
    return path


def generate_random_graph(node_count=12, edge_probability=0.28):
    points = {}
    for i in range(node_count):
        name = f"City{i + 1}"
        points[name] = (random.uniform(0, 100), random.uniform(0, 100))

    names = list(points.keys())
    adj = {name: set() for name in names}
    for i in range(node_count):
        for j in range(i + 1, node_count):
            if random.random() < edge_probability:
                adj[names[i]].add(names[j])
                adj[names[j]].add(names[i])

    for i in range(node_count - 1):
        if names[i + 1] not in adj[names[i]]:
            adj[names[i]].add(names[i + 1])
            adj[names[i + 1]].add(names[i])

    return points, {k: sorted(list(v)) for k, v in adj.items()}


def ask_demo_options():
    root = Tk()
    root.title("Graph Search Demo Setup")
    root.geometry("420x260")

    graph_mode = StringVar(value="Provided")
    search_method = StringVar(value="BFS")

    # ADDED: checkbox variable
    show_animation = BooleanVar(value=True)

    coordinates_file = StringVar(value="coordinates.csv")
    adjacencies_file = StringVar(value="Adjacencies.txt")
    values = {}

    def pick_coordinates():
        path = filedialog.askopenfilename(
            title="Select coordinates CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if path:
            coordinates_file.set(path)

    def pick_adjacencies():
        path = filedialog.askopenfilename(
            title="Select adjacencies file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if path:
            adjacencies_file.set(path)

    def submit():
        values["graph_mode"] = graph_mode.get()
        values["search_method"] = search_method.get()

        # ADDED: save checkbox value
        values["show_animation"] = show_animation.get()

        values["coordinates_file"] = coordinates_file.get().strip()
        values["adjacencies_file"] = adjacencies_file.get().strip()
        root.destroy()

    Label(root, text="Search method").grid(
        row=0,
        column=0,
        sticky="w",
        padx=10,
        pady=8
    )

    # CHANGED: OptionMenu replaced with radio buttons
    Radiobutton(
        root,
        text="BFS",
        variable=search_method,
        value="BFS"
    ).grid(
        row=0,
        column=1,
        sticky="w",
        padx=10
    )

    Radiobutton(
        root,
        text="DFS",
        variable=search_method,
        value="DFS"
    ).grid(
        row=0,
        column=2,
        sticky="w",
        padx=10
    )

    Label(root, text="Graph source").grid(
        row=1,
        column=0,
        sticky="w",
        padx=10,
        pady=8
    )

    OptionMenu(
        root,
        graph_mode,
        "Provided",
        "Random"
    ).grid(
        row=1,
        column=1,
        sticky="ew",
        padx=10
    )

    # ADDED: check box
    Checkbutton(
        root,
        text="Show search animation",
        variable=show_animation
    ).grid(
        row=2,
        column=0,
        columnspan=3,
        pady=8
    )

    # ADDED: GUI line
    line = Canvas(
        root,
        width=380,
        height=10,
        highlightthickness=0
    )

    line.create_line(
        10,
        5,
        370,
        5,
        fill="black",
        width=2
    )

    line.grid(
        row=3,
        column=0,
        columnspan=3,
        pady=5
    )

    Button(
        root,
        text="Pick Coordinates",
        command=pick_coordinates
    ).grid(
        row=4,
        column=0,
        padx=10,
        pady=8
    )

    Button(
        root,
        text="Pick Adjacencies",
        command=pick_adjacencies
    ).grid(
        row=4,
        column=1,
        padx=10,
        pady=8
    )

    Button(
        root,
        text="Run Demo",
        command=submit
    ).grid(
        row=5,
        column=0,
        columnspan=3,
        pady=12
    )

    root.columnconfigure(1, weight=1)
    root.mainloop()
    return values


def ask_start_goal_from_graph(cities):
    names = sorted(cities.keys())
    root = Tk()
    root.title("Choose Start and Goal")
    root.geometry("340x140")

    start_city = StringVar(value=names[0])
    goal_city = StringVar(value=names[min(1, len(names) - 1)])
    selected = {}

    def submit():
        selected["start"] = start_city.get()
        selected["goal"] = goal_city.get()
        root.destroy()

    Label(root, text="Start city").grid(
        row=0,
        column=0,
        sticky="w",
        padx=10,
        pady=10
    )

    OptionMenu(
        root,
        start_city,
        *names
    ).grid(
        row=0,
        column=1,
        sticky="ew",
        padx=10
    )

    Label(root, text="Goal city").grid(
        row=1,
        column=0,
        sticky="w",
        padx=10,
        pady=10
    )

    OptionMenu(
        root,
        goal_city,
        *names
    ).grid(
        row=1,
        column=1,
        sticky="ew",
        padx=10
    )

    Button(
        root,
        text="Search",
        command=submit
    ).grid(
        row=2,
        column=0,
        columnspan=2,
        pady=8
    )

    root.columnconfigure(1, weight=1)
    root.mainloop()
    return selected


def main():
    options = ask_demo_options()

    if not options:
        return

    if options["graph_mode"] == "Random":
        cities, adjacencies = generate_random_graph()

    else:
        try:
            cities = read_coordinates(
                options["coordinates_file"]
            )

            adjacencies = read_adjacencies(
                options["adjacencies_file"]
            )

        except FileNotFoundError as err:
            messagebox.showerror(
                "File Error",
                str(err)
            )
            return

        adjacencies = normalize_graph(
            cities,
            adjacencies
        )

    if not cities or not adjacencies:
        messagebox.showerror(
            "Input Error",
            "No valid graph data loaded."
        )
        return

    picks = ask_start_goal_from_graph(cities)

    if not picks:
        return

    start_city = picks["start"]
    goal_city = picks["goal"]

    if start_city not in adjacencies or goal_city not in adjacencies:
        messagebox.showerror(
            "Input Error",
            "Start or goal is not in the graph."
        )
        return

    # CHANGED: checkbox determines whether animation is shown
    if options["show_animation"]:
        path = run_and_animate_search(
            graph=adjacencies,
            cities=cities,
            search_method=options["search_method"],
            start_city=start_city,
            goal_city=goal_city,
        )

    else:
        # Run the search without displaying the animation
        if options["search_method"] == "DFS":
            path = dfs(
                adjacencies,
                start_city,
                goal_city
            )
        else:
            path = bfs(
                adjacencies,
                start_city,
                goal_city
            )

    if path:
        print(
            f"{options['search_method']} path: "
            f"{' -> '.join(path)}"
        )

    else:
        print(
            f"No path found from "
            f"{start_city} to {goal_city}."
        )


if __name__ == "__main__":
    main()
