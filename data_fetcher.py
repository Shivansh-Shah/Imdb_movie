import requests
from bs4 import BeautifulSoup
from data_scraping import *
import mysql.connector as mysql

def connect_db():
    '''function to connect to local MySQL server'''
    return mysql.connect(
        host="localhost",  # your MySQL server host
        user="root",       # your MySQL username
        password="sha123Ivi",  # your MySQL password
        database="cinephile_app"  # your MySQL database name
    )

con = connect_db()
cur = con.cursor()

def convert_date_format(date):
    '''function to convert date scraped into sql-accepted format'''
    lst = date.split()
    def month_from_date(lst):
        if lst[1] == 'Jan':
            return '01'
        elif lst[1] == 'Feb':
            return '02'
        elif lst[1] == 'Mar':
            return '03'
        elif lst[1] == 'Apr':
            return '04'
        elif lst[1] == 'May':
            return '05'
        elif lst[1] == 'Jun':
            return '06'
        elif lst[1] == 'Jul':
            return '07'
        elif lst[1] == 'Aug':
            return '08'
        elif lst[1] == 'Sep':
            return '09'
        elif lst[1] == 'Oct':
            return '10'
        elif lst[1] == 'Nov':
            return '11'
        elif lst[1] == 'Dec':
            return '12'
    newdate = lst[2] + '-' + month_from_date(lst) + '-' + lst[0]
    return newdate

def movie_data_dump(MovieID, data):
    '''function to dump all movie data scraped into the database'''
    #opening cursor
    cur = con.cursor()
    #building insert statements
    
    #inserting into movie table
    Mov_Dat_DML = 'INSERT INTO Movies (MovieID,  MovieName, MovieDate, MoviePlot, MoviePhoto, MovieRating) VALUES ({}, "{}", "{}", "{}", "{}", {});'.format(MovieID, data['Title'], convert_date_format(data['Released']), data['Plot'], data['Poster'], float(data['imdbRating']))
    cur.execute(Mov_Dat_DML)
    con.commit()

    #inserting into movie-genre relationship table
    Genre_List = data['Genre'].split(", ")
    
    for i in Genre_List:
        GenreID_Query = "SELECT GenreID FROM Genres WHERE GenreName = '{}';".format(i)
        cur.execute(GenreID_Query)
        GenreID = cur.fetchone()[0]
        Genre_Dat_DML =  "INSERT INTO Movie_Genre(MovieID, GenreID) VALUES({}, '{}');".format(MovieID, GenreID)    
        cur.execute(Genre_Dat_DML)
        con.commit()
 
    #inserting into movie-actor relationship table
    Actor_List = data['Actors'].split(", ")
    Actors_Query = "SELECT ActorName from Actors;"
    cur.execute(Actors_Query)
    Existing_Actors = [x[0] for x in list(cur.fetchall())]

    for i in Actor_List:
        #inserting into actor table if actor data isnt already present
        if i not in Existing_Actors:
            ActorID = i[0:3] + i[-3:] #actor ID is made up of 3 letters of first name and 3 letters of last name
            Actor_Info_DML = "INSERT INTO Actors(ActorID, ActorName) VALUES('{}', '{}')".format(ActorID, i)
            cur.execute(Actor_Info_DML)
            con.commit()
    
        #inserting into movie-actor relationship table
        ActorID_Query = "SELECT ActorID FROM Actors WHERE ActorName = '{}';".format(i)
        cur.execute(ActorID_Query)
        ActorID = cur.fetchone()[0]
        Actor_Dat_DML =  "INSERT INTO Movie_Actor(MovieID, ActorID) VALUES({}, '{}');".format(MovieID, ActorID)    
        cur.execute(Actor_Dat_DML)
        con.commit()

    #inserting into movie-director relationship table
    Director_List = data['Director'].split(", ")
    Directors_Query = "SELECT DirectorName from Directors;"
    cur.execute(Directors_Query)
    Existing_Directors = [x[0] for x in list(cur.fetchall())]

    for i in Director_List:
        #inserting into director table if director data isnt already present
        if i not in Existing_Directors:
            DirectorID = i[0:3] + i[-3:] #director ID is made up of 3 letters of first name and 3 letters of last name
            Director_Info_DML = "INSERT INTO Directors(DirectorID, DirectorName) VALUES('{}', '{}')".format(DirectorID, i)
            cur.execute(Director_Info_DML)
            con.commit()
    
        #inserting into movie-director relationship table
        DirectorID_Query = "SELECT DirectorID FROM Directors WHERE DirectorName = '{}';".format(i)
        cur.execute(DirectorID_Query)
        DirectorID = cur.fetchone()[0]
        Director_Dat_DML =  "INSERT INTO Movie_Director(MovieID, DirectorID) VALUES({}, '{}');".format(MovieID, DirectorID)    
        cur.execute(Director_Dat_DML)
        con.commit()

    con.commit()
    cur.close()

class Movie: #defining a class movie to store all data retrieved about the movie from the database.
    def __init__(self, id, name, date, plot, photo, rating, actors, directors, genres):
        self.id = id
        self.name = name
        self.date = date
        self.plot = plot
        self.photo = photo
        self.rating = rating
        self.actors = actors
        self.directors = directors
        self.genres = genres

def build_moviedata_object(MovieID):
    ''' getting all movie data from the database about a particular movie and returning it in the form of a movie object'''
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM Movies WHERE MovieID = {}".format(MovieID))
        retr_movie = list(cur.fetchall())[0] #converting data retrieved(id, name, date, plot, photo, rating) into tuple form to slice it
        if retr_movie is None:
            raise Exception
        cur.execute("SELECT Genres.GenreName FROM Movie_Genre, Genres WHERE Movie_Genre.GenreID = Genres.GenreID AND Movie_Genre.MovieID = {}".format(MovieID))
        retr_genres = [x[0] for x in cur.fetchall()] #converting data retrieved(genres) into list form to slice it
        cur.execute("SELECT Actors.ActorName FROM Movie_Actor, Actors WHERE Movie_Actor.ActorID = Actors.ActorID AND Movie_Actor.MovieID = {}".format(MovieID))
        retr_actors = [x[0] for x in cur.fetchall()] #converting data retrieved(actors) into list form to slice it
        cur.execute("SELECT Directors.DirectorName FROM Movie_Director, Directors WHERE Movie_Director.DirectorID = Directors.DirectorID AND Movie_Director.MovieID = {}".format(MovieID))
        retr_directors = [x[0] for x in (cur.fetchall())] #converting data retrieved(directors) into list form to slice it
    except:
        print("Not Found")
        return -1
    finally:
        cur.close()

    #building a movie object with retrieved data and returning it
    return Movie(MovieID, str(retr_movie[1]), str(retr_movie[2]), str(retr_movie[3]), retr_movie[4], (retr_movie[5]), retr_actors, retr_directors, retr_genres)


def filtersort(opt_filter, choice, opt_sortby, asc):
    '''
    function to build query for data retrieval 
    returns list of movie id's with given sort-filter parameters
    opt_filter is the filter option(must be a capitalised string that says 'GenreName', 'DirectorName', 'ActorName', 'MovieDate', or 'MovieRating') 
    opt_sortby is the sort option(must be a string that says 'MovieDate', or 'MovieRating')
    asc is the ascending/descending toggle, must be a string that says 'ASC' for ascending or 'DESC' for descending
    choice is the value by which you filter, eg 'Comedy' for genre
    '''
    cur = con.cursor()

    #defining a return function to return a unique list
    def return_lst(lst):
        unique_lst = []
        for i in lst:
            if i not in unique_lst:
                unique_lst.append(i)
        return unique_lst
    
    try:

        if opt_filter == 'Genre': #filter by genre
            #checking if genre is in database
            cur.execute("SELECT GenreName from Genres;")
            Existing_Data = [x[0] for x in list(cur.fetchall())]
            if choice not in Existing_Data:
                raise Exception
            
            cur.execute("SELECT GenreID FROM Genres WHERE GenreName = '{}'".format(choice))
            id = list(cur.fetchone())[0]
            query_string = "SELECT Movies.MovieID FROM Movies, Movie_Genre, Genres WHERE Movies.MovieID = Movie_Genre.MovieID AND Movie_Genre.GenreID = '{}' ORDER BY '{}' '{}';".format(id, opt_sortby, asc)
            cur.execute(query_string)
            lst = [x[0] for x in cur.fetchall()]
            return return_lst(lst)
        
        elif opt_filter == 'Director': #filter by director
            #checking if director is in database
            cur.execute("SELECT DirectorName from Directors;")
            Existing_Data = [x[0] for x in list(cur.fetchall())]
            if choice not in Existing_Data:
                raise Exception
            
            cur.execute("SELECT DirectorID FROM Directors WHERE DirectorName = '{}'".format(choice))
            id = list(cur.fetchone())[0]
            query_string = "SELECT Movies.MovieID FROM Movies, Movie_Director, Directors WHERE Movies.MovieID = Movie_Director.MovieID AND Movie_Director.DirectorID = '{}' ORDER BY '{}' '{}';".format(id, opt_sortby, asc)
            cur.execute(query_string)
            lst = [x[0] for x in cur.fetchall()]
            return return_lst(lst)
        
        elif opt_filter == 'Actor': #filter by actor
            #checking if actor is in database
            cur.execute("SELECT ActorName from Actors;")
            Existing_Data = [x[0] for x in list(cur.fetchall())]
            if choice not in Existing_Data:
                raise Exception
            
            cur.execute("SELECT ActorID FROM Actors WHERE ActorName = '{}'".format(choice))
            id = list(cur.fetchone())[0]
            query_string = "SELECT Movies.MovieID FROM Movies, Movie_Actor, Actors WHERE Movies.MovieID = Movie_Actor.MovieID AND Movie_Actor.ActorID = '{}' ORDER BY '{}' '{}';".format(id, opt_sortby, asc)
            cur.execute(query_string)
            lst = [x[0] for x in cur.fetchall()]
            return return_lst(lst)
        
        elif opt_filter == 'Year': #filter by year
            #checking if year is in database
            cur.execute("SELECT YEAR(MovieDate) from Movies;")
            Existing_Data = [x[0] for x in list(cur.fetchall())]
            if choice not in Existing_Data:
                raise Exception
            
            query_string = "SELECT MovieID FROM Movies WHERE YEAR(MovieDate) = '{}' SORT BY '{}' '{}';".format(choice, "MovieDate", asc)
            cur.execute(query_string)
            lst = [x[0] for x in cur.fetchall()]
            return return_lst(lst)

        elif opt_filter == 'Rating': #filter by rating above a certain value
            #checking if rating is in range
            if choice > 10 or choice < 0:
                raise Exception
            
            query_string = "SELECT MovieID FROM Movies WHERE MovieRating >= '{}' SORT BY '{}' '{}';".format(choice, "MovieRating", asc)
            cur.execute(query_string)
            lst = [x[0] for x in cur.fetchall()]
            return return_lst(lst)
    except:
        print("Not Found")
        return -1
    finally:
        cur.close()

def insert_favourites(Username, MovieName):
    '''function to link a user to their favourite movie'''
    cur = con.cursor()
    #exception handling: if movie is not in database, will print not found and return -1
    try:
        cur.execute("SELECT MovieID FROM Movies WHERE MovieName = '{}'".format(MovieName))
        MovieID = cur.fetchone()[0]
        if MovieID is None:
            raise Exception
        cur.execute("INSERT INTO User_Movie(Username, MovieID) VALUES('{}', {})".format(Username, MovieID))
        con.commit()
    except:
        print("Not Found")
        return -1
    finally:
        cur.close()

class User:
    def __init__(self, username, firstname, lastname, favourites):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.favourites = favourites

def get_userdata(Username):
    '''function to get user data, including username, first name, last name, and favourites in the form of a user object'''
    cur = con.cursor()
    try:
        #getting user data from the user table
        cur.execute("SELECT * FROM Users WHERE Username = '{}'".format(Username))
        UserData = cur.fetchone()
        if UserData is None:
            raise Exception
        #getting favourites from user_movie relationship table
        cur.execute("SELECT MovieID FROM User_Movie WHERE Username = '{}'".format(Username))
        UserMovies = [x[0] for x in cur.fetchall()]
    except:
        print("Not Found")
        return -1
    finally:
        cur.close()

    #returning user object
    return User(Username, UserData[1], UserData[2], UserMovies)

#testing
#movie_data_dump(getMovieID("PK"), getMovieData("PK"))
# print(filtersort("Director", "MovieDate", "ASC"))
# md = build_moviedata_object(206527)
# print(md.id, md.name, md.date, md.directors, md.photo, md.plot, md.rating, md.actors, md.genres)
insert_favourites('ShyNightshade', '3 Idiots')
insert_favourites('ShyNightshade', 'Dangal')
insert_favourites('ShyNightshade', 'Inception')

ud1 = get_userdata('ShyNightshade')
print(ud1.username, ud1.firstname, ud1.lastname, ud1.favourites)

con.close()
