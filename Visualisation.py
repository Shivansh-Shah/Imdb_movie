# Necessary libraries for running the file.

import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plot
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime

# Importing necessary functions from datascraped.py
from datascraped import getGraphData, getMovieID

# ===================================================================================================

# Constructing a class for total_votes graph
class Visualiser2:
    
    def __init__(self, GraphData):
        
        self.GraphData = GraphData

    
    # Method to display graph when called.
    
    def generate_graph(self):
        
        # Basic Syntax for creating a figure and a set of subplots
        fig, ax = plot.subplots()

        """ int(d['total_votes'].replace(',', '')) converts strings ( d['total_votes'] which are in thousands) into integers. """
        # Example: '234,560' is converted into 234560
        
        """ For better readability, we divide modified keys by 1000. """
        display_y = [int(d['total_votes'].replace(',', '')) / 1000 for d in self.GraphData]


        # Points to be displayed on axes are stored in the form of arrays.
        xpoints = np.array([datetime.fromtimestamp(d['x']/ 1000) for d in self.GraphData])
        ypoints = np.array(display_y)

        # Syntax to plot points on y-axis against x-axis 
        # color, marker, marksize, linestyle and linewidth are some customizers.
        ax.plot(xpoints, ypoints, color='teal', marker='o', markersize=2, linestyle='-', linewidth=1)

        
        # Datetime conversion factor
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        # Filters out the display points on x-axis upon a time interval of 6 months.
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))

        # Adds title to the graph ( not the window in which it pops up)
        ax.set_title('Total Votes Over Time', color='navy', fontsize=16, fontweight='bold')
        
        # Labelling x and y axes with some customizers
        ax.set_xlabel('Dates', color='darkred', fontsize=12, fontweight='bold')
        ax.set_ylabel("Total Votes ( in thousands )", color='darkred', fontsize=12, fontweight='bold')

        
        # Customizer to rotate points to x-axis to shift.
        plot.xticks(rotation=30, fontsize=8)
        
        #  Adds grids to the graph
        ax.grid(color='gray', linestyle='--', linewidth=0.5)
        
        # Function to limit the size of graph to the frame it's being alloted. ( If not alloted to any frame, it displays in 640x480 size format)
        plot.tight_layout()
        
        # Returns the figure.
        return fig

# ===================================================================================================


# Constructing a class for Average_ratings graph
# Figure in this class also records data from 2020.
class Visualiser1:
    
    
    def __init__(self, data):
        self.GraphData = data

    # Method to display graph when called
    def generate_graph(self):
        
        
        fig, ax = plot.subplots()

        display_y = [float(d['average_rating']) for d in self.GraphData]
        xpoints = np.array([datetime.fromtimestamp(d['x'] / 1000) for d in self.GraphData])
        ypoints = np.array(display_y)

        ax.plot(xpoints, ypoints, color='purple', marker='o', markersize=2, linestyle='-', linewidth=1)

        
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))

        ax.set_yticks([0, 2, 4, 6, 8, 10])
        
        ax.set_title('Average Rating Over Time', color='navy', fontsize=16, fontweight='bold')
        
        ax.set_xlabel('Dates', color='darkred', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Rating', color='darkred', fontsize=12, fontweight='bold')

        plot.xticks(rotation=30, fontsize=8)
        
        ax.grid(color='gray', linestyle='--', linewidth=0.5)
        
        plot.tight_layout()
        
        return fig

# ===================================================================================================

def graph_page(movieName):
    
    # Usin customizers for appearance and theme.
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")


    app = ctk.CTk()
    # Title and geometry for the window. 
    app.title(f"Graphs for {movieName}")
    app.geometry("1100x500")
    
    # Customizers to configure rows and columns.
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)
    
    
    # Function 
    def go_back():
    
        app.destroy()
        print("Back to dashboard!")
    # '#1A1A1A' is color code for a very dark shade of grey.
    sidebar = ctk.CTkFrame(app, width=250, fg_color="#1A1A1A")
    sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

    logo_label = ctk.CTkLabel(
        sidebar,
        text="CinePhille",
        font=ctk.CTkFont(size=18, weight="bold")
    )
    
    
    logo_label.pack(pady=(10, 20))

    
    back_button = ctk.CTkButton(
        sidebar,
        text="Back",
        font=ctk.CTkFont(size=14, weight="bold"),
        command=go_back,
        fg_color="#FFA500",
        text_color="black",
        hover_color="#FFB84D",
    )
    back_button.pack(fill="x", pady=10)

    
    content_frame = ctk.CTkFrame(app, fg_contcolor="transparent")
    content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
""" LOGIC PART FOR DISPLAYING GRAPHS """
    # Fetching MovieID and GraphData for the movie in the window page 
    
    movieID = getMovieID(movieName)
    GraphData = getGraphData(movieID)

    # Storing figures from classes into corresponding variables: ratings_graph and total_votes_graph
    ratings_graph = Visualiser1(GraphData)
    total_votes_graph= Visualiser2(GraphData)

    ##  Embedding figures into a Tkinter application.
    # customizing frames
    graph1_frame = ctk.CTkFrame(content_frame, fg_color="#2A2A2A", corner_radius=10)
    graph1_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)
    
    canvas1 = FigureCanvasTkAgg(ratings_graph.generate_graph(), master=graph1_frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill="both", expand=True)

    graph2_frame = ctk.CTkFrame(content_frame, fg_color="#2A2A2A", corner_radius=10)
    graph2_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    canvas2 = FigureCanvasTkAgg(total_votes_graph.generate_graph(), master=graph2_frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill="both", expand=True)

    # Runs the app.
    app.mainloop()


#
# # Sample Usage
# graph_page("Devara")
