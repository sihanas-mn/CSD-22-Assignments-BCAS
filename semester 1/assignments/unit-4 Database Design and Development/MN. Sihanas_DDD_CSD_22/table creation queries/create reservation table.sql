CREATE TABLE Reservation (
    ReservationID VARCHAR(10) PRIMARY KEY,
    GuestID VARCHAR(10),
    RoomID VARCHAR(10),
    StartDate DATE,
    EndDate DATE,
    NoGuest INT,
    PaymentStatus VARCHAR(20),
    FOREIGN KEY (GuestID) REFERENCES Guest(GuestID),
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);
