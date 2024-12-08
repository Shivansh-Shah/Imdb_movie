import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import importlib.util
import matplotlib
matplotlib.use('TkAgg')

# Define paths to your graph files
graph1_file = "votings_graph.py"
graph2_file = "ratings_graph.py"

def load_graph(file):
    """Load a graph from a specified file."""
    try:
        spec = importlib.util.spec_from_file_location("graph_module", file)
        graph_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(graph_module)
        return graph_module.generate_graph()  # Call the generate_graph function
    except Exception as e:
        print(f"Error loading graph from {file}: {e}")
        return None

# Set up the main application window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Graphs Viewer")
root.geometry("1050x500")

# Create frames for each graph
frame1 = ctk.CTkFrame(root, corner_radius=10)
frame1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

frame2 = ctk.CTkFrame(root, corner_radius=10)
frame2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# Load and display the first graph (from demofileforproject1.py)
figure1 = load_graph(graph1_file)
if figure1 is not None:
    canvas1 = FigureCanvasTkAgg(figure1, master=frame1)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill="both", expand=True)
else:
    error_label1 = ctk.CTkLabel(frame1, text="Failed to load graph from File 1.", font=("Arial", 12))
    error_label1.pack(pady=20)

# Load and display the second graph (from demographing.py)
figure2 = load_graph(graph2_file)
if figure2 is not None:
    canvas2 = FigureCanvasTkAgg(figure2, master=frame2)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill="both", expand=True)
else:
    error_label2 = ctk.CTkLabel(frame2, text="Failed to load graph from File 2.", font=("Arial", 12))
    error_label2.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()