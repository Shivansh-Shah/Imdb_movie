# Libraries required 

import requests
from bs4 import BeautifulSoup

#  Function to get movieID from our app's source 
def getMovieID(movieName):

    url="https://www.ratingraph.com/search-results/"
    
    for i in movieName.split(" "):
        
        url = url + i + "%20"
    movie = requests.get(url)
    
    if movie.status_code == 200:
    
        soup = BeautifulSoup(movie.text, 'html.parser' )
        data = soup.find_all( 'div' , class_ = 'titles results' )
        return(( data[0].find_all('a')[0].get('href') ).split('-')[-1][0:-1] )
    # Returns movieID for a specific movie title recorded in the source site.
    ## Major problem: Any typo while giving movieName as input causes error.
    ## It is advised to follow the correct spelling of a movie that is recorded
    # in the website as the function builds url to get ID 
    else:
    
        return -1
    
# Function the get graphData required for Visualisation.py
def getGraphData(movieID):
    
    url = "https://www.ratingraph.com/movie-history/"+movieID+'/'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        
        data = response.json()
        return( data[1]['data'] ) 
    
    else:
        return -1
    

# Function to retrieve MovieData for storing in database system.
def getMovieData(movieName):
    
    url = "https://www.omdbapi.com/?t="
    
    for i in movieName.split():
        url = url + i + "+"
    
    url = url[:len(url)-1] + "&plot=full&apikey=c2403270"
    response=requests.get(url)
    
    if response.status_code == 200:
    
        data = response.json()
        return(data) 
    
    else:
        return -1
    

