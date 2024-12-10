import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from finalbuf1 import Visualiser1
from finalbuf2 import Visualiser2
from datascraped import getMovieID, getGraphData, movieName 

class CreateWindow:
    """Creates a Tkinter window displaying two graphs and handles errors."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Average Ratings and Total Votes Graph")

        # Create frames for each graph
        self.frame1 = tk.Frame(self.root)
        self.frame1.pack(side=tk.LEFT)

        self.frame2 = tk.Frame(self.root)
        self.frame2.pack(side=tk.RIGHT)

        # Label for displaying errors
        self.error_label = tk.Label(self.root, text="", fg="red")
        self.error_label.pack(side=tk.BOTTOM)

    def display_graphs(self, graph1, graph2):
        """Displays the graphs in the Tkinter window."""
        # Embed the first graph into the first frame
        canvas1 = FigureCanvasTkAgg(graph1, master=self.frame1)
        canvas1.draw()
        canvas1.get_tk_widget().pack()

        # Embed the second graph into the second frame
        canvas2 = FigureCanvasTkAgg(graph2, master=self.frame2)
        canvas2.draw()
        canvas2.get_tk_widget().pack()

    def show_error(self, message):
        """Displays an error message in the error label."""
        self.error_label.config(text=message)

    def run(self):
        """Starts the Tkinter event loop."""
        self.root.mainloop()

def main():
    """Main function to fetch data and generate graphs."""
    window = CreateWindow()
    
    try:
        visualiser1 = Visualiser1(getGraphData(getMovieID(movieName)))
        visualiser2 = Visualiser2(getGraphData(getMovieID(movieName)))
        
        
        window.display_graphs(visualiser1.generate_graph(), visualiser2.generate_graph())
    except Exception as e:
        # Shows error messages if generated -> This is done only when we try to open any movie that is not in the moviedatabase.
        window.show_error(f"An error occurred while generating graphs: {e}")

    # Run the Tkinter event loop
    window.run()

# Run the main function
if __name__ == "__main__":
    main()
  
