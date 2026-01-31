import os
import random
import statistics
import movie_storage_sql as storage
from dotenv import load_dotenv

load_dotenv()


# =========================
# COMMANDS
# =========================

def list_movies():
    movies = storage.get_movies()
    print(f"\n{len(movies)} movies in total\n")

    for title, info in movies.items():
        print(f"{title} ({info['year']}): {info['rating']}")


def add_movie():
    title = input("Enter movie title: ").strip()
    storage.add_movie(title)


def delete_movie():
    title = input("Title to delete: ").strip()
    storage.delete_movie(title)


def update_movie():
    title = input("Title to update: ").strip()
    rating = float(input("New rating: "))
    storage.update_movie(title, rating)


def stats():
    movies = storage.get_movies()

    if not movies:
        print("No movies available.")
        return

    ratings = [m["rating"] for m in movies.values()]
    print(f"Average rating: {sum(ratings)/len(ratings):.2f}")
    print(f"Median rating: {statistics.median(ratings)}")


def random_movie():
    movies = storage.get_movies()

    if not movies:
        print("No movies available.")
        return

    title = random.choice(list(movies.keys()))
    print(title, movies[title])


def search_movie():
    query = input("Search title: ").strip()

    if not query:
        print("Empty search.")
        return

    results = storage.search_movies(query)

    if not results:
        print("No movies found.")
        return

    for title, info in results.items():
        print(f"{title} ({info['year']}): {info['rating']}")


def movies_sorted_by_rating():
    movies = storage.movies_sorted_by_rating()

    for title, info in movies.items():
        print(f"{info['rating']} – {title} ({info['year']})")


def generate_website():
    movies = storage.get_movies()

    with open("_static/index_template.html", encoding="utf-8") as f:
        html = f.read()

    grid = ""
    for title, info in movies.items():
        grid += f"""
        <li class="cards__item">
            <img src="{info['poster']}"/>
            <div class="card__title">{title}</div>
            <p>Year: {info['year']}<br>Rating: {info['rating']}</p>
        </li>
        """

    html = html.replace("__TEMPLATE_TITLE__", "My Movie App")
    html = html.replace("__TEMPLATE_MOVIE_GRID__", grid)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Website was generated successfully.")


# =========================
# MENU
# =========================

def print_menu():
    print("""
1. List movies
2. Add movie (API)
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Sort movies by rating
9. Generate website
0. Exit
""")


def main():
    while True:
        print_menu()
        choice = input("Choice: ").strip()

        if choice == "1":
            list_movies()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            delete_movie()
        elif choice == "4":
            update_movie()
        elif choice == "5":
            stats()
        elif choice == "6":
            random_movie()
        elif choice == "7":
            search_movie()
        elif choice == "8":
            movies_sorted_by_rating()
        elif choice == "9":
            generate_website()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
