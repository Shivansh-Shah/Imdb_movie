import requests

from bs4 import BeautifulSoup


def getMovieID(movieName):

    url="https://www.ratingraph.com/search-results/"
    
    for i in movieName.split(" "):
        
        url = url + i + "%20"
    movie = requests.get(url)
    
    if movie.status_code == 200:
    
        soup = BeautifulSoup(movie.text, 'html.parser' )
        data = soup.find_all( 'div' , class_ = 'titles results' )
        return(float( data[0].find_all('a')[0].get('href') ).split('-')[-1][0:-1] )
    
    else:
    
        return -1
    

def getGraphData(movieID):
    
    url = "https://www.ratingraph.com/movie-history/"+movieID+'/'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        
        data = response.json()
        return( data[1]['data'] ) 
    
    else:
        return -1
    

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
    

movieName = input()
movieID = getMovieID(movieName)
GraphData = getGraphData(movieID)
movieData = getMovieData(movieName)

print(GraphData)
