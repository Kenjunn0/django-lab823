import strawberry


@strawberry.type
class Movie:
    title: str
    year: int
    rating: int


movies_db = [Movie(title="Gotfather", year=1990, rating=10), ]


@strawberry.type
class Query:
    @strawberry.field
    def movies(self) -> list[Movie]:
        return movies_db

    @strawberry.field
    def movie(self, movie_id:int) -> Movie:
        return movies_db[movie_id - 1]


schema = strawberry.Schema(query=Query)
