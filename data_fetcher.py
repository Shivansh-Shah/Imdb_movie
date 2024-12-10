import requests
from bs4 import BeautifulSoup
from datascraped import *
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
    if check_in_database(MovieID) == True:
        return
    try:
        # Inserting into the movie table using a parameterized query
        Mov_Dat_DML = '''
        INSERT INTO Movies (MovieID, MovieName, MovieDate, MoviePlot, MoviePhoto, MovieRating) 
        VALUES (%s, %s, %s, %s, %s, %s);
        '''
        cur.execute(Mov_Dat_DML, (
            MovieID,
            data['Title'],
            convert_date_format(data['Released']),
            data['Plot'],
            data['Poster'],
            float(data['imdbRating'])
            ))
            
        # Commit the transaction
        con.commit()

        #inserting into movie-genre relationship table
        Genre_List = data['Genre'].split(", ")
        
        for i in Genre_List:
            GenreID_Query = "SELECT GenreID FROM Genres WHERE GenreName = '{}';".format(i)
            cur.execute(GenreID_Query)
            GenreID = cur.fetchone()[0]
            if GenreID is None:
                raise Exception
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
    except:
        pass
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

def delete_favourites(Username, MovieName):
    '''function to remove a user's favourite movie'''
    cur = con.cursor()
    #exception handling: if movie is not in database, will print not found and return -1
    try:
        cur.execute("SELECT MovieID FROM Movies WHERE MovieName = '{}'".format(MovieName))
        MovieID = cur.fetchone()[0]
        if MovieID is None:
            raise Exception
        cur.execute("DELETE FROM User_Movie WHERE Username = '{}' AND MovieID = {}".format(Username, MovieID))
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
        if UserData == ():
            raise Exception
        #getting favourites from user_movie relationship table
        cur.execute("SELECT MovieID FROM User_Movie WHERE Username = '{}'".format(Username))
        UserMovies = [x[0] for x in cur.fetchall()]
    except Exception:
        print("Not Found")
        return -1
    finally:
        cur.close()

    #returning user object
    return User(Username, UserData[1], UserData[2], UserMovies)

def build_db():
    '''this function can only be called once at the beginning of the program to build the database and then insert the data into the tables'''
    cur = con.cursor()

    movies_list = ["The Shawshank Redemption", "The Godfather", "The Dark Knight", "Pulp Fiction",
    "Forrest Gump", "Inception", "Fight Club", "The Matrix", "Goodfellas", "Se7en",
    "Interstellar", "The Silence of the Lambs", "Schindler's List", "The Green Mile",
    "The Departed", "Gladiator", "Braveheart", "The Prestige", "Titanic",
    "The Wolf of Wall Street", "Saving Private Ryan", "Django Unchained", "The Avengers",
    "Avatar", "Parasite", "Joker", "The Lion King", "Toy Story", "Finding Nemo",
    "WALL-E", "Up", "Frozen", "Shrek", "Moana", "Coco", "Beauty and the Beast",
    "Aladdin", "Mulan", "The Little Mermaid", "Tangled", "Ratatouille", "Zootopia",
    "Big Hero 6", "The Incredibles", "Monsters, Inc.", "Inside Out", "Brave", "Soul",
    "Onward", "Cars", "A Bug's Life", "Antz", "Kung Fu Panda", "How to Train Your Dragon",
    "The Lego Movie", "Spider-Man: Into the Spider-Verse", "The Secret Life of Pets",
    "Sing", "Despicable Me", "Minions", "Ice Age", "Madagascar", "Happy Feet",
    "Cloudy with a Chance of Meatballs", "Megamind", "Bolt", "Hotel Transylvania",
    "The Croods", "The Boss Baby", "Rio", "Horton Hears a Who!", "Epic", "Trolls",
    "Home", "Ferdinand", "Spies in Disguise", "Wonder Woman", "Black Panther", "Iron Man",
    "Thor", "Doctor Strange", "Guardians of the Galaxy", "Ant-Man", "Her",
    "Eternal Sunshine of the Spotless Mind", "La La Land", "Whiplash", "The Grand Budapest Hotel",
    "The Royal Tenenbaums", "Moonrise Kingdom", "Fantastic Mr. Fox", "Isle of Dogs",
    "The French Dispatch", "The Shape of Water", "Pan's Labyrinth", "Crimson Peak",
    "Hellboy", "Pacific Rim", "Edge of Tomorrow", "Oblivion", "Elysium", "District 9",
    "Chappie", "Moon", "Ex Machina", "Annihilation", "Arrival", "Blade Runner",
    "Blade Runner 2049", "Dune", "The Martian", "Gravity", "Ad Astra", "Contact",
    "Solaris", "A Space Odyssey", "The Terminator", "RoboCop", "Total Recall",
    "Starship Troopers", "Predator", "Alien", "The Thing", "They Live",
    "Escape from New York", "Big Trouble in Little China", "Christine", "Carrie",
    "Misery", "The Shining", "Doctor Sleep", "IT", "Stand by Me",
    "The Mist", "Pet Sematary", "Cujo", "The Amityville Horror", "Poltergeist",
    "The Conjuring", "The Conjuring 2", "Annabelle", "Insidious", "Sinister",
    "The Purge", "Saw", "Hostel", "Final Destination", "A Nightmare on Elm Street",
    "Us", "Get Out", "The Babadook", "The Witch", "Hereditary", "Midsommar",
    "The Lighthouse", "The Invisible Man", "Hush", "Bird Box", "A Quiet Place",
    "The Others", "Donnie Darko", "The Sixth Sense", "Signs", "Unbreakable",
    "Split", "Glass", "Old", "Looper", "Knives Out", "Murder on the Orient Express",
    "Clue", "The Hateful Eight", "Reservoir Dogs", "The Big Lebowski", "Fargo",
    "No Country for Old Men", "There Will Be Blood", "The Social Network",
    "The Imitation Game", "Bohemian Rhapsody", "Rocketman", "The Greatest Showman",
    "Les Misérables", "Chicago", "Moulin Rouge!", "West Side Story", "Amadeus",
    "Ray", "Walk the Line", "La Vie en Rose", "The Pianist", "Whale Rider",
    "Slumdog Millionaire", "Life of Pi", "The Revenant", "Cast Away", "The Impossible",
    "127 Hours", "Apollo 13", "First Man", "Hidden Figures", "The Theory of Everything",
    "A Beautiful Mind", "Good Will Hunting", "Dead Poets Society", "The Pursuit of Happyness",
    "Patch Adams", "One Flew Over the Cuckoo's Nest", "Rain Man", "The Terminal",
    "The Bucket List", "The Intouchables", "The Best Exotic Marigold Hotel", "Philomena",
    "The King's Speech", "Elizabeth", "Marie Antoinette", "The Duchess", "The Favourite",
    "Pride & Prejudice", "Emma", "Sense and Sensibility", "Little Women",
    "The Age of Innocence", "Atonement", "Anna Karenina", "Jane Eyre", "Wuthering Heights",
    "Rebecca", "Gone with the Wind", "The Notebook", "The Time Traveler's Wife",
    "Me Before You", "P.S. I Love You", "The Vow", "Love, Rosie", "Letters to Juliet",
    "Midnight in Paris", "Amélie", "Chocolat", "Notting Hill", "Four Weddings and a Funeral",
    "Love Actually", "When Harry Met Sally...", "Sleepless in Seattle", "You've Got Mail",
    "Pretty Woman", "Dirty Dancing", "Ghost", "Jerry Maguire", "As Good as It Gets",
    "The Holiday", "The Family Stone", "Crazy, Stupid, Love.", "Friends with Benefits",
    "No Strings Attached", "The Proposal", "27 Dresses", "Bride Wars", "The Wedding Planner",
    "Runaway Bride", "My Best Friend's Wedding", "Sweet Home Alabama", "Legally Blonde",
    "Clueless", "Mean Girls", "Easy A", "She's the Man", "10 Things I Hate About You",
    "The Princess Diaries", "The Lizzie McGuire Movie", "A Cinderella Story",
    "The Sisterhood of the Traveling Pants", "Ella Enchanted", "The Parent Trap",
    "Freaky Friday", "The Princess and the Frog", "Enchanted", "Pocahontas", "Hercules",
    "Tarzan", "The Hunchback of Notre Dame", "The Rescuers", "The Aristocats",
    "Robin Hood", "The Jungle Book", "Sleeping Beauty", "Peter Pan", "Alice in Wonderland",
    "Cinderella", "Snow White and the Seven Dwarfs", "Pinocchio", "Dumbo", "Bambi",
    "The Fox and the Hound", "The Black Cauldron", "Oliver & Company", "The Great Mouse Detective",
    "The Secret of NIMH", "An American Tail", "The Land Before Time", "All Dogs Go to Heaven",
    "Balto", "Spirit: Stallion of the Cimarron", "The Road to El Dorado", "Sinbad: Legend of the Seven Seas",
    "The Prince of Egypt", "Joseph: King of Dreams", "Chicken Run", "Wallace & Gromit: The Curse of the Were-Rabbit",
    "Shaun the Sheep Movie", "Arthur Christmas", "Flushed Away", "Open Season", "Surf's Up",
    "The Angry Birds Movie", "The Emoji Movie", "The SpongeBob SquarePants Movie",
    "Sponge on the Run", "The Lego Batman Movie", "The Lego Ninjago Movie",
    "Frozen II", "Ralph Breaks the Internet", "Wreck-It Ralph", "Trolls World Tour", "Sing 2",
    "The Croods: A New Age", "The Lego Movie 2", "The Angry Birds Movie 2", "Monsters University",
    "Lagaan", "Dilwale Dulhania Le Jayenge", "3 Idiots", "Sholay", "Kabhi Khushi Kabhie Gham",
    "Zindagi Na Milegi Dobara", "Jab We Met", "Chennai Express", "Dil Chahta Hai", "Mughal-e-Azam",
    "Dangal", "PK", "Bajirao Mastani", "Barfi!", "Tanu Weds Manu", "Kabir Singh", "Andhadhun",
    "Article 15", "Drishyam", "Gully Boy", "Queen", "Taare Zameen Par", "Rang De Basanti",
    "Swades", "Jodha Akbar", "Kahaani", "Lage Raho Munna Bhai", "My Name is Khan", "Dhoom",
    "Hera Pheri", "Bhool Bhulaiyaa", "Chupke Chupke", "Dil Se", "Wake Up Sid", "Kai Po Che",
    "Pyaasa", "Silsila", "Bhaag Milkha Bhaag", "Love Aaj Kal", "Vicky Donor", "Tumhari Sulu",
    "Chhichhore", "Haider", "Piku", "Padman", "Raazi", "The Lunchbox", "Tumbbad", "Rock On!!",
    "Goliyon Ki Raasleela Ram-Leela", "Judwaa 2", "Baahubali: The Beginning", "Baahubali: The Conclusion",
    "Krrish", "Sultan", "Singham", "Golmaal", "Kick", "Badhaai Ho", "Sonu Ke Titu Ki Sweety",
    "De De Pyaar De", "Ludo", "Mimi", "Bajrangi Bhaijaan", "Kesari", "Maine Pyar Kiya"
    ]

    for i in movies_list: #commits data of top 250 movies onto local system
        movie_data_dump(getMovieID(i), getMovieData(i))
    
    for mov in movies_list: #downloads all movie posters onto local system
        try:
            savePoster(mov)
        except:
            continue

    con.commit()
    cur.close()

def check_in_database(MovieID):
    '''will return True if the movie is in the database, False otherwise'''
    cur = con.cursor()
    cur.execute("SELECT MovieID FROM Movies")
    existing = [x[0] for x in cur.fetchall()]
    cur.close()
    if MovieID in existing:
        return True
    return False

con.close()
