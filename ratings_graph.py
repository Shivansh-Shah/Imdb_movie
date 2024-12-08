import matplotlib.pyplot as plot # This is for graphs

import numpy as np # Used for graphs too

# Both of the given codes are for datetime conversions.
import matplotlib.dates as mdates 

from datetime import datetime

#This is the data on which the graphs are based on.
from datascraped import GraphData

# Important point: The data is based on results it have been recording since 2020.

# Function to generate graph ( in this case, it's average_ratings over a period of time)
def generate_graph():
    
    # 
    fig, ax = plot.subplots()
    
    
    display_y = [float(d['average_rating']) for d in GraphData]

    xpoints = np.array([datetime.fromtimestamp(d['x']/ 1000) for d in GraphData])
    ypoints = np.array(display_y)

    ax.plot(xpoints, ypoints, color = 'Purple')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval = 180))

    ax.set_yticks([0, 2, 4, 6, 8, 10]) 

    plot.xticks( rotation = 30,fontsize = 5)

    ax.set_title('Average rating over time', color = 'Black', fontsize = 20)

    ax.set_xlabel('Dates', color = 'Red', fontsize = 14 )

    ax.set_ylabel('Average Rating', color = 'Red', fontsize = 20 )

    ax.grid()
        
    return fig
    
    
graph1 = generate_graph()

print(graph1)


#print(fig1)


