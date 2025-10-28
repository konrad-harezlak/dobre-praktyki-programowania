import csv
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

# Modele danych dla różnych typów danych
class Movie(BaseModel):
    movieId: int
    title: str
    genres: str

class Link(BaseModel):
    movieId: int
    imdbId: str
    tmdbId: int

class Rating(BaseModel):
    userId: int = Field(..., alias='user_id')
    movieId: int = Field(..., alias='movie_id')
    rating: float
    timestamp: int

class Tag(BaseModel):
    userId: int = Field(..., alias='user_id')
    movieId: int = Field(..., alias='movie_id')
    tag: str
    timestamp: int


# Funkcje do ładowania danych z plików CSV
def load_movies():
    # Otwórz plik CSV z kodowaniem 'utf-8'
    with open('movies.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        movies = []

        # Iteruj po wierszach w pliku
        for row in reader:
            movie = Movie(movieId=row['movieId'], title=row['title'], genres=row['genres'])
            movies.append(movie.__dict__)
    return movies

def load_links():
    links = []
    with open('links.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            link = Link(
                movie_id=int(row['movieId']),
                imdb_id=row['imdbId'],
                tmdb_id=int(row['tmdbId'])
            )
            links.append(link)
    return links

def load_ratings():
    ratings = []
    with open('ratings.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rating = Rating(
                user_id=int(row['userId']),
                movie_id=int(row['movieId']),
                rating=float(row['rating']),
                timestamp=int(row['timestamp'])
            )
            ratings.append(rating)
    return ratings

def load_tags():
    tags = []
    with open('tags.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tag = Tag(
                user_id=int(row['userId']),
                movie_id=int(row['movieId']),
                tag=row['tag'],
                timestamp=int(row['timestamp'])
            )
            tags.append(tag)
    return tags


# Endpointy API

@app.get("/", response_model=dict)
def read_root():
    return {"hello": "world"}

# Endpoint zwracający dane filmów
@app.get("/movies", response_model=List[Movie])
def get_movies():
    return load_movies()

# Endpoint zwracający dane o linkach do filmów
@app.get("/links", response_model=List[Link])
def get_links():
    return load_links()

# Endpoint zwracający dane o ocenach filmów
@app.get("/ratings", response_model=List[Rating])
def get_ratings():
    return load_ratings()

# Endpoint zwracający tagi filmów
@app.get("/tags", response_model=List[Tag])
def get_tags():
    return load_tags()
