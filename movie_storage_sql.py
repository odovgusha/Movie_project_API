from sqlalchemy import create_engine, text
import requests

DB_URL = "sqlite:///movies.db"
engine = create_engine(DB_URL, echo=True)

# Create table (with poster column)
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


def list_movies():
    """Retrieve all movies from DB."""
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT title, year, rating, poster FROM movies"
        ))
        rows = result.fetchall()

    return {
        row[0]: {"year": row[1], "rating": row[2], "poster": row[3]}
        for row in rows
    }


def add_movie_from_api(title, api_key):
    """Fetch movie from OMDb and store in DB."""
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
    try:
        res = requests.get(url, timeout=5)
        data = res.json()
    except Exception:
        print("❌ API connection error.")
        return

    if data.get("Response") == "False":
        print("❌ Movie not found.")
        return

    title = data["Title"]
    year = int(data["Year"][:4])
    rating = float(data["imdbRating"])
    poster = data["Poster"]

    with engine.connect() as conn:
        try:
            conn.execute(text("""
                INSERT INTO movies (title, year, rating, poster)
                VALUES (:t, :y, :r, :p)
            """), {"t": title, "y": year, "r": rating, "p": poster})
            conn.commit()
            print(f"✅ '{title}' added successfully.")
        except Exception:
            print("❌ Movie already exists.")


def delete_movie(title):
    with engine.connect() as conn:
        res = conn.execute(
            text("DELETE FROM movies WHERE title=:t"),
            {"t": title}
        )
        conn.commit()

    if res.rowcount == 0:
        print("❌ Movie not found.")
    else:
        print(f"✅ '{title}' deleted.")


def update_movie(title, rating):
    with engine.connect() as conn:
        res = conn.execute(text("""
            UPDATE movies SET rating=:r WHERE title=:t
        """), {"r": rating, "t": title})
        conn.commit()

    if res.rowcount == 0:
        print("❌ Movie not found.")
    else:
        print(f"✅ '{title}' updated.")
