import strawberry


@strawberry.type
class Movie:
    id:int
    title: str
    year: int
    rating: int


movies_db = [Movie(id=1, title="Gotfather", year=1990, rating=10), ]

def movies():
    return movies_db

def movie(movie_id:int):
    return movies_db[movie_id - 1]

def add_movie(title:str, year:int, rating:int):
    new_movie = Movie(id=len(movies_db) + 1, title=title, year=year, rating=rating)
    movies_db.append(new_movie)
    return new_movie


@strawberry.type
class Query:
    movies: list[Movie] = strawberry.field(resolver=movies)
    movie: Movie = strawberry.field(resolver=movie)


@strawberry.type
class Mutation:
    add_movie: Movie = strawberry.mutation(resolver=add_movie)



schema = strawberry.Schema(query=Query, mutation=Mutation)