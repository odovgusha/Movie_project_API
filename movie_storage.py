import json

MOVIES_FILE = "movies.json"



def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data. 

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    with open(MOVIES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    Assumes the JSON file already exists.
    """
    with open(MOVIES_FILE, "w", encoding="utf-8") as file:
        json.dump(movies, file, indent=4)


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
    save_movies(movies)
    print(f"Added '{title}' (Year: {year}, Rating: {rating}).\n")





def delete_movie(movies):
    title = input("Enter the exact title to delete: ").strip()
    if title in movies:
        del movies[title]
        print(f"Deleted '{title}'.\n")
    else:
        print(f"Movie '{title}' not found.\n")

    save_movies(movies)




def update_movie(movies):
    title = input("Enter title to update score: ").strip()

    if title not in movies:
        print(f"Movie '{title}' not found.\n")
        return

    new_rating = float(input("Enter new rating (0-10): ").strip())

    # update only the rating property
    movies[title]["rating"] = new_rating
    
    save_movies(movies)
    
    print(f"Updated '{title}' rating to {new_rating}.\n")
  