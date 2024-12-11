import requests

from bs4 import BeautifulSoup
import  download

def getMovieID(movieName):
        url="https://www.ratingraph.com/search-results/"

        for i in movieName.split(" "):

            url = url + i + "%20"
        movie = requests.get(url)

        try:
            if(movie.status_code == 200):
                soup = BeautifulSoup(movie.text, 'html.parser' )
                data = soup.find_all( 'div' , class_ = 'titles results' )
                # return((data[0].find_all('a')[0].get('href') ).split('-')[-1][0:-1] )
                return (((data[0].find_all('a')[0].get('href')).split('-')[-1][0:-1]))
        except:
                print("Movie not availabe")


def getGraphData(movieID):

    url = "https://www.ratingraph.com/movie-history/"+movieID+'/'

    response = requests.get(url)
    try:
         if(response.status_code == 200):

            data = response.json()
            return( data[1]['data'] )

    except:
        print("Movie not available")


def getMovieData(movieName):

    url = "https://www.omdbapi.com/?t="

    for i in movieName.split():
        url = url + i + "+"
    try:
        url = url[:len(url)-1] + "&plot=full&apikey=c2403270"
        response=requests.get(url)

        if response.status_code == 200:

            data = response.json()
            return(data)

        else:
            return -1
    except:
            print("Movie not available")

def savePoster(MovieName):

    movieID=getMovieID((MovieName))

    data = getMovieData(MovieName)
    posterlink = data['Poster']
    download.download_image(posterlink,f"posters/{movieID}.png")
    print(movieID)

movies = [
    "The Shawshank Redemption", "The Godfather", "The Dark Knight", "Pulp Fiction",
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
    "Misery", "The Shining", "Doctor Sleep", "IT", "The Green Mile", "Stand by Me",
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
    "127 Hours", "Gravity", "The Martian", "Interstellar", "Apollo 13", "First Man",
    "Hidden Figures", "The Theory of Everything", "A Beautiful Mind", "Good Will Hunting",
    "Dead Poets Society", "The Pursuit of Happyness", "Patch Adams", "One Flew Over the Cuckoo's Nest",
    "Rain Man", "Forrest Gump", "The Terminal", "The Bucket List", "The Intouchables",
    "The Best Exotic Marigold Hotel", "Philomena", "The King's Speech", "Elizabeth",
    "Marie Antoinette", "The Duchess", "The Favourite", "Pride & Prejudice", "Emma",
    "Sense and Sensibility", "Little Women", "The Age of Innocence", "Atonement",
    "Anna Karenina", "Jane Eyre", "Wuthering Heights", "Rebecca", "Gone with the Wind",
    "The Notebook", "The Time Traveler's Wife", "Me Before You", "P.S. I Love You",
    "The Vow", "Love, Rosie", "Letters to Juliet", "Midnight in Paris", "Amélie",
    "Chocolat", "Notting Hill", "Four Weddings and a Funeral", "Love Actually",
    "When Harry Met Sally...", "Sleepless in Seattle", "You've Got Mail", "Pretty Woman",
    "Dirty Dancing", "Ghost", "Jerry Maguire", "As Good as It Gets", "The Holiday",
    "The Family Stone", "Crazy, Stupid, Love.", "Friends with Benefits",
    "No Strings Attached", "The Proposal", "27 Dresses", "Bride Wars", "The Wedding Planner",
    "Runaway Bride", "My Best Friend's Wedding", "Sweet Home Alabama", "Legally Blonde",
    "Clueless", "Mean Girls", "Easy A", "She's the Man", "10 Things I Hate About You",
    "The Princess Diaries", "The Lizzie McGuire Movie", "A Cinderella Story",
    "The Sisterhood of the Traveling Pants", "Ella Enchanted", "The Parent Trap",
    "Freaky Friday", "The Princess and the Frog", "Enchanted", "Frozen", "Tangled",
    "Brave", "Moana", "Coco", "Onward", "Ratatouille", "WALL-E", "Up", "Finding Nemo",
    "The Lion King", "Aladdin", "Beauty and the Beast", "The Little Mermaid", "Mulan",
    "Pocahontas", "Hercules", "Tarzan", "The Hunchback of Notre Dame", "The Rescuers",
    "The Aristocats", "Robin Hood", "The Jungle Book", "Sleeping Beauty", "Peter Pan",
    "Alice in Wonderland", "Cinderella", "Snow White and the Seven Dwarfs", "Pinocchio",
    "Dumbo", "Bambi", "The Fox and the Hound", "The Black Cauldron", "Oliver & Company",
    "The Great Mouse Detective", "The Secret of NIMH", "An American Tail",
    "The Land Before Time", "All Dogs Go to Heaven", "Balto", "Spirit: Stallion of the Cimarron",
    "The Road to El Dorado", "Sinbad: Legend of the Seven Seas", "The Prince of Egypt",
    "Joseph: King of Dreams", "Chicken Run", "Wallace & Gromit: The Curse of the Were-Rabbit",
    "Shaun the Sheep Movie", "Arthur Christmas", "Flushed Away", "Open Season", "Surf's Up",
    "The Angry Birds Movie", "The Emoji Movie", "The SpongeBob SquarePants Movie",
    "Sponge on the Run", "The Lego Movie", "The Lego Batman Movie", "The Lego Ninjago Movie",
    "Big Hero 6", "Zootopia", "Bolt", "Frozen", "Frozen II", "Ralph Breaks the Internet",
    "Wreck-It Ralph", "Trolls", "Trolls World Tour", "The Secret Life of Pets",
    "Despicable Me", "Despicable Me 2", "Despicable Me 3", "Minions", "Sing",
    "Sing 2", "The Boss Baby", "The Croods", "The Croods: A New Age", "Ice Age",
    "Madagascar", "Shrek", "Kung Fu Panda", "How to Train Your Dragon",
    "The Lego Movie 2", "The Angry Birds Movie 2", "Cloudy with a Chance of Meatballs",
    "Hotel Transylvania", "Monsters, Inc.", "Monsters University", "Inside Out",
    "Brave", "Onward", "Soul", "Lagaan", "Dilwale Dulhania Le Jayenge", "3 Idiots", "Sholay", "Kabhi Khushi Kabhie Gham",
    "Zindagi Na Milegi Dobara", "Jab We Met", "Chennai Express", "Dil Chahta Hai", "Mughal-e-Azam",
    "Dangal", "PK", "Bajirao Mastani", "Barfi!", "Tanu Weds Manu", "Kabir Singh", "Andhadhun",
    "Article 15", "Drishyam", "Gully Boy", "Queen", "Taare Zameen Par", "Rang De Basanti",
    "Swades", "Jodha Akbar", "Kahaani", "Lage Raho Munna Bhai", "My Name is Khan", "Dhoom",
    "Kabir Singh", "Singh is Kinng", "Koi Mil Gaya", "Maine Pyar Kiya", "Hera Pheri", "Bhool Bhulaiyaa",
    "Chupke Chupke", "Dil Se", "Rang De Basanti", "Barfi", "Wake Up Sid", "Kai Po Che", "Pyaasa",
    "Silsila", "Shakti", "Jab Tak Hai Jaan", "Kabir Singh", "Zindagi Na Milegi Dobara", "Bhaag Milkha Bhaag",
    "Love Aaj Kal", "Vicky Donor", "Tumhari Sulu", "Chhichhore", "Haider", "Tanu Weds Manu",
    "Piku", "Padman", "Rustom", "Mardaani", "Kahaani", "Queen", "The Lunchbox", "Barfi", "Raazi",
    "The Dirty Picture", "Tanu Weds Manu Returns", "Rock On!!", "Dil Dhadakne Do", "Jolly LLB",
    "Pyaar Ka Punchnama", "Bajirao Mastani", "Dabangg", "Dhoom 3", "Goliyon Ki Raasleela Ram-Leela",
    "Judwaa 2", "Baahubali: The Beginning", "Baahubali: The Conclusion", "Krrish", "Sultan",
    "Singham", "Golmaal", "Race 3", "Kick", "Krishh", "Makkhi", "Chhota Bheem", "Meri Pyaari Bindu",
    "Badhaai Ho", "Sonu Ke Titu Ki Sweety", "De De Pyaar De", "Badlapur", "Piku", "Chupke Chupke",
    "Pyaasa", "Veer-Zaara", "Bhaag Milkha Bhaag", "Bajirao Mastani", "Prem Ratan Dhan Payo",
    "Tanu Weds Manu", "Chandni Chowk to China", "Pardes", "Don", "Kuch Kuch Hota Hai", "Dilwale",
    "Kabhi Alvida Naa Kehna", "Om Shanti Om", "Tees Maar Khan", "Rab Ne Bana Di Jodi", "Raees",
    "Housefull", "Jab Tak Hai Jaan", "Mujhse Dosti Karoge", "Mohenjo Daro", "Fan", "Ae Dil Hai Mushkil",
    "Baazigar", "Kal Ho Naa Ho", "Kuch Kuch Hota Hai", "Kabhi Khushi Kabhie Gham", "Dostana", "Jab We Met",
    "Dilwale Dulhania Le Jayenge", "Wake Up Sid", "Kahaani", "Piku", "Chhichhore", "The Lunchbox",
    "Zindagi Na Milegi Dobara", "Margarita with a Straw", "Vicky Donor", "Maqbool", "Tumbbad", "Tanu Weds Manu",
    "The Lunchbox", "Lagaan", "Rang De Basanti", "Swades", "Chakde! India", "Bhaag Milkha Bhaag",
    "Chupke Chupke", "Hera Pheri", "Bajirao Mastani", "Dil Se", "Taare Zameen Par", "Barfi!", "Sholay",
    "Shree 420", "Chupke Chupke", "Love Aaj Kal", "Pyaasa", "Rang De Basanti", "Dil Dhadakne Do",
    "Shubha Mangal Saavdhan", "Tanu Weds Manu Returns", "Tumhari Sulu", "Lage Raho Munna Bhai", "The Dirty Picture",
    "Bhaag Milkha Bhaag", "Vicky Donor", "Barfi", "Chupke Chupke", "Kabir Singh", "Dilwale Dulhania Le Jayenge",
    "Prem Ratan Dhan Payo", "Kal Ho Naa Ho", "Jab We Met", "Sultan", "Padmaavat", "The Lunchbox",
    "Dum Laga Ke Haisha", "Bajirao Mastani", "Jab Tak Hai Jaan", "Gully Boy", "Chhichhore",
    "Haider", "Zindagi Na Milegi Dobara", "Goliyon Ki Raasleela Ram-Leela", "Drishyam", "Aashiqui 2",
    "Dabangg", "Sultan", "Raazi", "Tanu Weds Manu", "Chandni Chowk to China", "Madhur Bhandarkar Films",
    "Rock On", "Heropanti", "Ram Gali", "Hichki", "Love Aj Kal"]
# movieName = input()
# movieID = getMovieID(movieName)
# print(movieID)
# GraphData = getGraphData(movieID)
# movieData = getMovieData(movieName)

#
# for mov in movies:
#     # try:
    #     savePoster(mov)
    # except:
#     #     continue
# print(getMovieID("Singham"))
