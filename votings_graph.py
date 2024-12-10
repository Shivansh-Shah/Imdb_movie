import matplotlib.pyplot as plot
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime

from datascraped import getMovieID, getGraphData, movieName

class Visualiser2:
    
    def __init__(self, GraphData):
        
        self.GraphData = GraphData
        
    def generate_graph(self):
        
        
        fig, ax = plot.subplots()
        
        display_x = [d['x'] for d in self.GraphData]
        display_y = [int(d['total_votes'].replace(',', '')) / 1000 for d in self.GraphData] 

        xpoints = np.array([datetime.fromtimestamp(d / 1000) for d in display_x] )

        ypoints = np.array(display_y)

        ax.plot(xpoints, ypoints, color = 'Black', marker = 'o', markersize = 0.01, linestyle = '-', linewidth = 0.8)
            
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval = 180))
                
        ax.set_title('Total Votes Over Time', color = 'Black', fontsize = 20)
                
        plot.xticks(rotation = 30, fontsize = 5)
                
        ax.set_xlabel('Dates', color = 'Red', fontsize = 10)
        ax.set_ylabel("Total Votes( in thousands )", color = 'Red', fontsize = 20)
                
        ax.grid()
        plot.tight_layout()
        return fig
        
    


