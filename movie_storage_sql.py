from sqlalchemy import create_engine, text
import requests
import os

# =========================
# DATABASE SETUP
# =========================

DB_URL = "sqlite:///movies.db"
engine = create_engine(DB_URL, echo=True)

# Create table once
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT
        )
    """))
    conn.commit()


# =========================
# CORE STORAGE API
# (JSON-compatible interface)
# =========================

def get_movies():
    """
    Load all movies from the database.
    Replacement for JSON get_movies().
    """
    with engine.connect() as conn:
        res = conn.execute(text(
            "SELECT title, year, rating, poster FROM movies"
        ))
        rows = res.fetchall()

    return {
        title: {
            "year": year,
            "rating": rating,
            "poster": poster
        }
        for title, year, rating, poster in rows
    }


def save_movies(_movies=None):
    """
    No-op for SQL storage.
    Exists only to keep the same API
    as the JSON version.
    """
    pass


def add_movie(title):
    """
    Add a movie using OMDb API.
    """
    api_key = os.getenv("API_KEY")

    if not api_key:
        print("API_KEY not found.")
        return

    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"

    try:
        data = requests.get(url, timeout=5).json()
    except Exception:
        print("API connection error.")
        return

    if data.get("Response") == "False":
        print("Movie not found.")
        return

    movie = {
        "title": data["Title"],
        "year": int(data["Year"][:4]),
        "rating": float(data["imdbRating"]) if data["imdbRating"] != "N/A" else 0.0,
        "poster": data.get("Poster", "")
    }

    with engine.connect() as conn:
        try:
            conn.execute(text("""
                INSERT INTO movies (title, year, rating, poster)
                VALUES (:title, :year, :rating, :poster)
            """), movie)
            conn.commit()
            print(f"'{movie['title']}' added successfully.")
        except Exception:
            print("Movie already exists.")


def delete_movie(title):
    """
    Delete a movie by title.
    """
    with engine.connect() as conn:
        res = conn.execute(
            text("DELETE FROM movies WHERE title = :t"),
            {"t": title}
        )
        conn.commit()

    if res.rowcount == 0:
        print("Movie not found.")
    else:
        print(f"'{title}' deleted.")


def update_movie(title, rating):
    """
    Update movie rating.
    """
    with engine.connect() as conn:
        res = conn.execute(text("""
            UPDATE movies
            SET rating = :r
            WHERE title = :t
        """), {"r": rating, "t": title})
        conn.commit()

    if res.rowcount == 0:
        print("Movie not found.")
    else:
        print(f"'{title}' updated.")


# =========================
# EXTRA DB QUERIES
# =========================

def search_movies(query):
    """
    Search movies by partial title.
    """
    with engine.connect() as conn:
        res = conn.execute(text("""
            SELECT title, year, rating, poster
            FROM movies
            WHERE title LIKE :q
        """), {"q": f"%{query}%"})
        rows = res.fetchall()

    return {
        t: {"year": y, "rating": r, "poster": p}
        for t, y, r, p in rows
    }


def movies_sorted_by_rating():
    """
    Return movies sorted by rating (DESC).
    """
    with engine.connect() as conn:
        res = conn.execute(text("""
            SELECT title, year, rating, poster
            FROM movies
            ORDER BY rating DESC
        """))
        rows = res.fetchall()

    return {
        t: {"year": y, "rating": r, "poster": p}
        for t, y, r, p in rows
    }
