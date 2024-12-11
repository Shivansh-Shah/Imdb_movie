# Cinephile_App 
## Contributers: 
- ShaiviNandi( BT2024003) : Worked on backend, particularly with MySQL syntax and it's
                              integration with Python. Built the data_fetcher.py module.
- ShivanshShah( BT2024243) :

- AmanKumarLahoti( BT2024123) :

- PSaratCBharadwaj( BT2024179): Actively contributed to the development and debugging of visualisation.py and other project files, ensuring error resolution

- Puttaraja Beedinalamath ( IMT2024091): 
## Overview

The **Cinephile_App** serves as an interactive movie database and visualization platform. It features data on movies present  in our database  using statistics such as *average ratings over time* and *total votes trends*. The visualization is powered by **Custom Tkinter**, and a **Matplotlib**.

---

## Features
-   ** Web Scraping** :

     Data scraped from the 2 websites are our source for our App's database and Visualisation
    
-   ** Database management** :

   The SQL database consists of 2 main tables: *Users* and *Movies*, along with a number of
  relationship tables which holds information related to our app.
  
   Stores information related to movies and the application' users.
- ** Visualisation ** : Visualisation.py displays two graphs in a separate window ( side by side frames). 

## Modules used: 
- **Tkinter**: GUI framework.
- **CustomTkinter**: Enhanced `tkinter` features.
- **Matplotlib**: For graph plotting.
- **MySQL Database**: Database handling for storing movies, actors, and user preferences.
- **Datetime & Numpy**: For datetime conversions and in visualisation.py

## Setup Instructions

To run this project locally, follow these steps
```
### 1. Install required software
install MySQLInstaller from https://dev.mysql.com/downloads/installer/ , and then run it, making sure to install both the client and server packages. 
 
### 2. Install Required Packages
Install dependencies with `pip`:
```bash
pip install requests
pip install beautifulsoup4
pip install pillow
pip install mysql-connector-python
pip install customtkinter matplotlib numpy

### 3. Setting up the database
1. Open your database client ( MySQL )
2. Run the script provided in MySQLSyntax.sql to build the database. 

### 4. Configure Database Connection (if needed)
Database connection settings will need to be set up- ensure database credentials are configured properly.

### 5. Run the Visualization Application
Launch the GUI application via:

python main.py
```
## Web scraping ( datascraped.py) 

- Source for Database management ( Omdbapi - website )
   https://www.omdbapi.com/

- Source for Visualisation ( ratingraph - website )
    https://www.ratingraph.com/

## Database Management ( data_fetcher.py and SQLSyntax.sql) 

- Has Two classes:
  **User** and **Movie**
 
- User class stores username and list of favourite movies of each user.
- Movie class stores all the information scraped from datascraped into the database system.

- Movie Table:
  The table stores information of all the movies in the database and is linked to the following relationship:
  Actors ( Movie_Actor )
  Directors ( Movie_Director )
  Genres ( Movie_Genre )

  each of these(Actors, Directors, and Genres) are also a table of their own containing all data about each actor, director and genre respectively. The data for actors and directors is scraped, and the data for genres is hardcoded in the MYSQLSyntax.sql file.

- User Table:
 Stores username and password for login, and is also linked to favourites ( via Vser_Movie ).

These are operated upon by the functions defined in the data_fetcher.py module:
- movie_data_dump(MovieID, MovieData) : this takes scraped data from datascraped.py about a particular movie and sorts this data into the database. 
- build_moviedata_object(MovieID) : this retrieves data about a particular movie from the database and returns it in the form of a movie object
- filtersort(opt_filter, choice, opt_sortby, asc) : returns list of movie id's with given sort-filter parameters
    opt_filter is the filter option(must be a capitalised string that says 'GenreName', 'DirectorName', 'ActorName', 'MovieDate', or 'MovieRating') 
    opt_sortby is the sort option(must be a string that says 'MovieDate', or 'MovieRating')
    asc is the ascending/descending toggle, must be a string that says 'ASC' for ascending or 'DESC' for descending
    choice is the value by which you filter, eg 'Comedy' for genre.
- insert_favourites(Username, MovieName) : this links a user to their favourite movie in the user_movie table
- delete_favourites(Username, MovieName) : this delinks a user from their favourite movie by deleting the record from the user_movie table
- get_userdata(Username) : this retrieves the user's favourite movies
- build_db(): this function can only be called once at the beginning of the program to build the database and then insert the data into the tables
- 
## Visualisation.py
- Has classes Visualiser1 and Visualiser2. 
- Visualiser1: This class has an attribute graphdata, which is fetched from datascraped.py
  It makes use of graphdata and returns a figure ( average ratings graph )
   
- Visualiser2: This class is similar to Visualiser1, except it returns another figure
  ( total votes graph ).

### Screenshot Example
 Yet to be updated.

 ## 
