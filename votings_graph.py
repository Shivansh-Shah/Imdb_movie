# These are the following modules which you need to import


import matplotlib.pyplot as plot
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime


# We import certain functions from the file ( datascraped.py ) for conversions ( GraphData from MovieID, MovieID from MovieName )
from datascraped import getMovieID, getGraphData, movieName

# Aim : To construct a class in python which has methods that can return graphs.


class Visualiser2:
    
    def __init__(self, GraphData):
    # GraphData is fetched when class is called.     
        self.GraphData = GraphData
        
    def generate_graph(self):
        # This method returns total_votes graph ( from 2020 ).

         fig, ax = plot.subplots() # Basic syntax to call out a figure with axes ( ax ) 
         
    
        display_y = [int(d['total_votes'].replace(',', '')) / 1000 for d in self.GraphData]  
        # Display_y is  a list containing all the inner_dictionary['total_votes'] values from graphdata scraped from datascraped.py

    # The follow 2 lines create an array for points on x and y axes
        xpoints = np.array([datetime.fromtimestamp(d['x'] / 1000) for d in self.GraphData])

        ypoints = np.array(display_y)

    # Syntax for plotting x and y axes. ( color, marker, markersize, linestyle, linewidth are some modifications used for plotting the graph )
        ax.plot(xpoints, ypoints, color = 'Black', marker = 'o', markersize = 0.01, linestyle = '-', linewidth = 0.8)

    # Formatter for representing points on x-axis ( yyyy-mm)
    # DayLocator(interval = 180 ) filters out xpoints which are 180 days apart in days.
# Only those points filtered out are gonna be displayed on x-axis.
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval = 180))
        # Title for the graph ( note: this is for the graph not the window it pops in the taskbar ).
        ax.set_title('Total Votes Over Time', color = 'Black', fontsize = 20)

        # Another modification to rotate points displayed on x-axis for better readability.
        plot.xticks(rotation = 30, fontsize = 5)

        # Labels x and y axes.
        ax.set_xlabel('Dates', color = 'Red', fontsize = 10)
        ax.set_ylabel("Total Votes( in thousands )", color = 'Red', fontsize = 20)

        # Adds grids ( also for better readability. )
        ax.grid()
        #  Limits the total size of graph.
        plot.tight_layout()

        # This returns the figure.
        return fig


""" Additional Comments """ 
# plot.tight_layout() limits the size of whole figure when it is called to display in frames. 
# Difference is noticed when we display th
        
    


