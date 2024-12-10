import matplotlib.pyplot as plot # This is for graphs

import numpy as np # Used for graphs too

# Both of the given codes are for datetime conversions.

import matplotlib.dates as mdates 
from datetime import datetime

#This is the data on which the graphs are based on.
from datascraped import getGraphData, movieName, getMovieID

# Important point: The data is based on results it have been recording since 2020.

class Visualiser1:
    def __init__(self, GraphData):
        
        self.GraphData = GraphData
# Function to generate graph ( in this case, it's average_ratings over a period of time)
    def generate_graph(self):
        
        # Function to return a tuple containing figure and axes 
        fig, ax = plot.subplots()
        
        # A list to store average ratings.
        display_y = [float(d['average_rating']) for d in self.GraphData]
    # These are storing all the possible x- coordinates
        xpoints = np.array([datetime.fromtimestamp(d['x']/ 1000) for d in self.GraphData])
    # These are all the y coordinates
        ypoints = np.array(display_y)

    # Function that calls to plot xpoints and ypoints
        ax.plot(xpoints, ypoints, color = 'Purple')
    #Formatter to represent x coordinates ( because GraphData has d['x'] in epoch time and above xpoints did conversion into seconds)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    #Filtering out the possible x-coordinates that are to be displayed by a time gap of 180 days.
        ax.xaxis.set_major_locator(mdates.DayLocator(interval = 180))

    #Display points on y axis. ( [0, 10] because average ratings lie in that interval only.)
        ax.set_yticks([0, 2, 4, 6, 8, 10]) 
    #Another formatter( for x co-ordinates that are shown) for better readability ( rotates the x-coordinates in anti-clockwise order. )
        plot.xticks( rotation = 30,fontsize = 5)

    # Adding title to the whole Graph
        ax.set_title('Average rating over time', color = 'Black', fontsize = 20)
    #Adding Labels for x and y axeses with some modifications
        ax.set_xlabel('Dates', color = 'Red', fontsize = 14 )

        ax.set_ylabel('Average Rating', color = 'Red', fontsize = 20 )
    # Making the graph have grids ( looks clean and neat afterwards)
        ax.grid()
        
        plot.tight_layout()
        
        return fig
        
    

# print(graph1) -> Doesn't show the graph but instead shows the dimensions of the graph that is gonna pop up.

# plot.show() -> Only this function can again make the graph pop up in a new window, even when it's outside the function.

