import matplotlib.pyplot as plot #Module for graphs
import numpy as np
# The below two modules imported are necessary for datetime conversions.
import matplotlib.dates as mdates
from datetime import datetime

#This is the data on which the graphs are based on
from datascraped import GraphData

# A function that generates a graph plotting total_votes from 2020 on y-axis against Dates on x-axis.
def generate_graph():

    # A function that returns a tuple containing figure and axes
    fig, ax = plot.subplots()
    # This list contains all the elements in d['total_votes'] with their commas(,) replaced with '' .
    # The above conversion is done for display points on y axis ( looks clean ).
    display_y = [int(d['total_votes'].replace(',', '')) / 1000 for d in GraphData] 
    #Conversion into seconds and then storing all the elements d['x'] in the form of an array
    xpoints = np.array([datetime.fromtimestamp(d['x'] / 1000) for d in GraphData] )
    #Consists of all display_y elements in the form of an array
    ypoints = np.array(display_y)
    # Reason for choosing arrays: From multiple sources, it's been recommended that 
    ax.plot(xpoints, ypoints, color = 'Black', marker = 'o', markersize = 0.01, linestyle = '-', linewidth = 0.8)
        
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval = 180))
            
    ax.set_title('Total Votes Over Time', color = 'Black', fontsize = 20)
            
    plot.xticks(rotation = 30, fontsize = 5)
            
    ax.set_xlabel('Dates', color = 'Red', fontsize = 10)
    ax.set_ylabel("Total Votes( in thousands )", color = 'Red', fontsize = 20)
            
    ax.grid()
    plot.tight_layout()
    fig.set_size_inches(6, 4)
    return fig
        
    
graph2 = generate_graph()
print(graph2)
plot.show()


