import grpc
from concurrent import futures
import pb2.movie_pb2 as movie_pb2
import pb2.movie_pb2_grpc as movie_pb2_grpc
import json

class MovieServicer(movie_pb2_grpc.MovieServicer):

    def __init__(self):
        with open('{}/data/movies.json'.format("."), "r") as jsf:
            self.db:list[str] = json.load(jsf)["movies"]

    def GetMovieByID(self, request, context):
        for movie in self.db:
            if movie['id'] == request.id:
                print("Movie found!")
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
        return movie_pb2.MovieData(title="", rating="", director="", id="")

    def GetListMovies(self, request, context):
        for movie in self.db:
            yield movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
    
    def GetMoviesByTitle(self, request, context):
        title:str = (request.title).lower()
        for movie in self.db:
            if movie['title'].lower().__contains__(title) :
                yield movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'],id=movie['id'])

    def GetMoviesByDirector(self, request, context):
        director:str = (request.director).lower()
        for movie in self.db:
            if movie['director'].lower().__contains__(director) :
                yield movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'],id=movie['id'])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    movie_pb2_grpc.add_MovieServicer_to_server(MovieServicer(), server)
    server.add_insecure_port('[::]:3001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
