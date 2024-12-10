# Cinephile_App 
## Introduction: 

 

## Overview

The **Cinephile_App** serves as an interactive movie database and visualization platform. It features data on movies present  in our database  using statistics such as *average ratings over time* and *total votes trends*. The visualization is powered by **Custom Tkinter**, and a **Matplotlib**.

---

## Features
- ** Database management** :

   The SQL database consists of 2 main tables: *Users* and *Movies*, along with a number of
  relationship tables which holds information related to our app.
  
   Stores information related to movies and the application' users.
- ** Visualisation ** : Visualisation.py displays two graphs in a separate window ( side by side ) 

## Modules used: 
- **Tkinter**: GUI framework.
- **CustomTkinter**: Enhanced `tkinter` features.
- **Matplotlib**: For graph plotting.
- **SQLite/MySQL Database**: Database handling for storing movies, actors, and user preferences.
- **Datetime & Numpy**: For datetime conversions and in visualisation.py

## Setup Instructions

To run this project locally, follow these steps
```

### 2. Install Required Packages
Install dependencies with `pip`:
```bash
pip install tkinter customtkinter matplotlib numpy

### 3. Set Up the Database Schema
1. Open your database client (MySQL, SQLite, etc.).
2. Run the schema script provided in `database/schema.sql` to create database tables.

### 4. Configure Database Connection (if needed)
Database connection settings might need to be set up within `datascraped.py`. Ensure database credentials are configured properly.

### 5. Run the Visualization Application
Launch the GUI application via:

python main.py
```


## Database Management ( data_fetcher.py and sql_syntax.py) 

- Has Two classes:
  **User** and **Movie**
 
- User class stores username and list of favourite movies of each user.
- Movie class stores all the information scraped from datascraped into the database system.

- Movie Table:
  The table stores information of all the movies in the database and is linked to the following:
  Actors ( Movie_Actor )
  Directors ( Movie_Director )
  Genres ( Movie_Genre )

- User Table:
 Stores username and password for login, and is also linked to favourites ( via Vser_Movie ).
## Visualisation.py
- Has classes Visualisation1 and Visualisation2. 
- Visualiser1: This class has an attribute graphdata, which is fetched from datascraped.py
  It makes use of graphdata and returns a figure ( average ratings graph )
   
- Visualiser2: This class is similar to Visualiser1, except it returns another figure
  ( total votes graph ).

### Screenshot Example
 Yet to be updated.

 ## 
