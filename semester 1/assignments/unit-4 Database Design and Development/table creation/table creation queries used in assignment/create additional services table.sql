CREATE TABLE AdditionalServices (
    ServiceID VARCHAR(10) PRIMARY KEY,
    RoomID VARCHAR(10),
    ServiceName VARCHAR(50),
    ServiceCharge DECIMAL(10, 2),
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);
