from abc import ABC, abstractmethod

class Room(ABC):
    def __init__(self, guests):
        self.guests = guests
    
    @abstractmethod
    def nightly_rate(self):
        pass

class Single(Room):
    def nightly_rate(self):
        return 300_000
    
class Double(Room):
    def nightly_rate(self):
        return 500_000
    
class Suite(Room):
    def nightly_rate(self):
        return 1_200_000
    
class HotelManager:
    def __init__(self):
        self.bookings = []
    
    def book(self, room: Room):
        self.bookings.append(room)

    def run(self, exporter: Exporter, messenger: Messenger):
        exporter.export(self.bookings)
        messenger.notify(self.bookings)
    
class Exporter(ABC):
    @abstractmethod
    def export(self, bookings):
        pass

class Messenger(ABC):
    @abstractmethod
    def notify(self, bookings):
        pass
   
class CsvExporter(Exporter):
    def export(self, bookings):
        for room in bookings:
            print(f"{room.guests},{room.nightly_rate()}")


class SmsMessenger(Messenger):
    def notify(self, bookings):
        for room in bookings:
            print(f"[SMS → {room.guests}] Your room is booked at {room.nightly_rate()} €/night")

hotel = HotelManager()
hotel.book(Single("Luke"))
hotel.book(Double("Leia"))
hotel.book(Suite("Han"))

hotel.run(CsvExporter(), SmsMessenger())
