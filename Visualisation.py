# The following are the necessary modules needed for displaying a new window

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Logic part for ratings and votings graphs are written in the form of classes and we import those classes here to make use of them.

from ratings_graph import Visualiser1
from votings_graph import Visualiser2

# datascraped.py is the file from which we're fetching data from, the below functions are required to fetch the graph data which Visualiser1 and 
# Visualiser2 classes make use of for generation of graphs.

from datascraped import getMovieID, getGraphData, movieName 

# ---- 


# We define a class named CreatWindow which implements the whole logic part reuired to generate a window.

class CreateWindow:
    #Creates a Tkinter window displaying two graphs and handles errors.

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
        #  This method displays the graphs in the Tkinter window.
        # In short, canvas1 and canvas2 embeds the  graphs into their corresponding frames.
        canvas1 = FigureCanvasTkAgg(graph1, master=self.frame1)
        canvas1.draw()
        canvas1.get_tk_widget().pack() # This is for graph in first frame.

    
        canvas2 = FigureCanvasTkAgg(graph2, master=self.frame2)
        canvas2.draw()
        canvas2.get_tk_widget().pack() # This is for graph in second frame.

    def show_error(self, message):
    # This pops up an error message only when we try to access an invalid moviename.
        self.error_label.config(text=message)

    def run(self):
        # This begins the execution. 
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
    

# This runs the main function, which in turn, returns the window which we desired. 
if __name__ == "__main__":
    main()
  
