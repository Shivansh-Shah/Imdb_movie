#   IMDB RATINGS AND MOVIES

## Project Overview
TrendAnalyzer is a Python-based file  that visualizes movie data trends using graphs. It focuses on two key aspects:
- Total votes over time.
- Average ratings over time.

The file features an intuitive graphical user interface (GUI) built with `tkinter` and `customtkinter`, providing interactive and visually appealing charts powered by `matplotlib`.

## Features
1. **Graphical Visualization:**
   - Displays "Total Votes Over Time" with customizable x and y axes.
   - Displays "Average Rating Over Time" with user-friendly formatting.
2. **Responsive GUI:**
   - Sidebar for navigation and customization.
   - Integrated graphs embedded in the GUI.
3. **Dynamic Data Fetching:**
   - Retrieves movie data using the `datascraped.py` module.
4. **Custom Styling:**
   - Dark-themed interface with polished elements for better aesthetics.

## Screenshots
*(Add screenshots of the application here to highlight the GUI and the graphs.)*

## Dependencies
To run the project, the following libraries and tools are required:

- **Python Libraries:**
  ```bash
  pip install requests
  pip install beautifulsoup4
  python -m pip install mysql-connector-python
  pip install matplotlib
  pip install numpy
  pip install customtkinter
  pip install pillow
  ```
- **Database:**
  - MySQL (must be installed on your system).

## List of Libraries/APIs/Databases Used
- **Libraries:**
  - `tkinter`: For GUI elements.
  - `customtkinter`: For enhanced UI components.
  - `matplotlib`: For graph plotting.
  - `numpy`: For numerical computations.
  - `Pillow`: For image processing.
  - `requests` and `beautifulsoup4`: For web scraping in `datascraped.py`.
  - `mysql-connector-python`: For database interactions.

- **Database:**
  - MySQL: Stores and retrieves movie data used in visualizations.

## Class and Module Descriptions

### Modules:
1. **`datascraped.py`**:
   - Contains functions to fetch movie data:
     - `getMovieID(movieName)`: Fetches the ID for a given movie.
     - `getGraphData(movieID)`: Retrieves the data needed for graph generation.

### Classes:
1. **`Visualiser1` (Average Ratings Graph):**
   - Handles the creation of the "Average Rating Over Time" graph.
   - Customizes axes, labels, grid, and overall design.

2. **`Visualiser2` (Total Votes Graph):**
   - Handles the creation of the "Total Votes Over Time" graph.
   - Converts vote counts to thousands for readability and customizes the appearance.

### Functions:
1. **`graph_page(movieName)`**:
   - Creates the main GUI window for displaying the graphs.
   - Fetches the required data and embeds graphs within the app.
   - Includes navigation options and custom styling.

## How to Run
1. Install the dependencies listed above.
2. Ensure MySQL is installed and properly configured on your system.
3. Clone this repository and navigate to the project directory.
4. Run the following command to start the application:
   ```bash
   python trendanalyzer.py
   ```
5. Enter the name of a movie to generate and view its data trends.



- Include more customization options for graphs (e.g., color themes).
- Enhance error handling and input validation.

## License
*(Specify your project's license here, if applicable.)*

