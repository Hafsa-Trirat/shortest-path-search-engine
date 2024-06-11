import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox

# Initialization
graph = None

def get_map_data(city_name):
    place_name = city_name + ", Algeria"  # Assuming Algeria for all cities
    global graph
    graph = ox.graph_from_place(place_name, network_type='drive')
    return graph

def update_nodes(event=None):
    selected_city = combobox_city.get()
    graph = get_map_data(selected_city)
    listbox_source.delete(0, tk.END)
    listbox_target.delete(0, tk.END)
    node_names = get_node_names(graph)
    for node in node_names.values():
        listbox_source.insert(tk.END, node)
        listbox_target.insert(tk.END, node)

def get_node_names(graph):
    node_names = {}
    for node in graph.nodes():
        node_names[node] = graph.nodes[node].get('name', f"Unnamed Node {node}")
    return node_names

def a_star_search(graph, source, target):
    path = nx.astar_path(graph, source, target, weight='length')
    return path

def plot_shortest_path(graph, shortest_path, ax):
    ox.plot_graph_route(graph, shortest_path, route_color='g', route_linewidth=3, node_size=0, ax=ax, show=False)

def main():
    selected_source = listbox_source.get(tk.ACTIVE)
    selected_target = listbox_target.get(tk.ACTIVE)
    
    if selected_source and selected_target:
        node_names = get_node_names(graph)
        # Reverse lookup to get the actual node IDs
        source_node = next(key for key, value in node_names.items() if value == selected_source)
        target_node = next(key for key, value in node_names.items() if value == selected_target)
        shortest_path = a_star_search(graph, source_node, target_node)
        plot_graph(shortest_path)
    else:
        messagebox.showwarning("Warning", "Please select both source and target nodes.")

def plot_graph(shortest_path):
    fig, ax = plt.subplots(figsize=(8, 6))
    ox.plot_graph(graph, ax=ax, node_size=0, show=False)
    plot_shortest_path(graph, shortest_path, ax)
    canvas = FigureCanvasTkAgg(fig, master=frame_map)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Initialize Tkinter
root = tk.Tk()

# Create frames for better organization
frame_input = ttk.Frame(root, padding="10")
frame_input.pack(fill='both', expand=True)

frame_map = ttk.Frame(root, padding="10", style="Map.TFrame")
frame_map.pack(fill='both', expand=True)

frame_buttons = ttk.Frame(root, padding="10")
frame_buttons.pack(fill='x')

btn_find_path = ttk.Button(
    frame_buttons, 
    text="Find Shortest Path", 
    command=main, 
    style="Accent.TButton"
)
btn_find_path.pack(fill='x', padx=5, pady=5)

# Create and place the widgets
label_city = ttk.Label(frame_input, text="Select City:")
label_city.grid(row=0, column=0, padx=5, pady=5)

cities = [
    "Adrar", "Ain Defla", "Ain Temouchent", "Alger", "Annaba", "Batna",
    "Bechar", "Bejaia", "Biskra", "Blida", "Bordj Bou Arreridj", "Bouira",
    "Boumerdes", "Chlef", "Constantine", "Djelfa", "El Bayadh", "El Oued",
    "El Tarf", "Ghardaia", "Guelma", "Illizi", "Jijel", "Khenchela",
    "Laghouat", "Muaskar", "Medea", "Mila", "Mostaganem", "Msila", "Naama",
    "Oran", "Ouargla", "Oum el Bouaghi", "Relizane", "Saida", "Setif", "Sidi Bel Abbes",
    "Skikda", "Souk Ahras", "Tamanrasset", "Tebessa", "Tiaret", "Tindouf",
    "Tipaza", "Tissemsilt", "Tizi Ouzou", "Tlemcen"
]

combobox_city = ttk.Combobox(frame_input, values=cities)
combobox_city.grid(row=0, column=1, padx=5, pady=5)
combobox_city.bind("<<ComboboxSelected>>", update_nodes)

label_source = ttk.Label(frame_input, text="Source Place:")
label_source.grid(row=1, column=0, padx=5, pady=5)

listbox_source = tk.Listbox(frame_input, selectmode="browse")
listbox_source.grid(row=1, column=1, padx=5, pady=5)

label_target = ttk.Label(frame_input, text="Destination Place:")
label_target.grid(row=2, column=0, padx=5, pady=5)

listbox_target = tk.Listbox(frame_input, selectmode="browse")
listbox_target.grid(row=2, column=1, padx=5, pady=5)

# Style configuration
style = ttk.Style()
style.configure("Accent.TButton", background="#787878", foreground="green")
style.configure("Map.TFrame", background="light blue")

# Run the main loop
root.mainloop()
