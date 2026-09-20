# Movie Recommendation System

A content-based movie recommendation web app built with Python, Pandas, scikit-learn, and Streamlit.

The application lets a user enter a movie title and returns five movies with similar content. It uses movie metadata rather than user ratings, so it is a content-based recommendation system rather than a collaborative-filtering system.

## Features

- Search for a movie by title.
- Press **Enter** or click **Search** to run a recommendation.
- Display the entered movie and five recommended movies.
- Show a similarity score for each recommendation.
- Clear the selected movie and recommendations when the search box is cleared.
- Use a responsive Streamlit interface.

## How It Works

The recommendation pipeline is:

```text
Movie metadata
      |
      v
Cleaned movie data
      |
      v
TF-IDF text vectorization
      |
      v
Cosine similarity
      |
      v
Top five similar movies
```

TF-IDF converts the text in the movie tags into numerical vectors. Cosine similarity compares those vectors and identifies movies with similar content.

The current model is based on the cleaned data in `data/processed/movies_cleaned.csv`. The original TMDB files are stored in `data/raw/`.

## Project Structure

```text
Movie-Recommendation-System/
|
|-- app.py                         # Streamlit application
|-- requirements.txt               # Python dependencies
|-- README.md                      # Project documentation
|
|-- data/
|   |-- raw/
|   |   |-- tmdb_5000_movies.csv    # Original movie data
|   |   `-- tmdb_5000_credits.csv   # Original credits data
|   `-- processed/
|       `-- movies_cleaned.csv      # Data loaded by the app
|
|-- notebooks/
|   `-- 01_explore_dataset.ipynb   # Dataset exploration
|
`-- src/
    |-- model.py                    # TF-IDF and similarity model
    `-- recommender.py              # Recommendation logic
```

## Requirements

- Python 3.10 or newer is recommended.
- Git.
- A terminal such as PowerShell, Command Prompt, or a Unix shell.

## Clone the Project

Open a terminal and run:

```bash
git clone https://github.com/Rubayetrafsan07/Movie-Recommendation-System.git
cd Movie-Recommendation-System
```

## Install and Run

### Windows PowerShell

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start the application:

```powershell
streamlit run app.py
```

Streamlit will print a local URL, usually:

```text
http://localhost:8501
```

Open that URL in your browser.

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

## Using the Application

1. Type a movie title or part of a title in the search box.
2. Press **Enter** or click **Search**.
3. The application displays the text you entered under **Your Movie**.
4. The application displays five similar movies with their similarity scores.
5. Clear the search box to remove the current result.

The app uses a matching movie from the dataset internally when the search text is only part of a title. The displayed search text remains exactly what the user entered.

## Main Files

### `app.py`

Loads the processed dataset and creates the Streamlit interface. It handles search input, session state, result display, and calls the recommender.

### `src/model.py`

Creates a `TfidfVectorizer` from the movie `tags` column and calculates the cosine similarity matrix.

### `src/recommender.py`

Finds the requested movie in the dataset, sorts movies by similarity, and returns the top five recommendations.



## Dataset

This project uses the TMDB 5000 Movies Dataset. The raw files contain movie and credits information, while the processed CSV contains the tags used by the recommendation model.

The model can use information such as:

- Movie overview
- Genres
- Keywords
- Cast
- Director

## Troubleshooting

### `streamlit` is not recognized

Make sure the virtual environment is active, then run:

```bash
python -m streamlit run app.py
```

### A dependency installation fails

Check your Python version and recreate the virtual environment:

```bash
python --version
python -m venv .venv
```

Then activate the environment and run the installation commands again.

### The app cannot find the data file

Run Streamlit from the project root, the folder that contains `app.py` and the `data` directory:

```bash
streamlit run app.py
```

## Future Improvements

- Add movie posters and release information.
- Add genre and rating filters.
- Improve matching for misspelled titles.
- Add a larger or regularly updated dataset.
- Deploy the Streamlit app online.

## License and Data Notice

This project is for learning and demonstration purposes. The movie data comes from the TMDB 5000 Movies Dataset. Check the dataset's terms and attribution requirements before distributing or deploying the project.