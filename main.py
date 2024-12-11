import customtkinter as ctk
from tkinter import messagebox,Canvas
import time
import mysql.connector
import random
from datetime import datetime
import string
from PIL import Image,ImageTk,ImageOps,ImageDraw
from sqlalchemy.sql.traversals import compare
from data_fetcher import get_userdata, build_moviedata_object, insert_favourites, delete_favourites, Movie , UserClass
import datascraped
from trendAnalyzer import Visualiser1 , Visualiser2

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datascraped import getGraphData,getMovieData,getMovieID

# Function to connect to MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="shivansh6165",
        database="Cinephile_App"
    )

user_name=""


def login_page():
    global user_name
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    def login():
        user_id = user_id_entry.get()
        password = password_entry.get()
        verify_credentials(user_id, password)


    def verify_credentials(user_id, password):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user_id, password))
        user = cursor.fetchone()
        db.close()

        if user:
            global user_name
            user_name=user
            messagebox.showinfo("Login", "Login Successful")
            app.destroy()
            dashboard()
        else:
            messagebox.showerror("Login", "Invalid User ID or Password")


    def sign_up():
        login_frame.grid_forget()
        sign_up_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        sign_up_button.grid_forget()


    def submit_sign_up():
        username = sign_up_username_entry.get()
        password = sign_up_password_entry.get()
        confirm_password = sign_up_confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror("Sign Up", "Passwords do not match!")
        else:

            db = connect_db()
            cursor = db.cursor()

            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                db.commit()
                messagebox.showinfo("Sign Up", "Sign-Up Successful!")
            except mysql.connector.IntegrityError:
                messagebox.showerror("Sign Up", "Username already exists!")

            db.close()
            sign_up_frame.grid_forget()
            app.destroy()
            login_page()


    def forget_password():
        login_frame.grid_forget()
        forget_password_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def goback():
        app.destroy()
        login_page()

    def reset_password():
        username = forget_username_entry.get()

        if not username:
            messagebox.showerror("Error", "Username cannot be empty!")
            return

        # Generate a new random password
        new_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

        # Update password in MySQL database
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            messagebox.showerror("Error", "Username does not exist!")
            db.close()
            return

        try:
            cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
            db.commit()
            messagebox.showinfo("Password Reset", f"Your new password is: {new_password}")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")
        finally:
            db.close()
        app.destroy()



    app = ctk.CTk()
    app.title("Cinephile App Login")
    app.geometry("600x320")

    image_path = "-logo.png"
    pil_image = Image.open(image_path)

    pil_image = pil_image.resize((300,300))

    image = ImageTk.PhotoImage(pil_image)

    main_frame = ctk.CTkFrame(app)
    main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


    image_label = ctk.CTkLabel(main_frame, image=image,text='')
    image_label.grid(row=0, column=0, padx=(0, 20), pady=20)

    login_frame = ctk.CTkFrame(app)
    login_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")


    user_id_label = ctk.CTkLabel(login_frame, text="USER ID", font=ctk.CTkFont(size=14))
    user_id_label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")
    user_id_entry = ctk.CTkEntry(login_frame, placeholder_text="Enter your User ID")
    user_id_entry.grid(row=0, column=1, padx=10, pady=(20, 10))


    password_label = ctk.CTkLabel(login_frame, text="PASSWORD", font=ctk.CTkFont(size=14))
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    password_entry = ctk.CTkEntry(login_frame, placeholder_text="Enter your Password", show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)


    login_button = ctk.CTkButton(login_frame, text="LOGIN", command=login)
    login_button.grid(row=2, column=0, columnspan=2, pady=20)


    sign_up_label = ctk.CTkLabel(login_frame, text="New User?")
    sign_up_label.grid(row=3, column=0, pady=(10, 5), sticky="e")
    sign_up_button = ctk.CTkButton(login_frame, text="SIGN UP", command=sign_up, width=100)
    sign_up_button.grid(row=3, column=1, pady=(10, 5), sticky="w")


    forget_password_button = ctk.CTkButton(login_frame, text="Reset Password", command=forget_password)
    forget_password_button.grid(row=4, column=0, columnspan=2, pady=10)


    sign_up_frame = ctk.CTkFrame(app)


    sign_up_username_label = ctk.CTkLabel(sign_up_frame, text="Username", font=ctk.CTkFont(size=14))
    sign_up_username_label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")
    sign_up_username_entry = ctk.CTkEntry(sign_up_frame, placeholder_text="Choose a Username")
    sign_up_username_entry.grid(row=0, column=1, padx=10, pady=(20, 10))

    sign_up_password_label = ctk.CTkLabel(sign_up_frame, text="Password", font=ctk.CTkFont(size=14))
    sign_up_password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    sign_up_password_entry = ctk.CTkEntry(sign_up_frame, placeholder_text="Choose a Password", show="*")
    sign_up_password_entry.grid(row=1, column=1, padx=10, pady=10)

    sign_up_confirm_password_label = ctk.CTkLabel(sign_up_frame, text="Confirm Password", font=ctk.CTkFont(size=14))
    sign_up_confirm_password_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    sign_up_confirm_password_entry = ctk.CTkEntry(sign_up_frame, placeholder_text="Confirm Password", show="*")
    sign_up_confirm_password_entry.grid(row=2, column=1, padx=10, pady=10)


    sign_up_submit_button = ctk.CTkButton(sign_up_frame, text="SUBMIT", command=submit_sign_up)
    goback_button = ctk.CTkButton(sign_up_frame, text="Go Back", command=goback)
    sign_up_submit_button.grid(row=3, column=0, columnspan=2, pady=(10, 20))
    goback_button.grid(row=4, column=0, columnspan=2, pady=(10, 20))


    forget_password_frame = ctk.CTkFrame(app)


    forget_username_label = ctk.CTkLabel(forget_password_frame, text="Username", font=ctk.CTkFont(size=14))
    forget_username_label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")
    forget_username_entry = ctk.CTkEntry(forget_password_frame, placeholder_text="Enter your Username")
    forget_username_entry.grid(row=0, column=1, padx=10, pady=(20, 10))


    reset_password_button = ctk.CTkButton(forget_password_frame, text="RESET PASSWORD", command=reset_password)

    goBack_button = ctk.CTkButton(forget_password_frame, text="Go Back", command=goback)
    reset_password_button.grid(row=1, column=0, columnspan=2, pady=(10, 20))
    goBack_button.grid(row=2, column=0, columnspan=2, pady=(10, 20))


    app.mainloop()

















def dashboard():

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")


    app = ctk.CTk()
    app.title("Movie Dashboard")
    app.geometry("1280x720")
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)

    def create_movie_card(parent, movie):
        card = ctk.CTkFrame(parent, width=180, height=280, corner_radius=10)
        card.grid_propagate(False)


        try:

            poster_path = f"posters/{movie['id']}.png"
            img = Image.open(poster_path).resize((170, 220), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            #
            def open_movie_page(moviename):
                app.destroy()
                movie_page(moviename)


            poster_button = ctk.CTkButton(
                card,
                image=photo,

                command=lambda: open_movie_page(movie['title']),
                fg_color="transparent",
                 # hover_color="#2A2A2A",
                text='',
                hover_color="#787777"
            )
            poster_button.image = photo
            poster_button.grid(row=0, column=0, padx=5, pady=5)

        except Exception as e:
            print(f"Error loading image for {movie['title']}: {e}")
            fallback_label = ctk.CTkLabel(card, text="No Image", fg_color="gray")
            fallback_label.grid(row=0, column=0, padx=5, pady=5)


        title_label = ctk.CTkLabel(
            card,
            text=movie.get("title", "Unknown"),
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=170,
            anchor="center",
        )
        title_label.grid(row=1, column=0, pady=5)

        return card




    def create_movie_section(parent, section_title, movies):

        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", padx=10, pady=20)
        title_label = ctk.CTkLabel(section_frame, text=section_title, font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(anchor="w", padx=450, pady=10)


        canvas_frame = ctk.CTkFrame(section_frame)
        canvas_frame.pack(fill="x")

        canvas = ctk.CTkCanvas(canvas_frame, bg="#2A2A2A", height=300, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scroll_x = ctk.CTkScrollbar(section_frame, orientation="horizontal", command=canvas.xview)
        scroll_x.pack(side="bottom", fill="x")
        canvas.configure(xscrollcommand=scroll_x.set)

        container = ctk.CTkFrame(canvas, fg_color="transparent")
        canvas.create_window((0, 0), window=container, anchor="nw")


        for idx, movie in enumerate(movies):
            card = create_movie_card(container, movie)
            card.grid(row=0, column=idx, padx=20, pady=10)


        container.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    sidebar = ctk.CTkFrame(app, width=250, fg_color="#1A1A1A")
    sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

    logo_label = ctk.CTkLabel(sidebar, text="Cinephiile", font=ctk.CTkFont(size=18, weight="bold"))
    logo_label.pack(pady=(10, 20))


    def home():
        app.destroy()
        dashboard()


    home_button = ctk.CTkButton(
        sidebar,
        text="Home",
        font=ctk.CTkFont(size=14, weight="bold"),
        command=home,
        fg_color="#FFA500",
        text_color="black",
        hover_color="#FFB84D",
    )
    home_button.pack(fill="x", pady=10)



    def search_movi():
        app.destroy()
        search_movies()

    searchmovie_button = ctk.CTkButton(
    sidebar,
    text="Search Movies",
    font=ctk.CTkFont(size=14, weight="bold"),
    command=search_movi ,
    fg_color="#FFA500",
    text_color="black",
    hover_color="#FFB84D",
)
    searchmovie_button.pack(fill="x", pady=20)

    def fav():
        global user_name
        print(user_name)
        app.destroy()
        favourites(user_name)

    favourites_button = ctk.CTkButton(
        sidebar,
        text="Favourites",
        font=ctk.CTkFont(size=14, weight="bold"),
        command=fav,
        fg_color="#FFA500",
        text_color="black",
        hover_color="#FFB84D",
    )
    favourites_button.pack(fill="x", pady=20)

    def comparison():
        app.destroy()
        movie_comp()

    compare_button = ctk.CTkButton(
        sidebar,
        text="Compare",
        font=ctk.CTkFont(size=14, weight="bold"),
        command=comparison,
        fg_color="#FFA500",
        text_color="black",
        hover_color="#FFB84D",
    )
    compare_button.pack(fill="x", pady=20)



    report_button = ctk.CTkButton(
        sidebar,
        text="Report",
        font=ctk.CTkFont(size=14, weight="bold"),
        command=lambda:reportGeneratorPage(),
        fg_color="#FFA500",
        text_color="black",
        hover_color="#FFB84D",
    )
    report_button.pack(fill="x", pady=20)



    def logout():
        app.destroy()
        login_page()

    logout_button = ctk.CTkButton(
        sidebar,
        text="Logout",
        font=ctk.CTkFont(size=14, weight="bold"),
        command=logout,
        fg_color="#FFA500",
        text_color="black",
        hover_color="#FFB84D",
    )
    logout_button.pack(fill="x", pady=20)


    content_frame = ctk.CTkFrame(app, fg_color="transparent")
    content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    # Create a canvas for vertical scrolling
    canvas = ctk.CTkCanvas(content_frame, bg="#1A1A1A", highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")

    scroll_y = ctk.CTkScrollbar(content_frame, orientation="vertical", command=canvas.yview)
    scroll_y.grid(row=0, column=1, sticky="ns")

    canvas.configure(yscrollcommand=scroll_y.set)

    # Create a container frame for movie sections
    content_container = ctk.CTkFrame(canvas, fg_color="transparent")
    canvas.create_window((0, 0), window=content_container, anchor="nw")

    categories = {
        "BlockBuster Movies": [{"id":140776,"title":"3 Idiots"},{"id":175185,"title":"PK"},{"id":74027,"title":"Lagaan"},{"id":121008,"title":"Life Of Pi"},{"id":34506,"title":"The Godfather"},{"id":147116,"title":"Inception"},{"id":19148,"title":"Avatar"},{"id":132597,"title":"The Wolf Of Wall Street"},{"id":185080,"title":"The Jungle Book"},],
        "Sci-Fi Movies": [{"id":40216,"title":"Gravity"},{"id":66093,"title":"Matrix"},{"id":147116,"title":"Inception"},{"id":150532,"title":"Oblivion"},{"id":152374,"title":"Elysium"},{"id":127928,"title":"Interstealler"},{"id":192797,"title":"Bring Him Home"}],
        #"Crime|Action|Thriller Movies": [{"id":189647,"title":"Murder On Orient Express"},{"id":190364,"title":" The Hateful Eight"},{"id":198160,"title":"Avengers Endgame"},{"id":168598,"title":"The Imitation Game"},{"id":40216,"title":"Gravity"},{"id":37663,"title":"Sholay"},{"id":52309,"title":"Godfellas"},{"id":55198,"title":"Reservoir Dogs"},],
        "Comedy Movies": [{"id":325766,"title":"Stree 2"},{"id":169396,"title":"Chennai Express"},{"id":153334,"title":"Zindgi Na Milegi Dobara"},{"id":154881,"title":"Midnight In Paris"},{"id":62456,"title":"Chicken Run"},],
        "Romance Movies": [{"id":62283,"title":"Titanic"},{"id":232138,"title":"Kabir Singh"},{"id":137253,"title":"Jab We Met"},{"id":58723,"title":"DDLJ"},{"id":193785,"title":"Bajirao Mastani"},],
        "Horror Movies":[{"id":40549,"title":"The Amity Ville"},{"id":185331,"title":"Conjoring 2"},{"id":22021,"title":"IT"},{"id":73681,"title":"The Sixth Sense"},{"id":45733,"title":"A Nightmare"},{"id":211390,"title":"Doctor Sleep"},{"id":174733,"title":"Babadook"},]
    }



    for category, movies in categories.items():
        create_movie_section(content_container, category, movies)


    content_container.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))


    app.mainloop()





























def graph_page(movieName):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title(f"Graphs for {movieName}")
    app.geometry("1100x500")
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)



    sidebar = ctk.CTkFrame(app, width=250, fg_color="#1A1A1A")
    sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

    logo_label = ctk.CTkLabel(
        sidebar,
        text="CinePhille",
        font=ctk.CTkFont(size=18, weight="bold")
    )
    logo_label.pack(pady=(10, 20))

    def go_back():
        app.destroy()
        dashboard()
        


    back_button = ctk.CTkButton(
        sidebar,
        text="Back",
        font=ctk.CTkFont(size=14, weight="bold"),
        command=go_back,
        fg_color="#FFA500",
        text_color="black",
        hover_color="#FFB84D",
    )
    back_button.pack(fill="x", pady=10)

    content_frame = ctk.CTkFrame(app, fg_color="transparent")
    content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    movieID = getMovieID(movieName)
    movieData = getGraphData(movieID)

    graph1OBJ = Visualiser1(movieData)
    graph2OBJ = Visualiser2(movieData)

    graph1_frame = ctk.CTkFrame(content_frame, fg_color="#2A2A2A", corner_radius=10)
    graph1_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

    canvas1 = FigureCanvasTkAgg(graph1OBJ.generate_graph(), master=graph1_frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill="both", expand=True)

    graph2_frame = ctk.CTkFrame(content_frame, fg_color="#2A2A2A", corner_radius=10)
    graph2_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    canvas2 = FigureCanvasTkAgg(graph2OBJ.generate_graph(), master=graph2_frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill="both", expand=True)

    app.mainloop()
















def movie_page(movie):
    move=movie
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    movie_data = datascraped.getMovieData(movie)
    movie_id=datascraped.getMovieID(movie)

    def open_graph_page():
        nonlocal move
        messagebox.showinfo("Graph Page", "Navigating to graph page...")
        app2.destroy()
        graph_page(move)


    app2 = ctk.CTk()
    app2.title("Movie Details")
    app2.geometry("900x500")


    main_frame = ctk.CTkFrame(app2)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)


    poster_frame = ctk.CTkFrame(main_frame, width=350)
    poster_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

    try:

        poster = Image.open(f"posters/{movie_id}.png")
        poster = poster.resize((200, 600), Image.Resampling.LANCZOS)
        poster_img = ctk.CTkImage(poster, size=(200, 600))
        poster_label = ctk.CTkLabel(poster_frame, image=poster_img, text="")
        poster_label.image = poster_img
        poster_label.pack(pady=10)
    except:
        try:
            datascraped.savePoster(movie)
            poster = Image.open(f"posters/{movie_id}.png")
            poster = poster.resize((200, 600), Image.Resampling.LANCZOS)
            poster_img = ctk.CTkImage(poster, size=(200, 600))
            poster_label = ctk.CTkLabel(poster_frame, image=poster_img, text="")
            poster_label.image = poster_img
            poster_label.pack(pady=10)
        except:
            error_label = ctk.CTkLabel(poster_frame, text="Poster not found", font=ctk.CTkFont(size=14, weight="bold"))
            error_label.pack(pady=10)


    # graph_button = ctk.CTkButton(poster_frame, text="Show Line Graph", command=open_graph_page, width=200)
    # graph_button.pack(pady=10)


    details_frame = ctk.CTkFrame(main_frame)
    details_frame.grid(row=0, column=1, sticky="nsew")


    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=2)
    main_frame.grid_rowconfigure(0, weight=1)


    movie_title_label = ctk.CTkLabel(details_frame, text=f"{movie_data['Title']} ({movie_data['Year']})",
                                     font=ctk.CTkFont(size=24, weight="bold"))
    movie_title_label.grid(row=0, column=0, sticky="w", pady=(10, 5))


    movie_genre = movie_data["Genre"]
    movie_genre = movie_genre.replace(",", "|")
    rating_label = ctk.CTkLabel(details_frame,
                                text=f"⭐ {movie_data["imdbRating"]}    {movie_data["Runtime"]}    {movie_genre}",
                                font=ctk.CTkFont(size=14))
    rating_label.grid(row=1, column=0, sticky="w", pady=(0, 10))


    director_label = ctk.CTkLabel(details_frame, text=f"Director: {movie_data["Director"]}", font=ctk.CTkFont(size=14))
    director_label.grid(row=2, column=0, sticky="w", pady=5)


    cast_label = ctk.CTkLabel(
        details_frame,
        text=f"Cast: {movie_data["Actors"]}",
        font=ctk.CTkFont(size=14),
        wraplength=500,
        justify="left"
    )
    cast_label.grid(row=3, column=0, sticky="w", pady=5)


    language_label = ctk.CTkLabel(details_frame, text=f"Language: {movie_data["Language"]}", font=ctk.CTkFont(size=14))
    language_label.grid(row=4, column=0, sticky="w", pady=5)


    plot_label = ctk.CTkLabel(details_frame, text="Plot:", font=ctk.CTkFont(size=16, weight="bold"))
    plot_label.grid(row=5, column=0, sticky="w", pady=(15, 5))
    plot = movie_data["Plot"].split(".")
    plot = f"{plot[0]}.{plot[1]}"
    plot_text = ctk.CTkLabel(
        details_frame,
        text=f"{plot}",
        font=ctk.CTkFont(size=14),
        wraplength=500,
        justify="left"
    )
    plot_text.grid(row=6, column=0, sticky="w", pady=10)


    is_favorite=False
    user_data=get_userdata(user_name[0])
    print(user_data.favourites,movie_id)
    
    for i in user_data.favourites:
        if( int(i) == int (movie_id)):
            is_favorite=True

    print(is_favorite)
    
    heart_label = None
    heart_img = None


    def toggle_favorite():
        nonlocal is_favorite, heart_label, heart_img,move,movie_id
        global user_name
       
        if not(is_favorite):
            heart_img = ctk.CTkImage(Image.open("heart_red.png").resize((40, 40), Image.Resampling.LANCZOS))
            messagebox.showinfo("Favorites", "Added to favorites!")
            print(user_name,move)
            is_favorite=True
            insert_favourites(user_name[0],move,movie_id)
        else:
            heart_img = ctk.CTkImage(Image.open("heart_gray.png").resize((40, 40), Image.Resampling.LANCZOS))
            messagebox.showinfo("Favorites", "Removed from favorites!")
            is_favorite=False
            delete_favourites(user_name[0],move)


        heart_label.configure(image=heart_img)
        heart_label.image = heart_img


    try:


        if(is_favorite):
            heart_img = ctk.CTkImage(
            Image.open("heart_red.png").resize((40, 40), Image.Resampling.LANCZOS))
        
        else:
            heart_img = ctk.CTkImage(
            Image.open("heart_gray.png").resize((40, 40), Image.Resampling.LANCZOS))
        heart_label = ctk.CTkLabel(details_frame, image=heart_img, text="")
        heart_label.image = heart_img
        heart_label.grid(row=0, column=1, sticky="e", padx=10)
        heart_label.bind("<Button-1>", lambda event: toggle_favorite())
    except:
        error_label = ctk.CTkLabel(details_frame, text="Heart icon not found", font=ctk.CTkFont(size=14, weight="bold"))
        error_label.grid(row=0, column=1, sticky="e", padx=10)


    graph_button = ctk.CTkButton(details_frame, text="Show Graph", command=open_graph_page, width=150)
    graph_button.grid(row=7, pady=20)

    def opendashboard():
        app2.destroy()
        dashboard()

    dashboardpage_button = ctk.CTkButton(details_frame, text="Go Back", command=opendashboard, width=150)
    dashboardpage_button.grid(row=8, pady=20)


    app2.mainloop()

























def search_movies():

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")


    app = ctk.CTk()
    app.title("🎥 Movie Search App")
    app.geometry("400x300")


    search_var = ctk.StringVar()

    def search_movie():
        nonlocal search_var
        movie_name = search_var.get()
        result_label.configure(text=f"🔎 Searching for: {movie_name}")
        app.destroy()
        movie_page(movie_name)
    def go_back():
        app.destroy()
        dashboard()


    search_label = ctk.CTkLabel(
        app, text="🔍 Search for a Movie:", text_color="white", font=("Arial", 16)
    )
    search_label.pack(pady=(20, 10))


    search_entry = ctk.CTkEntry(
        app, textvariable=search_var, placeholder_text="🎬 Enter movie name", width=300
    )
    search_entry.pack(pady=(0, 10))


    search_button = ctk.CTkButton(
        app, text="Search 🔎", command=search_movie, width=150
    )
    search_button.pack(pady=(0, 20))


    back_button = ctk.CTkButton(
        app,
        text="⬅️ Back",
        command=go_back,
        fg_color="#FFA500",
        text_color="black",
        width=150,
        hover_color="#FFB84D"
    )
    back_button.pack(pady=(0, 20))


    result_label = ctk.CTkLabel(
        app, text="", text_color="yellow", font=("Arial", 14)
    )
    result_label.pack(pady=(10, 0))


    app.mainloop()
















def favourites(user_name):

    userobject = get_userdata(user_name[0])
    favorites = userobject.favourites
    movie_list = []


    for movie_id in favorites:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(f"SELECT movieName FROM movies WHERE movieID = {movie_id}")
        name = cursor.fetchone()[0]
        db.close()
        movie_data = build_moviedata_object(movie_id,name)
        poster_path = f"posters/{movie_id}.png"
        movie_list.append({
            "title": movie_data.name,
            "poster": poster_path
        })


    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")


    app = ctk.CTk()
    app.geometry("900x500")
    app.title("Favorites Page")


    main_frame = ctk.CTkFrame(app, fg_color="#1A1A1A", corner_radius=15)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    title_label = ctk.CTkLabel(
        main_frame, text="My Favorite Movies",
        font=("Helvetica", 28, "bold"), text_color="#FFFFFF"
    )
    title_label.pack(pady=15)


    canvas = Canvas(
        main_frame, width=900, height=400,
        bg="#1A1A1A", highlightthickness=0
    )
    canvas.pack(padx=10, pady=10)


    scrollable_frame = ctk.CTkFrame(canvas, fg_color="#1A1A1A")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")


    images = []


    def add_rounded_corners(image, radius=20):
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, *image.size), radius, fill=255)
        rounded_image = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        rounded_image.putalpha(mask)
        return rounded_image


    def on_poster_click(movie_title):
        app.destroy()
        movie_page(movie_title)


    for movie in movie_list:
        try:

            img = Image.open(movie["poster"]).resize((150, 200))
            img = add_rounded_corners(img, radius=15)
        except Exception:
            img = Image.new("RGBA", (150, 200), color="gray")


        img_tk = ImageTk.PhotoImage(img)
        images.append(img_tk)


        movie_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        movie_frame.pack(side="left", padx=20, pady=10)


        poster_button = ctk.CTkButton(
            movie_frame,
            image=img_tk,
            width=150,
            height=200,
            text="",
            fg_color="transparent",
            hover_color="#FFB84D",
            command=lambda title=movie["title"]: on_poster_click(title)
        )
        poster_button.pack()


        title_label = ctk.CTkLabel(
            movie_frame,
            text=movie["title"],
            font=("Helvetica", 12, "bold"),
            text_color="#E0E0E0",
            wraplength=150,
            anchor="center"
        )
        title_label.pack(pady=5)




    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


    scrollbar = ctk.CTkScrollbar(main_frame, orientation="horizontal", command=canvas.xview)
    scrollbar.pack(fill="x", padx=10)
    canvas.configure(xscrollcommand=scrollbar.set)


    def on_mousewheel(event):
        canvas.xview_scroll(-1 * (event.delta // 120), "units")

    canvas.bind_all("<Shift-MouseWheel>", on_mousewheel)

    def go_back():
        app.destroy()
        dashboard()

    back_button = ctk.CTkButton(
    app,
    text="⬅️ Back",
    command=go_back,
    fg_color="#FFA500",
    text_color="black",
    width=150,
    hover_color="#FFB84D"
    )
    back_button.pack(pady=(0, 5))

    app.mainloop()














def movie_comp_page(movie1, movie2):
    movie1=build_moviedata_object(getMovieID(movie1),movie1)
    movie2=build_moviedata_object(getMovieID(movie2),movie2)
    app = ctk.CTk()
    app.title("Movie Comparison")
    app.geometry("900x700")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    title_label = ctk.CTkLabel(
        app,
        text=f"🎥 Movie Details: {movie1.name} vs {movie2.name}",
        font=("Helvetica", 26, "bold"),
        text_color="#FFFFFF",
    )
    title_label.pack(pady=20)

    content_frame = ctk.CTkFrame(app, fg_color="#2E2E2E", corner_radius=15)
    content_frame.pack(padx=20, pady=0, fill="both", expand=True)

    bottom_frame = ctk.CTkFrame(app, fg_color="#1E1E1E")
    bottom_frame.pack(fill="x", padx=20, pady=0)
    # id1 = datascraped.getMovieID(movie1)
    # id2 = datascraped.getMovieID(movie2)
    # data1 = datascraped.getMovieData(movie1)
    # data2 = datascraped.getMovieData(movie2)

    data = {
        movie1.name: {
            "poster": f"posters/{movie1.id}.png",
            "Director": f"{movie1.directors}",
            "Year": movie1.date,
            "Rating": f"⭐ {movie1.rating}",
            "Genre":movie1.genres,
            "Actors":movie1.actors
        },
        movie2.name: {
            "poster": f"posters/{movie2.id}.png",
            "Director":movie2.directors,
            "Year":movie2.date,
            "Rating": f"⭐ {movie2.rating}",
            "Genre":movie2.genres,
            "Actors":movie2.actors
        },
    }

    def add_movie_details(frame, movie_name):
        movie_data =data[movie_name]

        poster_img = Image.open(movie_data["poster"]).resize((200, 300))
        poster_tk = ctk.CTkImage(light_image=poster_img, size=(200, 300))

        # Poster Label
        poster_label = ctk.CTkLabel(frame, image=poster_tk, text="")
        poster_label.image = poster_tk
        poster_label.pack(pady=10)


        title_label = ctk.CTkLabel(
            frame,
            text=movie_name,
            font=("Helvetica", 22, "bold"),
            text_color="#E1E1E1",
        )
        title_label.pack(pady=5)

        details_text = (
            f"🎬 **Director**: {movie_data['Director']}\n"
            f"📅 **Year**: {movie_data['Year']}\n"
            f"🌟 **Rating**: {movie_data['Rating']}\n"
            f"📝 **Genre**: {movie_data["Genre"]}\n"
            f"   **Actors**: {movie_data["Actors"]}"
        )
        details_label = ctk.CTkLabel(
            frame,
            text=details_text,
            font=("Arial", 14, "italic"),
            text_color="#B0BEC5",
            justify="left",
            wraplength=300,
        )
        details_label.pack(pady=10, padx=5)

    def go_back():
        app.destroy()
        dashboard()


    movie1_frame = ctk.CTkFrame(content_frame, fg_color="#333333", corner_radius=10)
    movie1_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    add_movie_details(movie1_frame, movie1.name)

    movie2_frame = ctk.CTkFrame(content_frame, fg_color="#333333", corner_radius=10)
    movie2_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    add_movie_details(movie2_frame, movie2.name)


    back_button = ctk.CTkButton(
        bottom_frame,
        text="Back",
        font=ctk.CTkFont(size=16, weight="bold"),
        command=go_back,
        fg_color="#FFA500",
        text_color="black",
        hover_color="#FFB84D",
    )
    back_button.pack(pady=10)


    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)

    app.mainloop()


def open_movie_comparison_window():
    comparison_window = ctk.CTk()
    comparison_window.title("Compare Movies")
    comparison_window.geometry("600x450")
    comparison_window.configure(fg_color="#1E1E2F")

    title_label = ctk.CTkLabel(
        comparison_window,
        text="🎥 Compare Two Movies 🎥",
        font=("Arial", 24, "bold"),
        text_color="#FFFFFF",
    )
    title_label.pack(pady=20)

    input_frame = ctk.CTkFrame(comparison_window, fg_color="#2D2D3E", corner_radius=15)
    input_frame.pack(pady=20, padx=30, fill="both", expand=True)

    entry_movie1 = ctk.CTkEntry(
        input_frame,
        placeholder_text="Enter the first movie name",
        font=("Arial", 14),
        width=400,
        corner_radius=10,
    )
    entry_movie1.pack(pady=15, padx=20)
    entry_movie2 = ctk.CTkEntry(
        input_frame,
        placeholder_text="Enter the second movie name",
        font=("Arial", 14),
        width=400,
        corner_radius=10,
    )
    entry_movie2.pack(pady=15, padx=20)

    def compare_movies():
        movie1 = entry_movie1.get().strip()
        movie2 = entry_movie2.get().strip()
        print(movie1,movie2)

        if movie1 and movie2:
            comparison_window.destroy()
            movie_comp_page(movie1, movie2)
        else:
            comparison_result.set("⚠️ Please enter both movie names!")

    compare_button = ctk.CTkButton(
        input_frame,
        text="Compare",
        font=("Arial", 16, "bold"),
        fg_color="#4CAF50",
        hover_color="#3E8E41",
        command=compare_movies,
        corner_radius=8,
    )
    compare_button.pack(pady=20)

    def go_back():
        comparison_window.destroy()
        movie_comp()

    back_button = ctk.CTkButton(
        comparison_window,
        text="Back",
        font=ctk.CTkFont(size=16, weight="bold"),
        command=go_back,
        fg_color="#FFA500",
        text_color="black",
        hover_color="#FFB84D", )
    back_button.pack(pady=20)

    comparison_result = ctk.StringVar()
    result_label = ctk.CTkLabel(
        input_frame,
        textvariable=comparison_result,
        font=("Arial", 14),
        text_color="#FFFFFF",
        wraplength=500,
        justify="center",
    )
    result_label.pack(pady=20)
    comparison_window.mainloop()



def movie_comp():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    root.title("Movie Comparison")
    root.geometry("800x500")
    root.configure(fg_color="#121212")


    dashboard_label = ctk.CTkLabel(
        root,
        text="🎬 Welcome to Movie Comparison 🎬",
        font=("Arial", 28, "bold"),
        text_color="#FFFFFF",
    )
    dashboard_label.pack(pady=30)


    decor_frame = ctk.CTkFrame(root, fg_color="#1E1E2F", corner_radius=15, height=80)
    decor_frame.pack(fill="x", padx=40, pady=10)

    decor_label = ctk.CTkLabel(
        decor_frame,
        text="Explore, Compare, and Analyze Your Favorite Movies!",
        font=("Arial", 16, "italic"),
        text_color="#AAAAAA",
    )
    decor_label.pack(pady=15)


    def comp():
        root.destroy()
        open_movie_comparison_window()

    compare_window_button = ctk.CTkButton(
        root,
        text="🔍 Compare Movies",
        font=("Arial", 18, "bold"),
        fg_color="#4CAF50",
        hover_color="#3E8E41",
        command=comp,
        corner_radius=12,
    )
    compare_window_button.pack(pady=50)


    def go_back():
        root.destroy()
        dashboard()

    back_button = ctk.CTkButton(
        root,
        text="Back",
        font=ctk.CTkFont(size=16, weight="bold"),
        command=go_back,
        fg_color="#FFA500",
        text_color="black",
        hover_color="#FFB84D", )
    back_button.pack()
    root.mainloop()







ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Database connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shivansh6165",
    database="Cinephile_App"
)

if con.is_connected():
    print("Successfully connected to the database")
else:
    print("Failed to connect to the database")


def update_filter_values(*args):
    
    selected_filter = filter_option.get()
    dropdown_values = []

    try:
        cur = con.cursor()

        if selected_filter == "Genre":
            cur.execute("SELECT DISTINCT GenreName FROM Genres;")
        elif selected_filter == "Director":
            cur.execute("SELECT DISTINCT DirectorName FROM Directors;")
        elif selected_filter == "Actor":
            cur.execute("SELECT DISTINCT ActorName FROM Actors;")
        elif selected_filter == "Year":
            cur.execute("SELECT DISTINCT YEAR(MovieDate) FROM Movies;")
        elif selected_filter == "Rating":
            cur.execute("SELECT DISTINCT ROUND(MovieRating, 1) FROM Movies;")

        dropdown_values = [str(row[0]) for row in cur.fetchall()]

        

        # Clear and update the dropdown values
        filter_value_dropdown.set("")  # Clear current selection
        filter_value_dropdown.configure(values=dropdown_values)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update filter values: {e}")
    finally:
        cur.close()

# Function to handle selection submission
def update(app,btn,filter_value_dropdown):
    
    update_filter_values()
    selected_filter = filter_option.get()
    selected_value = filter_value_dropdown.get()


def generateReportPage(filter,option):
    display_results_window(filter,option)






def display_results_window(filter_by, filter_value):
    results_window = ctk.CTk()
    results_window.geometry("600x400")
    results_window.title("Filtered Results")

    try:
        cur = con.cursor()


        query = """
            SELECT DISTINCT MovieName, MovieDate, MovieRating
            FROM Movies
            JOIN Movie_Genre ON Movies.MovieID = Movie_Genre.MovieID
            JOIN Genres ON Movie_Genre.GenreID = Genres.GenreID
            JOIN Movie_Actor ON Movies.MovieID = Movie_Actor.MovieID
            JOIN Actors ON Movie_Actor.ActorID = Actors.ActorID
            JOIN Movie_Director ON Movies.MovieID = Movie_Director.MovieID
            JOIN Directors ON Movie_Director.DirectorID = Directors.DirectorID
        """

        if filter_by == "Genre":
            query += "WHERE GenreName = %s"
        elif filter_by == "Director":
            query += "WHERE DirectorName = %s"
        elif filter_by == "Actor":
            query += "WHERE ActorName = %s"
        elif filter_by == "Year":
            query += "WHERE YEAR(MovieDate) = %s"
        elif filter_by == "Rating":
            query += "WHERE ROUND(MovieRating, 1) = %s"

        cur.execute(query, (filter_value,))
        results = cur.fetchall()

        if not results:
            ctk.CTkLabel(results_window, text="No results found.", font=("Arial", 14)).pack(pady=20)
        else:
            output_lines = []
            for movie in results:
                movie_text = f"Name: {movie[0]}, Date: {movie[1]}, Rating: {movie[2]}"
                output_lines.append(movie_text)
                ctk.CTkLabel(results_window, text=movie_text, font=("Arial", 12)).pack(pady=5)

            # Save results to a file
            file_name = "reports/"+datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
            with open(file_name, "w") as file:
                file.write("\n".join(output_lines))
                
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch results: {e}")
    finally:
        cur.close()



    results_window.mainloop()
















def reportGeneratorPage():
    app = ctk.CTk()
    app.geometry("500x400")
    app.title("Movie Filter")

    
    def generateReport(filter,option):
        app.destroy()
        generateReportPage(filter,option)


    ctk.CTkLabel(app, text="Filter By:").pack(pady=10)
    global filter_option
    filter_option = ctk.CTkComboBox(app, values=["Genre", "Director", "Actor", "Year"])
    filter_option.pack(pady=10)



   


    btn=ctk.CTkButton(app, text="Update", command=lambda:update(app,btn,filter_value_dropdown), width=200).pack(pady=20)
    
    ctk.CTkLabel(app, text="Select Value:").pack(pady=10)
    global filter_value_dropdown
    filter_value_dropdown = ctk.CTkComboBox(app, values=[])
    filter_value_dropdown.pack(pady=10)

    
    btn2=ctk.CTkButton(app, text="Generate Report", command=lambda:generateReport(filter_option.get(),filter_value_dropdown.get()), width=200).pack(pady=20)

    app.mainloop()




login_page()
