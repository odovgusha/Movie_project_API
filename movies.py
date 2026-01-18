import random
import statistics
import movie_storage_sql as storage

API_KEY = "PUT_YOUR_KEY_HERE"


def command_list_movies():
    movies = storage.list_movies()
    print(f"\n{len(movies)} movies in total\n")
    for title, info in movies.items():
        print(f"{title} ({info['year']}): {info['rating']}")


def command_add_movie():
    title = input("Enter movie title: ").strip()
    storage.add_movie_from_api(title, API_KEY)


def command_delete_movie():
    title = input("Title to delete: ").strip()
    storage.delete_movie(title)


def command_update_movie():
    title = input("Title to update: ").strip()
    rating = float(input("New rating: "))
    storage.update_movie(title, rating)


def command_stats():
    movies = storage.list_movies()
    ratings = [m["rating"] for m in movies.values()]

    print(f"Average: {sum(ratings)/len(ratings):.2f}")
    print(f"Median: {statistics.median(ratings)}")


def command_random():
    movies = storage.list_movies()
    title = random.choice(list(movies.keys()))
    print(title, movies[title])


def generate_website():
    movies = storage.list_movies()

    with open("_static/index_template.html") as f:
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

    with open("index.html", "w") as f:
        f.write(html)

    print("✅ Website was generated successfully.")


def print_menu():
    print("""
1. List movies
2. Add movie (API)
3. Delete movie
4. Update movie
5. Stats
6. Random movie
9. Generate website
0. Exit
""")


def main():
    while True:
        print_menu()
        c = input("Choice: ")

        if c == "1":
            command_list_movies()
        elif c == "2":
            command_add_movie()
        elif c == "3":
            command_delete_movie()
        elif c == "4":
            command_update_movie()
        elif c == "5":
            command_stats()
        elif c == "6":
            command_random()
        elif c == "9":
            generate_website()
        elif c == "0":
            break


if __name__ == "__main__":
    main()
