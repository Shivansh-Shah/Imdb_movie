import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ratings_graph import Graph1
from votings_graph import Graph2

# Create the main application window
root = tk.Tk()
root.title("Average ratings and Total Votes graph")

# Create frames for each graph
frame1 = tk.Frame(root)
frame1.pack(side=tk.LEFT)

frame2 = tk.Frame(root)
frame2.pack(side=tk.RIGHT)

# Embed the first graph into the first frame
canvas1 = FigureCanvasTkAgg(Graph1, master=frame1)
canvas1.draw()
canvas1.get_tk_widget().pack()

# Embed the second graph into the second frame
canvas2 = FigureCanvasTkAgg(Graph2, master=frame2)
canvas2.draw()
canvas2.get_tk_widget().pack()

# Start the Tkinter event loop
root.mainloop()
