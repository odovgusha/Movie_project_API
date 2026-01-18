from sqlalchemy import create_engine, text
import requests


engine = create_engine("sqlite:///movies.db", echo=True)

# Create table
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
    """Read movies from DB"""
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT title, year, rating, poster FROM movies"
        ))

    return {
        row[0]: {
            "year": row[1],
            "rating": row[2],
            "poster": row[3]
        } for row in result.fetchall()
    }


def add_movie_from_api(title, api_key):
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
    data = requests.get(url).json()

    if data["Response"] == "False":
        print("Movie not found")
        return

    title = data["Title"]
    year = int(data["Year"][:4])
    rating = float(data["imdbRating"])
    poster = data["Poster"]

    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO movies (title, year, rating, poster)
            VALUES (:t, :y, :r, :p)
        """), {"t": title, "y": year, "r": rating, "p": poster})
        conn.commit()

    print(f"'{title}' added successfully.")


def delete_movie(title):
    with engine.connect() as conn:
        conn.execute(
            text("DELETE FROM movies WHERE title=:t"),
            {"t": title}
        )
        conn.commit()


def update_movie(title, rating):
    with engine.connect() as conn:
        conn.execute(text("""
            UPDATE movies
            SET rating=:r
            WHERE title=:t
        """), {"r": rating, "t": title})
        conn.commit()
