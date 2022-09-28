import grpc

from protos import movie_pb2
from protos import movie_pb2_grpc
from protos import booking_pb2
from protos import booking_pb2_grpc
from protos import user_pb2
from protos import user_pb2_grpc
from protos import base_pb2
from protos import base_pb2_grpc

#MOVIES
def get_movie_by_id(stub:movie_pb2_grpc.MovieStub, id):
    movie = stub.GetMovieByID(id)
    print(movie)


def get_list_movies(stub:movie_pb2_grpc.MovieStub):
    allmovies = stub.GetListMovies(movie_pb2.Empty())
    for movie in allmovies:
        print("Movie called %s" % (movie.title))

def get_movies_by_title(stub:movie_pb2_grpc.MovieStub,title):
    movies = stub.GetMoviesByTitle(title)
    for movie in movies :
        print(f"Found {movie}")

def get_movies_by_director(stub:movie_pb2_grpc.MovieStub,director):
    movies = stub.GetMoviesByDirector(director)
    for movie in movies :
        print(f"Found {movie}")

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3001') as channel:
        stub = movie_pb2_grpc.MovieStub(channel)

        print("-------------- GetMovieByID --------------")
        movieid = movie_pb2.MovieID(id="a8034f44-aee4-44cf-b32c-74cf452aaaae")
        get_movie_by_id(stub, movieid)

        print("-------------- GetListMovies --------------")
        get_list_movies(stub)
        
        print("-------------- GetMoviesByTitle --------------")
        title = movie_pb2.MovieTitle(title="creed")
        get_movies_by_title(stub,title)

        print("-------------- GetMoviesByDirector --------------")
        director = movie_pb2.MovieDirector(director="ridley")
        get_movies_by_director(stub,director)

        channel.close()

#BOOKINGS
def get_booking_by_userId(stub:booking_pb2_grpc.BookingStub,userId):
    booking = stub.GetBookingByUserId(userId)
    print(booking)

def get_list_bookings(stub:booking_pb2_grpc.BookingStub):
    bookings = stub.GetAllBookings(base_pb2.Empty())
    for booking in bookings:
        print("Booking from %s" % (booking.userId))

def run2():
    with grpc.insecure_channel('localhost:3002') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        
        print("-------------- GetBookingById --------------")
        userId = user_pb2.UserID(id="dwight_schrute")
        get_booking_by_userId(stub=stub,userId=userId)

                
        print("-------------- GetListBookings --------------")
        get_list_bookings(stub=stub)

        channel.close()

run2()