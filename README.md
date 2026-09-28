# Movie Recommender System

Pick a movie and get **5 similar movies with posters**. It's a content-based recommender built with Python, scikit-learn and Streamlit.

**Live demo:** https://your-app-name.streamlit.app  <!-- replace with your Streamlit link -->

## How it works

1. **Data:** the TMDB 5000 Movies dataset (4,806 movies after cleaning).
2. **Tags:** for each movie, the overview, genres, keywords, top 3 actors and director are combined into one text.
3. **Vectors:** `CountVectorizer` (5,000 words, English stop words removed) turns each movie's tags into word counts.
4. **Similarity:** cosine similarity compares every movie with every other movie.
5. **App:** `app.py` shows the 5 movies with the highest scores and gets their posters from the TMDB API.

## Project files

| File | What it does |
| --- | --- |
| `notebook.ipynb` | Cleans the data and builds the model (run once) |
| `model/movie_list.pkl` | Movie IDs, titles and tags |
| `model/similarity.pkl` | Similarity scores, 185 MB (stored with Git LFS) |
| `app.py` | The Streamlit web app |
| `requirements.txt` | Libraries to install |
| `tmdb_5000_movies.csv`, `tmdb_5000_credits.csv` | Raw dataset (only needed to run the notebook) |

## Run the app

1. Install **Python 3.10+** from [python.org](https://www.python.org/downloads/) (tick **Add Python to PATH**) and **Git** from [git-scm.com](https://git-scm.com/) (Git LFS comes with it on Windows).
2. Download the project:
   ```bash
   git lfs install
   git clone https://github.com/jhshreya/movie-recommender.git
   cd movie-recommender
   ```
3. Install the libraries:
   ```bash
   py -m pip install -r requirements.txt
   ```
4. Start the app:
   ```bash
   py -m streamlit run app.py
   ```
5. Open **http://localhost:8501**, pick a movie and click **Show Recommendation**. Press **Ctrl + C** in the terminal to stop.

> On macOS/Linux, use `pip3` and `streamlit run app.py` instead of the `py -m` commands.

## Run the notebook (rebuild the model)

You only need this if you change how the model is built. The app already uses the files in `model/`.

1. If `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` aren't in the folder, download them from [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) and put them next to `notebook.ipynb`.
2. In VS Code, install the **Python** and **Jupyter** extensions.
3. Open `notebook.ipynb`, click **Select Kernel → Python Environments** and pick your Python.
4. Click **Run All**. The last cell prints `Saved model/movie_list.pkl and model/similarity.pkl`.
5. Restart the app to use the new model.

## Deploy (Streamlit Community Cloud)

1. Push the project to GitHub (the `.pkl` files go through Git LFS).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **Create app** → **Deploy a public app from GitHub**.
3. Repository `jhshreya/movie-recommender`, branch `main`, main file `app.py` → **Deploy**.
4. Every `git push` redeploys the app automatically.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `pip` or `streamlit` "not recognized" | Use `py -m pip ...` and `py -m streamlit run app.py` |
| All posters show "No Poster" | Your network may block TMDB. Change DNS to `8.8.8.8`, use a VPN or another network, then restart the app |
| `UnpicklingError: invalid load key` | The `.pkl` files didn't download. Run `git lfs pull` |
| `FileNotFoundError` in the notebook | Put both CSV files in the same folder as the notebook |

## Next steps

- Use `TfidfVectorizer` and stemming for better matches
- Merge the tables on movie ID instead of title (fixes duplicate titles like "Batman")
- Re-rank results by rating so the suggestions are also good movies
- Store only the top 10 neighbours per movie to shrink the 185 MB file

## Credits

Dataset: [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) on Kaggle. Posters: [TMDB](https://www.themoviedb.org/). This product uses the TMDB API but is not endorsed or certified by TMDB.

**Author:** [jhshreya](https://github.com/jhshreya)
