from sqlalchemy import create_engine, text
import requests

# Create SQLite DB file automatically
engine = create_engine("sqlite:///movies.db", echo=True)

# Create table (only once)
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            year INTEGER,
            rating REAL,
            poster TEXT
        )
    """))
    conn.commit()


def list_movies():
    """
    Read movies from database
    """
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT title, year, rating, poster FROM movies"
        ))
        rows = result.fetchall()

    # Convert SQL rows → dictionary
    return {
        row[0]: {
            "year": row[1],
            "rating": row[2],
            "poster": row[3]
        }
        for row in rows
    }


def add_movie_from_api(title, api_key):
    """
    Fetch movie data from OMDb API
    and store locally
    """
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
    data = requests.get(url).json()

    if data["Response"] == "False":
        print("Movie not found.")
        return

    # Extract from API
    title = data["Title"]
    year = int(data["Year"][:4])
    rating = float(data["imdbRating"])
    poster = data["Poster"]

    # Insert into database
    with engine.connect() as conn:
        try:
            conn.execute(text("""
                INSERT INTO movies (title, year, rating, poster)
                VALUES (:t, :y, :r, :p)
            """), {
                "t": title,
                "y": year,
                "r": rating,
                "p": poster
            })
            conn.commit()
            print("Movie added.")
        except:
            print("Movie already exists.")


def delete_movie(title):
    """
    Remove movie from DB
    """
    with engine.connect() as conn:
        result = conn.execute(
            text("DELETE FROM movies WHERE title=:t"),
            {"t": title}
        )
        conn.commit()

    if result.rowcount == 0:
        print("Movie not found.")
    else:
        print("Movie deleted.")


def update_movie(title, rating):
    """
    Update rating
    """
    with engine.connect() as conn:
        result = conn.execute(text("""
            UPDATE movies
            SET rating=:r
            WHERE title=:t
        """), {"r": rating, "t": title})
        conn.commit()

    if result.rowcount == 0:
        print("Movie not found.")
    else:
        print("Rating updated.")
