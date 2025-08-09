CREATE TABLE Complaints (
    ComplaintID VARCHAR(10) PRIMARY KEY,
    GuestID VARCHAR(10),
    RoomID VARCHAR(10),
    Description VARCHAR(255),
    Date DATE,
    FOREIGN KEY (GuestID) REFERENCES Guest(GuestID),
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);
