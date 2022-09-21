import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json

EMPTY_BOOKING = {
    "userid" : "",
    "dates" : []
}

def createDateItem(date,movies)->booking_pb2.DateItem:
    item:booking_pb2.DateItem = booking_pb2.DateItem(date=date)
    item.moviesId.extend(movies)
    return item

def createBookingItem(booking):
    dates = list(map(
                    lambda date:
                        createDateItem(date=date["date"],movies=date["movies"]),
                    booking["dates"]
                ))
    booking_data = booking_pb2.BookingData(userId=booking['userid'])
    booking_data.date.extend(dates)
    return booking_data



class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db:list[str] = json.load(jsf)["bookings"]

    def GetBookingByUserId(self, request, context):
        for booking in self.db:
            if booking['userid'] == request.id:
                print("Booking found!")
                return createBookingItem(booking)

        return createBookingItem(EMPTY_BOOKING)

    def GetAllBookings(self, request, context):
        for booking in self.db:
            yield createBookingItem(booking)
 
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
