import random
import os
import statistics
import movie_storage


def print_title():
    print("*" * 10, "My Movies Database", "*" * 10)
    print()

def print_menu():
    print("Menu:")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")
    print("0. Quit")
    print()

"""
def handle_choice(choice,movies):
    if choice == "1":
        list_movies(movies)
    elif choice == "2":
        add_movie(movies)
    elif choice == "3":
        delete_movie(movies)
    elif choice == "4":
        update_movie(movies)
    elif choice == "5":
        stats(movies)
    elif choice == "6":
        random_movie(movies)
    elif choice == "7":
        search_movie(movies)
    elif choice == "8":
        movies_sorted_by_rating(movies)
    elif choice == "0":
        return False  # Quit
    else:
        print("Invalid choice. Please enter a number from 0 to 8.\n")
    return True  
"""
def handle_choice(choice,movies):
    if choice == "1":
        list_movies(movies)
    elif choice == "2":
        movie_storage.add_movie(movies)
    elif choice == "3":
        movie_storage.delete_movie(movies)
    elif choice == "4":
        movie_storage.update_movie(movies)
    elif choice == "5":
        stats(movies)
    elif choice == "6":
        random_movie(movies)
    elif choice == "7":
        search_movie(movies)
    elif choice == "8":
        movies_sorted_by_rating(movies)
    elif choice == "0":
        return False  # Quit
    else:
        print("Invalid choice. Please enter a number from 0 to 8.\n")
    return True  



def list_movies(movies):
    for i, (title, info) in enumerate(movies.items(), 1):
        print(f"{i}. {title} – {info['year']} – Rating {info['rating']}")


def add_movie(movies):
    
    title = input("Enter title: ").strip()
    if len(title) == 0:
        print("Title cannot be empty.\n")
        return
    if title in movies:
        print(f"'{title}' already exists. Use Update to change the rating.\n")
        return
    rating = float(input("Enter rating: ").strip())
    year = int(input("Enter year: ").strip())

    # store as a nested dictionary
    movies[title] = {
        "year": year,
        "rating": rating
    }

    print(f"Added '{title}' (Year: {year}, Rating: {rating}).\n")

def delete_movie(movies):
    title = input("Enter the exact title to delete: ").strip()
    if title in movies:
        del movies[title]
        print(f"Deleted '{title}'.\n")
    else:
        print(f"Movie '{title}' not found.\n")

def update_movie(movies):
    title = input("Enter title to update score: ").strip()

    if title not in movies:
        print(f"Movie '{title}' not found.\n")
        return

    new_rating = float(input("Enter new rating (0-10): ").strip())

    # update only the rating property
    movies[title]["rating"] = new_rating

    print(f"Updated '{title}' rating to {new_rating}.\n")

def stats(movies):
    if not movies:
        print("No movies to compute stats.\n")
        return

    # Extract only the ratings
    ratings = [info["rating"] for info in movies.values()]

    avg = sum(ratings) / len(ratings)
    med = statistics.median(ratings)

    max_score = max(ratings)
    min_score = min(ratings)

    # Find all movies with highest rating
    best_titles = [title for title, info in movies.items() if info["rating"] == max_score]

    # Find all movies with lowest rating
    worst_titles = [title for title, info in movies.items() if info["rating"] == min_score]

    print(f"Total movies: {len(movies)}")
    print(f"Average rating: {avg:.1f}")
    print(f"Median rating: {med:.1f}")
    print(f"Best: {', '.join(best_titles)}, Score: {max_score}")
    print(f"Worst: {', '.join(worst_titles)}, Score: {min_score}")


def random_movie(movies):
    if len(movies) == 0:
        print("No movies in the database.\n")
    movie = random.choice(list(movies.keys()))
    info = movies[movie]

    print(f"Random pick: {movie}, {info['year']}, {info['rating']}")

def search_movie(movies):
    q = input("Enter the title of the movie: ").strip().lower()
    if len(q) == 0:
        print("Empty query.\n")
        return

    found = False
    for title, rating in movies.items():
        if q in title.lower():
            print(f"- {title}: {rating}")
            found = True

    if not found:
        print("No matches.")



def movies_sorted_by_rating(movies):
    if not movies:
        print("No movies in the database.\n")
        return

    movie_list = [(title, info["rating"], info["year"]) for title, info in movies.items()]
    for i in range(len(movie_list)):
        for j in range(i + 1, len(movie_list)):
            if movie_list[i][1] < movie_list[j][1]:
                movie_list[i], movie_list[j] = movie_list[j], movie_list[i]
    for title, rating, year in movie_list:
        print(f"{rating}  {title} ({year})")

def pre_menu_prompt():
    while True:
        ans = input("Type 'm' to open the menu or 'q' to quit: ").strip().lower()
        if ans == 'q':
            return False
        if ans == 'm':
            return True
        print("Please type 'm' or 'q'.")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Dictionary to store the movies and the rating
    """
    movies = {
    "The Shawshank Redemption":{"year": 1994, "rating": 9.3},
    "The Shawshank Redemption 2":{"year": 1994, "rating": 9.3},
    "Pulp Fiction": {"year": 1994, "rating": 8.8},
    "The Godfather": {"year": 1972, "rating": 9.2},
    "The Godfather: Part II": {"year": 1974, "rating": 9.0},
    "The Dark Knight": {"year": 2008, "rating": 9.0},
    "12 Angry Men": {"year": 1957, "rating": 9.0},
    "Everything Everywhere All at Once":{"year": 2022, "rating": 8.5},
    "Forrest Gump": {"year": 1994, "rating": 8.8},
    "Star Wars: Episode V – The Empire Strikes Back": {"year": 1980, "rating": 8.7},
}
    """
    movies = movie_storage.get_movies()
    #print(movies)
    while True:
        print_title()
        #print()
        #clear_screen()

        print_menu()
        choice = input("Enter choice (0-8): ").strip()
        if not handle_choice(choice,movies):
            print("Goodbye!")
            break
            clear_screen()
        if not pre_menu_prompt():
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
